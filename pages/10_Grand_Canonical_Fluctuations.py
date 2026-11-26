import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.special import gammaln
from utils import apply_plot_style, render_sidebar_footer

st.set_page_config(
    page_title="10 — Grand Canonical Fluctuations",
    layout="wide"
)

apply_plot_style()

st.title("10. Open-System Density & Energy Fluctuations (Grand Canonical Ensemble)")
st.markdown(
    "Based on **Chapter 4: Density Fluctuations in Grand Canonical Ensemble** & "
    "**Energy Fluctuations in Grand Canonical Ensemble** (Eqs. 4.5.3–4.5.14)"
)

# --- Sidebar Controls ---
st.sidebar.header("Open-System & Compressibility Parameters")
N_bar = st.sidebar.slider(
    "Mean Particle Number N̄ inside Open Volume V",
    min_value=10, max_value=1000, value=100, step=10
)
kT_val = st.sidebar.slider(
    "Thermal Energy kT (units of ε₀)",
    min_value=0.5, max_value=4.0, value=1.5, step=0.1
)
kappa_ratio = st.sidebar.slider(
    "Compressibility Ratio κ_T / κ_ideal (κ_ideal = v / kT)",
    min_value=0.2, max_value=50.0, value=1.0, step=0.2,
    help="κ_T / κ_ideal = 1 corresponds to a classical ideal gas; large values model critical opalescence."
)
dU_dN_factor = st.sidebar.slider(
    "Energy per Added Particle (∂U/∂N̄)_{T,V} / (kT)",
    min_value=0.5, max_value=4.0, value=1.5, step=0.1,
    help="Equals 3/2 for a monatomic classical ideal gas."
)

# --- Exact Formulas from Lecture Notes (Eqs. 4.5.3 - 4.5.14) ---
# Specific volume v = V / N_bar; for ideal gas kappa_ideal = v / (kT) => (kT / V) * kappa_T = kappa_ratio / N_bar
# Eq. (4.5.7): <ΔN^2> = N_bar^2 * (kT / V) * kappa_T = N_bar * kappa_ratio
var_N = N_bar * kappa_ratio
sigma_N = np.sqrt(var_N)
rel_fluct_N = sigma_N / N_bar          # Eq. (4.5.4): sqrt(kT * kappa_T / v) ~ 1 / sqrt(N_bar)

# Monatomic heat capacity C_V = (3/2) N_bar k
Cv_over_k = 1.5 * N_bar
# First term in Eq. (4.5.14): Canonical energy variance <(ΔE)^2>_canonical = k T^2 C_V
var_E_canonical = (kT_val ** 2) * Cv_over_k

# Second term in Eq. (4.5.14): [(∂U / ∂N̄)_{T,V}]^2 * <ΔN^2>
dU_dN = dU_dN_factor * kT_val
var_E_exchange = (dU_dN ** 2) * var_N

# Total open-system energy variance (Eq. 4.5.14)
var_E_total = var_E_canonical + var_E_exchange
sigma_E_total = np.sqrt(var_E_total)
U_mean = dU_dN * N_bar
rel_fluct_E = sigma_E_total / U_mean

exchange_share_pct = (var_E_exchange / var_E_total) * 100.0

# --- Key Metrics Row ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Particle Variance ⟨ΔN²⟩", f"{var_N:.1f}", f"σ_N / N̄ = {rel_fluct_N:.4f} (Eq. 4.5.4)")
c2.metric("Canonical Energy Variance", f"{var_E_canonical:.1f} ε₀²", "kT² C_V (Closed System)")
c3.metric("Particle-Exchange Variance", f"{var_E_exchange:.1f} ε₀²", f"{exchange_share_pct:.1f}% of Total ⟨ΔE²⟩")
c4.metric("Total Open Energy RMS σ_E", f"{sigma_E_total:.2f} ε₀", f"σ_E / U = {rel_fluct_E:.4f}")

# --- Plotting ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.2, 4.7), dpi=150)

# Panel 1: Grand Canonical Particle Distribution P(N) = (N̄^N e^{-N̄}) / N! (Ideal Gas Poisson Limit)
# For general kappa_ratio, show both exact ideal-gas Poisson P(N) and Gaussian envelope with variance N_bar * kappa_ratio
n_min = max(0, int(N_bar - 4.0 * max(sigma_N, np.sqrt(N_bar))))
n_max = int(N_bar + 4.0 * max(sigma_N, np.sqrt(N_bar)))
N_vals = np.arange(n_min, n_max + 1)

# Exact ideal gas distribution from Eq. (4.4.3): P(N) = (N_bar^N * exp(-N_bar)) / N!
ln_P_ideal = N_vals * np.log(N_bar) - N_bar - gammaln(N_vals + 1.0)
P_ideal = np.exp(ln_P_ideal)

# Effective distribution width for tunable compressibility kappa_T (Eq. 4.5.7)
P_eff = (1.0 / (np.sqrt(2.0 * np.pi) * sigma_N)) * np.exp(-((N_vals - N_bar) ** 2) / (2.0 * var_N))

ax1.plot(N_vals, P_ideal, color="#1f77b4", lw=2.0, linestyle="--",
         label=r"Ideal Gas ($\kappa_T = \kappa_{\mathrm{ideal}}$): $\overline{\Delta N^2} = \overline{N}$")
