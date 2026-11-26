import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.special import gammaln
from utils import apply_plot_style, render_sidebar_footer

st.set_page_config(
    page_title="03 — 3N Hypersphere & Ideal Gas Processes",
    layout="wide"
)

apply_plot_style()

st.title("03. $3N$-Dimensional Hypersphere State Counting & Ideal Gas Processes")
st.markdown(
    "Based on **Chapter 1: Application to a Classical Ideal Gas** "
    "(Eqs. 1.4.5–1.4.29)"
)

# --- Sidebar Controls ---
st.sidebar.header("Quantum Box & Hypersphere Parameters")
E_star = st.sidebar.slider(
    "Dimensionless Energy Parameter E* = 8mV^(2/3)E / h²",
    min_value=10.0, max_value=250.0, value=64.0, step=2.0
)
N_particles = st.sidebar.slider(
    "Number of Particles N (for Shell Sensitivity Check)",
    min_value=2, max_value=200, value=20, step=2
)
delta_frac = st.sidebar.slider(
    "Relative Energy Shell Thickness (Δ / E)",
    min_value=0.001, max_value=0.20, value=0.05, step=0.005
)

st.sidebar.markdown("---")
st.sidebar.header("Thermodynamic Expansion Parameters")
V_init = st.sidebar.slider("Initial Volume Vᵢ (dimensionless)", min_value=1.0, max_value=5.0, value=1.0, step=0.2)
V_final = st.sidebar.slider("Final Volume V_f (dimensionless)", min_value=1.5, max_value=10.0, value=4.0, step=0.2)
T_init = st.sidebar.slider("Initial Temperature kTᵢ (units of ε₀)", min_value=1.0, max_value=10.0, value=4.0, step=0.5)

# --- 1. Positive Octant Lattice Point Counting (3D Projection: n_x^2 + n_y^2 + n_z^2 <= E*) ---
R_sphere = np.sqrt(E_star)
n_max = int(np.floor(R_sphere))
grid_1d = np.arange(1, max(n_max + 1, 2))
nx, ny, nz = np.meshgrid(grid_1d, grid_1d, grid_1d, indexing="ij")
r2 = nx**2 + ny**2 + nz**2
inside_mask = r2 <= E_star

nx_in, ny_in, nz_in = nx[inside_mask], ny[inside_mask], nz[inside_mask]
exact_lattice_count = len(nx_in)
# Eq. (1.4.13) for N = 1 (3D positive octant: (1/8) * (4/3)*pi*R^3)
continuous_octant_vol = (1.0 / 8.0) * (4.0 / 3.0) * np.pi * (R_sphere ** 3)

# --- 2. Shell Thickness Sensitivity (Eq. 1.4.17 vs Eq. 1.4.18) ---
# Compute ln Sigma and ln Gamma using exact gammaln(3N/2 + 1)
# Taking V / h^3 * (2*pi*m*E)^(3/2) proportional to (E*)^(3/2) * (pi/4)^(3/2)
dim = 3 * N_particles
ln_Sigma = (
    -dim * np.log(2.0)
    + (dim / 2.0) * np.log(np.pi)
    - gammaln(0.5 * dim + 1.0)
    + (dim / 2.0) * np.log(E_star)
)
shell_correction = np.log(0.5 * dim) + np.log(delta_frac)
ln_Gamma = ln_Sigma + shell_correction
rel_shell_diff = abs(shell_correction / ln_Sigma) * 100.0

# --- 3. Isothermal vs Adiabatic Processes (Eqs. 1.4.27 - 1.4.29) ---
gamma = 5.0 / 3.0  # Eq. (1.4.26)
V_arr = np.linspace(V_init, V_final, 300)

# Scale per particle (P / N in units of ε₀ / V₀)
P_init = T_init / V_init
P_isothermal = T_init / V_arr
P_adiabatic = P_init * ((V_init / V_arr) ** gamma)

T_final_adiab = T_init * ((V_init / V_final) ** (gamma - 1.0))
dS_isothermal_per_Nk = np.log(V_final / V_init)  # Eq. (1.4.27)
dE_adiabatic_per_Nk = 1.5 * (T_final_adiab - T_init)  # Eq. (1.4.21) & (1.4.29)

# --- Key Metrics Row ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Hypersphere Radius √E*", f"{R_sphere:.2f}", f"Exact 1-Particle States: {exact_lattice_count}")
c2.metric("Continuous Octant Approx Σ", f"{continuous_octant_vol:.1f}", f"Error: {abs(exact_lattice_count - continuous_octant_vol)/max(exact_lattice_count,1)*100:.1f}%")
c3.metric("Shell Correction |ln(3NΔ/2E) / ln Σ|", f"{rel_shell_diff:.2f}%", "Vanishes as N → ∞ (Eq. 1.4.18)")
c4.metric("Adiabatic Final Temp kT_f", f"{T_final_adiab:.2f} ε₀", f"γ = 5/3; ΔS_iso / Nk = {dS_isothermal_per_Nk:.3f}")

# --- Plotting ---
fig = plt.figure(figsize=(15.2, 4.7), dpi=150)

