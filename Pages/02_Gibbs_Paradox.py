import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.special import gammaln
from utils import apply_plot_style, render_sidebar_footer

st.set_page_config(
    page_title="02 — Gibbs Paradox & 1/N! Correction",
    layout="wide"
)

apply_plot_style()

st.title("02. Entropy of Mixing, Gibbs Paradox & the $1/N!$ Correction")
st.markdown(
    "Based on **Chapter 1: The Entropy of Mixing and Gibbs Paradox** & "
    "**The \"Correct\" Enumeration of Microstates** (Eqs. 1.5.1–1.5.6)"
)

# --- Sidebar Controls ---
st.sidebar.header("Two-Compartment Box Setup")
gas_mode = st.sidebar.radio(
    "Gas Identity in Compartments 1 & 2",
    options=["Identical Gases (m₁ = m₂)", "Dissimilar Gases (m₁ ≠ m₂)"]
)

counting_mode = st.sidebar.radio(
    "Microstate Enumeration Method",
    options=[
        "Uncorrected Classical (Eq. 1.5.1 — Distinguishable)",
        "Gibbs Corrected 1/N! (Eq. 1.5.6 — Sackur-Tetrode)"
    ]
)

N1 = st.sidebar.slider("Molecules in Compartment 1 (N₁)", min_value=10, max_value=500, value=100, step=10)
N2 = st.sidebar.slider("Molecules in Compartment 2 (N₂)", min_value=10, max_value=500, value=100, step=10)
V1 = st.sidebar.slider("Volume of Compartment 1 (V₁, dimensionless units)", min_value=10.0, max_value=500.0, value=100.0, step=10.0)
V2 = st.sidebar.slider("Volume of Compartment 2 (V₂, dimensionless units)", min_value=10.0, max_value=500.0, value=100.0, step=10.0)
T_dim = st.sidebar.slider("Dimensionless Temperature (kT / ε₀)", min_value=0.5, max_value=10.0, value=2.5, step=0.1)

# Dimensionless masses (in units where h^2 / (2*pi*m0*eps0*l0^2) = 1)
m1 = 1.0
m2 = 1.0 if gas_mode.startswith("Identical") else 4.0

# --- Entropy Calculations (in units of Boltzmann constant k) ---
def entropy_uncorrected(N, V, m, kT):
    # Eq. (1.5.1) in units of k: N*ln(V) + (3/2)*N*ln(m*kT) + (3/2)*N
    return N * np.log(V) + 1.5 * N * np.log(m * kT) + 1.5 * N

def entropy_sackur_tetrode(N, V, m, kT):
    # Eq. (1.5.6) using exact ln(N!) via gammaln(N+1) so both small and large N are exact
    return entropy_uncorrected(N, V, m, kT) - gammaln(N + 1)

V_total = V1 + V2
N_total = N1 + N2
use_gibbs = counting_mode.startswith("Gibbs Corrected")

if not use_gibbs:
    S1_init = entropy_uncorrected(N1, V1, m1, T_dim)
    S2_init = entropy_uncorrected(N2, V2, m2, T_dim)
    S_init_sum = S1_init + S2_init
    # Final state: each gas expands to V1 + V2
    S_final = entropy_uncorrected(N1, V_total, m1, T_dim) + entropy_uncorrected(N2, V_total, m2, T_dim)
else:
    S1_init = entropy_sackur_tetrode(N1, V1, m1, T_dim)
    S2_init = entropy_sackur_tetrode(N2, V2, m2, T_dim)
    S_init_sum = S1_init + S2_init
    if gas_mode.startswith("Identical"):
        # Identical particles become a single indistinguishable assembly of N1 + N2 in V1 + V2
        S_final = entropy_sackur_tetrode(N_total, V_total, m1, T_dim)
    else:
        # Dissimilar gases remain mutually distinguishable: divide by N1! and N2! separately
        S_final = entropy_sackur_tetrode(N1, V_total, m1, T_dim) + entropy_sackur_tetrode(N2, V_total, m2, T_dim)

