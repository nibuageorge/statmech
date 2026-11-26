import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from utils import apply_plot_style, render_sidebar_footer

st.set_page_config(
    page_title="06 — Canonical Energy Fluctuations",
    layout="wide"
)

apply_plot_style()

st.title("06. Canonical Energy Fluctuations & Equivalence with Microcanonical Ensemble")
st.markdown(
    "Based on **Chapter 3: Energy Fluctuations: Equivalence with the Microcanonical Ensemble** "
    "(Eqs. 3.6.3–3.6.10 & Page 43 Diagram)"
)

# --- Sidebar Controls ---
st.sidebar.header("Canonical System Parameters")
N_particles = st.sidebar.slider(
    "Number of Monatomic Gas Particles N (Note Page 43 starts at N = 10)",
    min_value=4, max_value=1000, value=10, step=2
)
kT_val = st.sidebar.slider(
    "Thermal Energy kT (units of ε₀)",
    min_value=0.5, max_value=5.0, value=1.5, step=0.1
)
show_gaussian_approx = st.sidebar.checkbox(
    "Overlay Gaussian Approximation (Eq. 3.6.8)",
    value=True
)

# --- Exact Formulas from Lecture Notes (Monatomic Classical Ideal Gas) ---
# Eq. (1.4.21) & (1.4.22): U = (3/2) N kT, C_V = (3/2) N k
f_half = 1.5 * N_particles               # 3N / 2
U_mean = f_half * kT_val                 # Macroscopic internal energy U = E*
Cv_over_k = f_half                       # C_V / k = 3N / 2

# Eq. (3.6.3) & (3.6.4): Variance <(ΔE)^2> = k T^2 C_V = (kT)^2 * (C_V / k)
sigma_E = kT_val * np.sqrt(Cv_over_k)
rel_fluctuation = sigma_E / U_mean       # Equals sqrt(2 / (3N)) ~ 1 / sqrt(N)

# Energy grid centered around U_mean
e_min = max(1e-4 * U_mean, U_mean - 4.5 * sigma_E)
e_max = U_mean + 4.5 * sigma_E
E_grid = np.linspace(e_min, e_max, 1500)
beta = 1.0 / kT_val

# Log-space evaluation to avoid overflow at large N:
# g(E) ~ E^(3N/2 - 1), Boltzmann factor = exp(-beta * E)
exponent_g = f_half - 1.0
ln_g = exponent_g * np.log(E_grid)
ln_boltz = -beta * E_grid
ln_prod = ln_g + ln_boltz

# Normalize each curve to peak = 1.0 over the plotted window (matching Page 43 schematic)
ln_prod_max = np.max(ln_prod)
prod_norm = np.exp(ln_prod - ln_prod_max)

# Scale g(E) and exp(-beta E) smoothly around E* = U for visual clarity
g_vis = np.exp(ln_g - exponent_g * np.log(U_mean)) * 0.55
boltz_vis = np.exp(-beta * (E_grid - U_mean)) * 0.55
# Clip steep tails for clean display
g_vis = np.clip(g_vis, 0, 1.35)
boltz_vis = np.clip(boltz_vis, 0, 1.35)

# Gaussian approximation Eq. (3.6.8): exp(-(E - U)^2 / (2 k T^2 C_V))
gaussian_approx = np.exp(-((E_grid - U_mean) ** 2) / (2.0 * (sigma_E ** 2)))

# Finite-N logarithmic correction ratio in Eq. (3.6.9):
# | (1/2) kT ln(2*pi*(kT)^2*(C_V/k)) | / U
log_corr = 0.5 * kT_val * np.log(2.0 * np.pi * (kT_val ** 2) * Cv_over_k)
rel_free_energy_corr = abs(log_corr / U_mean) * 100.0

# --- Key Metrics Row ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Most Probable Energy E* = U", f"{U_mean:.2f} ε₀", f"(3/2) N kT")
c2.metric("RMS Spread σ_E = √(kT²C_V)", f"{sigma_E:.2f} ε₀", f"C_V / k = {Cv_over_k:.1f}")
c3.metric("Relative Fluctuation σ_E / U", f"{rel_fluctuation:.4f}", f"√(2/3N) = {np.sqrt(2.0/(3.0*N_particles)):.4f}")
c4.metric("O(ln N) / O(N) Correction (Eq. 3.6.9)", f"{rel_free_energy_corr:.2f}%", "Vanishes as N → ∞")

# --- Plotting ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.2, 4.7), dpi=150)

