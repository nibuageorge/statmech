import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from utils import apply_plot_style, render_sidebar_footer

st.set_page_config(
    page_title="08 — Grand Canonical Models: Ideal Gas vs. Localized Solid",
    layout="wide"
)

apply_plot_style()

st.title("08. Grand Canonical Ensemble: Classical Ideal Gas vs. Localized Particles")
st.markdown(
    "Based on **Chapter 4: Application to a Classical Ideal Gas** & "
    "**Application to a System of Independent Localised Particles** (Eqs. 4.4.1–4.4.24)"
)

# --- Sidebar Controls ---
st.sidebar.header("1. Classical Ideal Gas (Eqs. 4.4.1–4.4.12a)")
kinematic_regime = st.sidebar.radio(
    "Kinematic Regime f(T) = C Tⁿ",
    options=[
        "Non-Relativistic Monatomic Gas (n = 3/2)",
        "Relativistic / Photon Gas (n = 3)"
    ]
)
z_gas = st.sidebar.slider("Gas Fugacity z = exp(μ/kT)", min_value=0.05, max_value=2.0, value=0.50, step=0.05)
V_gas = st.sidebar.slider("Container Volume V (dimensionless)", min_value=10.0, max_value=200.0, value=50.0, step=10.0)
T_gas = st.sidebar.slider("Gas Dimensionless Temperature kT / ε₀", min_value=0.5, max_value=5.0, value=2.0, step=0.1)

st.sidebar.markdown("---")
st.sidebar.header("2. Localized Oscillator Lattice (Eqs. 4.4.13–4.4.24)")
x_target = st.sidebar.slider(
    "Convergence Parameter x = z φ(T) < 1 (Eq. 4.4.15)",
    min_value=0.50, max_value=0.995, value=0.95, step=0.005
)
T_over_theta = st.sidebar.slider(
    "Reduced Temperature kT / (ħω)",
    min_value=0.08, max_value=3.0, value=0.60, step=0.02
)

# --- 1. Classical Ideal Gas Calculations ---
n_exp = 1.5 if kinematic_regime.startswith("Non-Relativistic") else 3.0
f_T_gas = T_gas ** n_exp                  # f(T) = C * T^n with C = 1
q_gas = z_gas * V_gas * f_T_gas           # Eq. (4.4.4): q = ln Q = z V f(T)
N_bar_gas = q_gas                         # Eq. (4.4.6): N_bar = z V f(T)
P_gas = z_gas * T_gas * f_T_gas           # Eq. (4.4.5): P = z kT f(T)
U_gas = n_exp * N_bar_gas * T_gas         # Eq. (4.4.11a): U = n N kT
pressure_energy_ratio = P_gas / (U_gas / V_gas)  # Equals 1/n: 2/3 or 1/3

# --- 2. Localized Particles Calculations (Eqs. 4.4.15 - 4.4.24) ---
# Mean particle number Eq. (4.4.17): N_bar = x / (1 - x) where x = z * phi(T)
N_bar_loc = x_target / (1.0 - x_target)
# Pressure Eq. (4.4.16): P = -(kT / V) * ln(1 - x) -> 0 as V -> inf
P_loc = -(T_over_theta / V_gas) * np.log(1.0 - x_target)

# Quantum vs Classical 1D Harmonic Oscillator (u = hbar*omega / kT = 1 / T_over_theta)
u_curr = 1.0 / T_over_theta
# Eq. (4.4.23): phi_q = 1 / (2 sinh(u/2))
# U_q / N = (hbar*omega) * (1/2 + 1/(exp(u) - 1)) = (hbar*omega / 2) * coth(u/2)
E_per_particle_q = 0.5 * (1.0 / np.tanh(0.5 * u_curr))  # in units of hbar*omega
E_per_particle_c = T_over_theta                         # Eq. (4.4.24): U_c / N = kT

# --- Key Metrics Row ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Ideal Gas Mean ⟨N⟩ = q", f"{N_bar_gas:.2f}", f"PV / (⟨N⟩kT) = {P_gas * V_gas / (N_bar_gas * T_gas):.2f}")
c2.metric("Ideal Gas P / (U/V) = 1/n", f"{pressure_energy_ratio:.4f}", "2/3 (Non-rel) vs 1/3 (Rel)")
c3.metric("Localized Lattice Mean ⟨N⟩", f"{N_bar_loc:.1f}", f"P_solid = {P_loc:.4f} → 0 as V→∞")
c4.metric("Oscillator U/⟨N⟩ (Quantum vs Class)", f"{E_per_particle_q:.3f} vs {E_per_particle_c:.3f}", "Units of ħω (Zero-point = 0.500)")

# --- Plotting ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.2, 4.7), dpi=150)

# Panel 1: Classical Ideal Gas — Energy Density vs Pressure P = (1/n)(U/V)
u_dens_axis = np.linspace(0, 15.0, 200)
ax1.plot(u_dens_axis, (2.0 / 3.0) * u_dens_axis, color="#1f77b4", lw=2.2,
         label=r"Non-Relativistic ($n = 3/2$): $P = \frac{2}{3}\left(\frac{U}{V}\right)$")
ax1.plot(u_dens_axis, (1.0 / 3.0) * u_dens_axis, color="#d62728", lw=2.2, linestyle="--",
         label=r"Relativistic / Photon ($n = 3$): $P = \frac{1}{3}\left(\frac{U}{V}\right)$")