delta_S = S_final - S_init_sum

# Classical validity parameter <n_i> ~ (N/V) * lambda_th^3
occ_1 = (N1 / V1) * ((m1 * T_dim) ** (-1.5))
occ_2 = (N2 / V2) * ((m2 * T_dim) ** (-1.5))
max_occ = max(occ_1, occ_2)

# --- Key Metrics Row ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Initial Entropy (S₁ + S₂) / k", f"{S_init_sum:.2f}")
c2.metric("Final Mixed Entropy S_T / k", f"{S_final:.2f}")
c3.metric(
    "Entropy of Mixing ΔS / k",
    f"{delta_S:.3f}",
    "Paradoxical ΔS > 0!" if (gas_mode.startswith("Identical") and not use_gibbs and abs(delta_S) > 1e-6) else "Physically Consistent"
)
c4.metric(
    "Max State Occupancy ⟨nᵢ⟩",
    f"{max_occ:.4f}",
    "Classical Limit Valid (⟨nᵢ⟩ ≪ 1)" if max_occ < 0.2 else "Quantum Regime Approaching"
)

# --- Plotting ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4.6), dpi=150)

# Panel 1: Compartment Schematic (Before vs After Partition Removal)
rng = np.random.default_rng(42)
x1_before = rng.uniform(0.05, 0.46, min(N1, 150))
y1_before = rng.uniform(0.56, 0.94, min(N1, 150))
x2_before = rng.uniform(0.54, 0.95, min(N2, 150))
y2_before = rng.uniform(0.56, 0.94, min(N2, 150))

x1_after = rng.uniform(0.05, 0.95, min(N1, 150))
y1_after = rng.uniform(0.05, 0.43, min(N1, 150))
x2_after = rng.uniform(0.05, 0.95, min(N2, 150))
y2_after = rng.uniform(0.05, 0.43, min(N2, 150))

color2 = "#1f77b4" if gas_mode.startswith("Identical") else "#d62728"
label2 = "Gas 1 (Identical)" if gas_mode.startswith("Identical") else "Gas 2 (Distinct)"

# Top box: Partition present
ax1.add_patch(plt.Rectangle((0.02, 0.54), 0.96, 0.42, fill=False, edgecolor="#222222", lw=1.8))
ax1.plot([0.5, 0.5], [0.54, 0.96], color="#111111", lw=2.5, label="Removable Partition")
ax1.scatter(x1_before, y1_before, s=16, color="#1f77b4", alpha=0.8, label="Gas 1")
ax1.scatter(x2_before, y2_before, s=16, color=color2, alpha=0.8, label=label2)
ax1.text(0.26, 0.97, f"Before: S₁+S₂ = {S_init_sum:.1f}k", ha="center", fontsize=9.5, fontweight="bold")

# Bottom box: Partition removed
ax1.add_patch(plt.Rectangle((0.02, 0.03), 0.96, 0.42, fill=False, edgecolor="#222222", lw=1.8))
ax1.scatter(x1_after, y1_after, s=16, color="#1f77b4", alpha=0.8)
ax1.scatter(x2_after, y2_after, s=16, color=color2, alpha=0.8)
ax1.text(0.50, 0.46, f"After Removal: S_T = {S_final:.1f}k  (ΔS = {delta_S:.2f}k)", ha="center", fontsize=9.5, fontweight="bold")

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1.04)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.grid(False)
ax1.set_title("Gibbs Mixing Experiment")
ax1.legend(loc="lower right", fontsize=8, framealpha=0.92)

# Panel 2: Extensivity Test S(αN, αV, T) vs α S(N, V, T)
alpha_vals = np.linspace(0.2, 3.0, 100)
S_base_uncorr = entropy_uncorrected(N1, V1, m1, T_dim)
S_base_corr = entropy_sackur_tetrode(N1, V1, m1, T_dim)