ax1.plot(N_vals, P_eff, color="#d62728", lw=2.3,
         label=rf"Current $\kappa_T / \kappa_{{\mathrm{{ideal}}}} = {kappa_ratio:.1f}$ ($\sigma_N = {sigma_N:.1f}$)")
ax1.fill_between(N_vals, 0, P_eff, color="#d62728", alpha=0.16)
ax1.axvline(N_bar, color="#111111", linestyle=":", lw=1.4, label=rf"Mean $\overline{{N}} = {N_bar}$")
ax1.set_xlabel(r"Instantaneous Particle Count $N$")
ax1.set_ylabel(r"Probability $P(N)$")
ax1.set_title(r"Open-System Particle Distribution $P(N)$ (Eq. 4.5.7)")
ax1.legend(loc="upper right", fontsize=8.0, framealpha=0.95)

# Panel 2: Decomposition of Open-System Energy Variance <ΔE^2> vs Compressibility Ratio (Eq. 4.5.14)
k_scan = np.linspace(0.2, 50.0, 250)
var_can_scan = np.full_like(k_scan, var_E_canonical)
var_exc_scan = (dU_dN ** 2) * (N_bar * k_scan)
var_tot_scan = var_can_scan + var_exc_scan

ax2.plot(k_scan, var_tot_scan / (kT_val ** 2 * N_bar), color="#111111", lw=2.4,
         label=r"Total $\overline{\Delta E^2} / (\overline{N}k^2T^2)$ (Eq. 4.5.14)")
ax2.plot(k_scan, var_can_scan / (kT_val ** 2 * N_bar), color="#1f77b4", lw=2.0, linestyle="--",
         label=r"Canonical Term: $kT^2 C_V$")
ax2.plot(k_scan, var_exc_scan / (kT_val ** 2 * N_bar), color="#ff7f0e", lw=2.0, linestyle="-.",
         label=r"Exchange Term: $\left(\frac{\partial U}{\partial \overline{N}}\right)^2 \overline{\Delta N^2}$")
ax2.scatter([kappa_ratio], [var_E_total / (kT_val ** 2 * N_bar)], color="#d62728", s=55, zorder=5)

ax2.set_xlabel(r"Isothermal Compressibility Ratio $\kappa_T / \kappa_{\mathrm{ideal}}$")
ax2.set_ylabel(r"Normalized Variance $\overline{\Delta E^2} / (\overline{N}k^2T^2)$")
ax2.set_title(r"Critical Opalescence Divergence ($\kappa_T \to \infty$)")
ax2.legend(loc="upper left", fontsize=8.0, framealpha=0.95)

# Panel 3: 1 / sqrt(N_bar) Scaling of Both Relative Fluctuations (Eq. 4.5.4)
N_axis = np.linspace(10, 1000, 300)
rel_N_curve = np.sqrt(kappa_ratio / N_axis)
rel_E_curve = np.sqrt((1.5 + (dU_dN_factor ** 2) * kappa_ratio) / ((dU_dN_factor ** 2) * N_axis))

ax3.plot(N_axis, rel_N_curve, color="#d62728", lw=2.2,
         label=r"Density Fluctuation $\frac{\sqrt{\overline{\Delta N^2}}}{\overline{N}} = \sqrt{\frac{kT\kappa_T}{v}} \propto \frac{1}{\sqrt{\overline{N}}}$")
ax3.plot(N_axis, rel_E_curve, color="#2ca02c", lw=2.2, linestyle="--",
         label=r"Energy Fluctuation $\frac{\sqrt{\overline{\Delta E^2}}}{\overline{E}} \propto \frac{1}{\sqrt{\overline{N}}}$")
ax3.scatter([N_bar, N_bar], [rel_fluct_N, rel_fluct_E], color="#111111", s=45, zorder=5)

ax3.set_xlabel(r"Mean Particle Number $\overline{N}$")
ax3.set_ylabel("Relative RMS Fluctuation")
ax3.set_title(r"Ensemble Equivalence in Thermodynamic Limit ($\overline{N} \to \infty$)")
ax3.legend(loc="upper right", fontsize=8.0, framealpha=0.95)

plt.tight_layout()
st.pyplot(fig)

with st.expander("Classroom Derivation Reference (Equations from Lecture Notes)", expanded=False):
    st.latex(r"\overline{\Delta N^2} = kT\left(\frac{\partial \overline{N}}{\partial \mu}\right)_{V,T} = \overline{N}^2 \frac{kT}{V}\kappa_T \implies \frac{\sqrt{\overline{\Delta N^2}}}{\overline{N}} = \sqrt{\frac{kT\kappa_T}{v}} \propto \frac{1}{\sqrt{V}} \propto \frac{1}{\sqrt{\overline{N}}} \qquad (4.5.3,\; 4.5.7,\; 4.5.4)")
    st.latex(r"\overline{\Delta E^2} = \langle (\Delta E)^2 \rangle_{\text{canonical}} + \left[\left(\frac{\partial U}{\partial \overline{N}}\right)_{T,V}\right]^2 \overline{\Delta N^2} = kT^2 C_V + \left[\left(\frac{\partial U}{\partial \overline{N}}\right)_{T,V}\right]^2 \overline{\Delta N^2} \qquad (4.5.11,\; 4.5.14)")

render_sidebar_footer()