# Panel 1: Exact Recreation of Page 43 Three-Curve Diagram: g(E), exp(-βE), and g(E)exp(-βE)
ax1.plot(E_grid, g_vis, color="#ff7f0e", lw=2.0, label=r"Density of States $g(E) \propto E^{\frac{3N}{2}-1}$")
ax1.plot(E_grid, boltz_vis, color="#1f77b4", lw=2.0, label=r"Boltzmann Factor $e^{-\beta E}$")
ax1.plot(E_grid, prod_norm, color="#111111", lw=2.4, label=r"Product $g(E)e^{-\beta E}$ (Normalized)")
ax1.fill_between(E_grid, 0, prod_norm, color="#38bdf8", alpha=0.35)

if show_gaussian_approx:
    ax1.plot(
        E_grid, gaussian_approx, color="#d62728", lw=1.8, linestyle="--",
        label=r"Gaussian: $\exp\left[-\frac{(E-U)^2}{2kT^2C_V}\right]$ (Eq. 3.6.8)"
    )

ax1.axvline(U_mean, color="#2ca02c", linestyle=":", lw=1.6, label=rf"$E^* = U = {U_mean:.1f}$")
ax1.set_ylim(0, 1.22)
ax1.set_xlabel(r"System Energy $E$ ($\varepsilon_0$)")
ax1.set_ylabel(r"Relative Amplitude")
ax1.set_title(rf"Sharp Peak of $g(E)e^{{-\beta E}}$ at $N = {N_particles}$ (Page 43)")
ax1.legend(loc="upper right", fontsize=8.0, framealpha=0.95)

# Panel 2: Reduced Variable Distribution P(E / U) Across System Sizes
reduced_E = np.linspace(0.4, 1.6, 1000)
N_examples = [10, 50, 250, 1000]
colors_ex = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

for n_ex, col in zip(N_examples, colors_ex):
    # Relative variance = 2 / (3 * n_ex)
    rel_var = 2.0 / (3.0 * n_ex)
    p_red = np.exp(-((reduced_E - 1.0) ** 2) / (2.0 * rel_var))
    ax2.plot(reduced_E, p_red, color=col, lw=2.0, label=rf"$N = {n_ex}$ ($\sigma_E/U = {np.sqrt(rel_var):.3f}$)")

ax2.axvline(1.0, color="#111111", linestyle=":", lw=1.3)
ax2.set_xlabel(r"Reduced Energy Variable $E / U$")
ax2.set_ylabel(r"Normalized Probability $P(E/U)$")
ax2.set_title(r"Collapse Toward Dirac $\delta(E/U - 1)$ as $N \to \infty$")
ax2.set_ylim(0, 1.15)
ax2.legend(loc="upper right", fontsize=8.3, framealpha=0.95)

# Panel 3: 1 / sqrt(N) Scaling Law (Eq. 3.6.4)
N_axis = np.linspace(4, 1000, 400)
rel_fluct_curve = np.sqrt(2.0 / (3.0 * N_axis))

ax3.plot(N_axis, rel_fluct_curve, color="#6a3d9a", lw=2.3, label=r"$\frac{\sqrt{\langle(\Delta E)^2\rangle}}{U} = \sqrt{\frac{2}{3N}} \propto \frac{1}{\sqrt{N}}$")
ax3.scatter([N_particles], [rel_fluctuation], color="#d62728", s=55, zorder=5,
            label=rf"Current $N = {N_particles}$ ($\sigma_E/U = {rel_fluctuation:.3f}$)")
ax3.axhline(0, color="#333333", lw=1.0)
ax3.set_xlabel(r"Number of Particles $N$")
ax3.set_ylabel(r"Relative RMS Fluctuation $\sigma_E / U$")
ax3.set_title(r"Thermodynamic Limit Scaling: $\sigma_E / U \propto 1/\sqrt{N}$")
ax3.legend(loc="upper right", fontsize=8.5, framealpha=0.95)

plt.tight_layout()
st.pyplot(fig)

with st.expander("Classroom Derivation Reference (Equations from Lecture Notes)", expanded=False):
    st.latex(r"\langle (\Delta E)^2 \rangle = \langle E^2 \rangle - \langle E \rangle^2 = kT^2 C_V \qquad (3.6.3)")
    st.latex(r"\frac{\sqrt{\langle (\Delta E)^2 \rangle}}{\langle E \rangle} = \frac{\sqrt{kT^2 C_V}}{U} \sim \frac{\sqrt{N}}{N} = \frac{1}{\sqrt{N}} \qquad (3.6.4\text{a},\; 3.6.4)")
    st.latex(r"P(E) \propto e^{-\beta E} g(E) = e^{-\beta(U - TS)} \exp\left(\frac{-(E - U)^2}{2kT^2 C_V}\right) \qquad (3.6.8)")
    st.latex(r"A = (U - TS) - \frac{1}{2}kT\ln(2\pi kT^2 C_V) \xrightarrow{N \to \infty} U - TS \qquad (3.6.9,\; 3.6.10)")

render_sidebar_footer()