curr_u_dens = min(U_gas / V_gas, 14.5)
ax1.scatter([curr_u_dens], [(1.0 / n_exp) * curr_u_dens], color="#2ca02c", s=55, zorder=5,
            label=rf"Current State ($1/n = {1.0/n_exp:.2f}$)")
ax1.set_xlabel(r"Internal Energy Density $U / V$")
ax1.set_ylabel(r"Mechanical Pressure $P$")
ax1.set_title(r"Ideal Gas Equation of State: $P = \frac{1}{n}\left(\frac{U}{V}\right)$")
ax1.legend(loc="upper left", fontsize=8.3, framealpha=0.95)

# Panel 2: Localized Particles — Geometric Series Divergence of Q and <N> as z*phi(T) -> 1
x_grid = np.linspace(0.05, 0.985, 300)
Q_loc_curve = 1.0 / (1.0 - x_grid)       # Eq. (4.4.15): Q = [1 - z phi(T)]^(-1)
N_loc_curve = x_grid / (1.0 - x_grid)    # Eq. (4.4.17): N_bar = z phi(T) / [1 - z phi(T)]

ax2.plot(x_grid, Q_loc_curve, color="#1f77b4", lw=2.2, label=r"Grand Partition $\mathcal{Q} = [1 - z\phi(T)]^{-1}$")
ax2.plot(x_grid, N_loc_curve, color="#2ca02c", lw=2.2, linestyle="--", label=r"Mean Particles $\overline{N} = \frac{z\phi(T)}{1 - z\phi(T)}$")
ax2.axvline(1.0, color="#d62728", linestyle=":", lw=1.6, label=r"Convergence Bound $z\phi(T) = 1$")
if x_target <= 0.985:
    ax2.scatter([x_target], [N_bar_loc], color="#9467bd", s=50, zorder=5)

ax2.set_ylim(0, 70)
ax2.set_xlabel(r"Dimensionless Parameter $x = z\phi(T)$")
ax2.set_ylabel(r"$\mathcal{Q}$ and $\overline{N}$")
ax2.set_title(r"Localized System: Macroscopic $\overline{N} \gg 1$ Requires $z\phi(T) \to 1^-$")
ax2.legend(loc="upper left", fontsize=8.3, framealpha=0.95)

# Panel 3: Quantum vs Classical 1D Harmonic Oscillator Lattice (Eqs. 4.4.23 & 4.4.24)
t_red = np.linspace(0.06, 2.5, 300)
u_red = 1.0 / t_red

# Mean energy per oscillator U / (N * hbar * omega)
U_quantum = 0.5 * (1.0 / np.tanh(0.5 * u_red))
U_classical = t_red

# Heat capacity per oscillator C_V / (N * k) = (u/2)^2 / sinh^2(u/2)
Cv_quantum = ((0.5 * u_red) / np.sinh(0.5 * u_red)) ** 2
Cv_classical = np.ones_like(t_red)

ax3.plot(t_red, U_quantum, color="#1f77b4", lw=2.2, label=r"Quantum $U/(\overline{N}\hbar\omega)$ (Eq. 4.4.23)")
ax3.plot(t_red, U_classical, color="#1f77b4", lw=1.7, linestyle="--", label=r"Classical $U/(\overline{N}\hbar\omega) = kT/\hbar\omega$ (Eq. 4.4.24)")
ax3.plot(t_red, Cv_quantum, color="#d62728", lw=2.2, label=r"Quantum $C_V / (\overline{N}k)$")
ax3.plot(t_red, Cv_classical, color="#d62728", lw=1.7, linestyle="--", label=r"Classical $C_V / (\overline{N}k) = 1$")

ax3.axvline(T_over_theta, color="#444444", linestyle=":", lw=1.3)
ax3.set_xlabel(r"Reduced Temperature $kT / (\hbar\omega)$")
ax3.set_ylabel(r"Dimensionless Energy & Heat Capacity")
ax3.set_title("Quantum vs. Classical 1D Oscillator Lattice")
ax3.legend(loc="upper left", fontsize=7.8, framealpha=0.95)

plt.tight_layout()
st.pyplot(fig)

with st.expander("Classroom Derivation Reference (Equations from Lecture Notes)", expanded=False):
    st.latex(r"\mathcal{Q}(z,V,T) = \exp\{zVf(T)\} \implies q = zVf(T), \qquad PV = \overline{N}kT, \qquad P = \frac{1}{n}\left(\frac{U}{V}\right) \qquad (4.4.4,\; 4.4.10)")
    st.latex(r"\mathcal{Q}(z,V,T) = \sum_{N_r=0}^{\infty} [z\phi(T)]^{N_r} = [1 - z\phi(T)]^{-1}, \qquad \overline{N} = \frac{z\phi(T)}{1 - z\phi(T)} \qquad (4.4.15,\; 4.4.17)")
    st.latex(r"\phi_{\text{quantum}}(T) = \frac{1}{2\sinh\left(\frac{\hbar\omega}{2kT}\right)} \xrightarrow{\hbar\omega \ll kT} \phi_{\text{classical}}(T) = \frac{kT}{\hbar\omega} \qquad (4.4.23,\; 4.4.24)")

render_sidebar_footer()