S_scaled_uncorr = np.array([entropy_uncorrected(a * N1, a * V1, m1, T_dim) for a in alpha_vals])
S_scaled_corr = np.array([entropy_sackur_tetrode(a * N1, a * V1, m1, T_dim) for a in alpha_vals])

ax2.plot(alpha_vals, alpha_vals * S_base_corr, color="#111111", linestyle="--", lw=1.8, label=r"True Extensive: $\alpha S(N,V,T)$")
ax2.plot(alpha_vals, S_scaled_corr, color="#2ca02c", lw=2.2, label=r"With $1/N!$: $S(\alpha N, \alpha V, T)$")
ax2.plot(alpha_vals, S_scaled_uncorr - (S_base_uncorr - S_base_corr) * alpha_vals, color="#d62728", lw=2,
         label=r"Without $1/N!$: $+\alpha N k \ln\alpha$ Error")
ax2.set_title(r"Extensivity Check: Scaling $(N,V) \to (\alpha N, \alpha V)$")
ax2.set_xlabel(r"Scaling Factor $\alpha$")
ax2.set_ylabel(r"Entropy $S / k$")
ax2.legend(loc="upper left", fontsize=8.5, framealpha=0.95)

# Panel 3: ΔS vs Volume Fraction x = V1 / (V1 + V2) at Equal Densities (N1/V1 = N2/V2)
x_frac = np.linspace(0.02, 0.98, 200)
N_tot_demo = N1 + N2
V_tot_demo = V1 + V2
N1_x = x_frac * N_tot_demo
N2_x = (1.0 - x_frac) * N_tot_demo
V1_x = x_frac * V_tot_demo
V2_x = (1.0 - x_frac) * V_tot_demo

# Eq. (1.5.3): Mixing entropy for dissimilar gases (or uncorrected identical gases)
dS_mixing_curve = N1_x * np.log(V_tot_demo / V1_x) + N2_x * np.log(V_tot_demo / V2_x)
dS_identical_corrected = np.zeros_like(x_frac)

ax3.plot(x_frac, dS_mixing_curve, color="#d62728", lw=2.2,
         label=r"Dissimilar (or Uncorrected): Eq. (1.5.3)")
ax3.plot(x_frac, dS_identical_corrected, color="#2ca02c", lw=2.4, linestyle="--",
         label=r"Identical + $1/N!$: $\Delta S^* = 0$")

current_x = V1 / V_total
ax3.scatter([current_x], [delta_S], color="#6a3d9a", s=55, zorder=5, label=f"Current Setup (ΔS/k = {delta_S:.2f})")
ax3.set_title(r"Mixing Entropy $\Delta S / k$ vs. Volume Ratio $V_1/V$")
ax3.set_xlabel(r"Initial Volume Fraction $V_1 / (V_1 + V_2)$")
ax3.set_ylabel(r"$\Delta S / k$")
ax3.legend(loc="upper right", fontsize=8.5, framealpha=0.95)

plt.tight_layout()
st.pyplot(fig)

with st.expander("Classroom Derivation Reference (Equations from Lecture Notes)", expanded=False):
    st.latex(r"\Delta S = k \left[ N_1 \ln\left(\frac{V_1 + V_2}{V_1}\right) + N_2 \ln\left(\frac{V_1 + V_2}{V_2}\right) \right] \qquad (1.5.3)")
    st.latex(r"\Gamma_{\text{new}} = \frac{\Gamma_{\text{old}}}{N!} \implies S_{\text{new}} = S_{\text{old}} - k\ln(N!) \qquad (1.5.4\text{b},\; 1.5.4\text{c})")
    st.latex(r"S(N,V,T) = Nk\ln\left(\frac{V}{N}\right) + \frac{3}{2}Nk\left[\frac{5}{3} + \ln\left(\frac{2\pi mkT}{h^2}\right)\right] \qquad (1.5.6)")

render_sidebar_footer()