# Panel 1: 3D Positive Octant (n_x > 0, n_y > 0, n_z > 0) for N = 1
ax1 = fig.add_subplot(1, 3, 1, projection="3d")
ax1.set_facecolor("white")
if exact_lattice_count > 0:
    ax1.scatter(nx_in, ny_in, nz_in, c=nx_in**2 + ny_in**2 + nz_in**2, cmap="viridis", s=18, alpha=0.85)

# Wireframe of positive octant surface
u = np.linspace(0, np.pi / 2, 24)
v = np.linspace(0, np.pi / 2, 24)
xs = R_sphere * np.outer(np.cos(u), np.sin(v))
ys = R_sphere * np.outer(np.sin(u), np.sin(v))
zs = R_sphere * np.outer(np.ones_like(u), np.cos(v))
ax1.plot_wireframe(xs, ys, zs, color="#d62728", alpha=0.25, lw=0.8)

ax1.set_title(r"Positive Octant ($n_x,n_y,n_z > 0$) for $N=1$")
ax1.set_xlabel(r"$n_x$")
ax1.set_ylabel(r"$n_y$")
ax1.set_zlabel(r"$n_z$")
ax1.set_xlim(0, R_sphere * 1.05)
ax1.set_ylim(0, R_sphere * 1.05)
ax1.set_zlim(0, R_sphere * 1.05)

# Panel 2: ln Gamma vs ln Sigma across N (Eq. 1.4.17 vs 1.4.18)
ax2 = fig.add_subplot(1, 3, 2)
N_scan = np.arange(2, 205, 2)
dim_scan = 3 * N_scan
ln_Sigma_scan = (
    -dim_scan * np.log(2.0)
    + (dim_scan / 2.0) * np.log(np.pi)
    - gammaln(0.5 * dim_scan + 1.0)
    + (dim_scan / 2.0) * np.log(E_star)
)
ln_Gamma_scan = ln_Sigma_scan + np.log(0.5 * dim_scan) + np.log(delta_frac)

ax2.plot(N_scan, ln_Sigma_scan, color="#1f77b4", lw=2.2, label=r"Cumulative $\ln \Sigma(N,V,E)$ (Eq. 1.4.15)")
ax2.plot(N_scan, ln_Gamma_scan, color="#d62728", lw=2.0, linestyle="--", label=r"Thin Shell $\ln \Gamma(N,V,E;\Delta)$ (Eq. 1.4.17)")
ax2.axvline(N_particles, color="#444444", linestyle=":", lw=1.3)
ax2.scatter([N_particles], [ln_Gamma], color="#d62728", s=45, zorder=5)
ax2.set_title(r"Insensitivity to Shell Thickness $\Delta$ ($N \gg 1$)")
ax2.set_xlabel(r"Number of Particles $N$")
ax2.set_ylabel(r"$\ln \Sigma$ and $\ln \Gamma$")
ax2.legend(loc="best", fontsize=8.5, framealpha=0.95)

# Panel 3: Isothermal vs Adiabatic Expansion (Eqs. 1.4.27 - 1.4.29)
ax3 = fig.add_subplot(1, 3, 3)
ax3.plot(V_arr, P_isothermal, color="#1f77b4", lw=2.3, label=r"Isothermal ($T=\text{const}$): $PV = NkT$")
ax3.plot(V_arr, P_adiabatic, color="#2ca02c", lw=2.3, linestyle="--", label=r"Adiabatic ($S=\text{const}$): $PV^{5/3} = \text{const}$")
ax3.fill_between(V_arr, P_adiabatic, P_isothermal, color="#9467bd", alpha=0.14, label="Work Difference")
ax3.scatter([V_init, V_final, V_final], [P_init, P_isothermal[-1], P_adiabatic[-1]], color="#111111", s=35, zorder=5)

ax3.set_title(r"Isothermal vs. Adiabatic Expansion ($\gamma = 5/3$)")
ax3.set_xlabel(r"Volume $V$")
ax3.set_ylabel(r"Pressure $P / N$ ($\varepsilon_0 / V_0$)")
ax3.legend(loc="upper right", fontsize=8.5, framealpha=0.95)

plt.tight_layout()
st.pyplot(fig)

with st.expander("Classroom Derivation Reference (Equations from Lecture Notes)", expanded=False):
    st.latex(r"\sum_{r=1}^{3N} n_r^2 = \frac{8mV^{2/3}E}{h^2} \equiv E^* \qquad (1.4.7)")
    st.latex(r"\Sigma(N,V,E) \approx \left(\frac{1}{2}\right)^{3N}\left\{\frac{\pi^{3N/2}}{(3N/2)!}(E^*)^{3N/2}\right\} = \frac{1}{(3N/2)!}\left[\frac{V}{h^3}(2\pi mE)^{3/2}\right]^N \qquad (1.4.13,\; 1.4.14)")
    st.latex(r"\ln\Gamma \approx \ln\Sigma + \left\{\ln\left(\frac{3N}{2}\right) + \ln\left(\frac{\Delta}{E}\right)\right\} \approx \ln\Sigma \qquad (1.4.17,\; 1.4.18)")
    st.latex(r"S_f - S_i = Nk\ln\left(\frac{V_f}{V_i}\right) \quad (\text{Isothermal}), \qquad PV^{5/3} = \text{const},\; TV^{2/3} = \text{const} \quad (\text{Adiabatic}) \qquad (1.4.27,\; 1.4.28)")

render_sidebar_footer()