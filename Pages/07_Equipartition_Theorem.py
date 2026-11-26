import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from utils import apply_plot_style, render_sidebar_footer

st.set_page_config(
    page_title="07 — The Equipartition Theorem",
    layout="wide"
)

apply_plot_style()

st.title("07. The Equipartition Theorem ($U = \\frac{1}{2} f kT$)")
st.markdown(
    "Based on **Chapter 3: The Equipartition Theorem** "
    "(Eqs. 3.7.1–3.7.9)"
)

# --- Sidebar Controls ---
st.sidebar.header("Quadratic Hamiltonian Parameters")
kT_val = st.sidebar.slider("Thermal Energy kT (units of ε₀)", min_value=0.5, max_value=5.0, value=2.0, step=0.1)
A1 = st.sidebar.slider("Momentum Coefficient A₁ = 1/(2m)", min_value=0.2, max_value=3.0, value=0.5, step=0.1)
B1 = st.sidebar.slider("Position Coefficient B₁ = k_spring / 2", min_value=0.2, max_value=3.0, value=1.8, step=0.1)
n_samples = st.sidebar.slider("Canonical Phase-Space Samples", min_value=500, max_value=10000, value=3000, step=500)
seed_val = st.sidebar.number_input("Random Seed", min_value=1, max_value=9999, value=42, step=1)

# --- Canonical Phase-Space Sampling (Eq. 3.5.3 & Eq. 3.7.7) ---
# For H = A1 * P^2 + B1 * Q^2, canonical density rho(Q, P) ~ exp(-beta * (A1*P^2 + B1*Q^2))
# This is an exact bivariate Gaussian with:
# sigma_P = sqrt(kT / (2 * A1)), sigma_Q = sqrt(kT / (2 * B1))
rng = np.random.default_rng(int(seed_val))
sigma_P = np.sqrt(kT_val / (2.0 * A1))
sigma_Q = np.sqrt(kT_val / (2.0 * B1))

P_samples = rng.normal(0.0, sigma_P, size=n_samples)
Q_samples = rng.normal(0.0, sigma_Q, size=n_samples)

E_kin_samples = A1 * (P_samples ** 2)   # A1 * P^2
E_pot_samples = B1 * (Q_samples ** 2)   # B1 * Q^2
H_samples = E_kin_samples + E_pot_samples

# Running ensemble averages
idx = np.arange(1, n_samples + 1)
running_kin = np.cumsum(E_kin_samples) / idx
running_pot = np.cumsum(E_pot_samples) / idx
running_tot = running_kin + running_pot

# Generalized Equipartition checks (Eqs. 3.7.2 - 3.7.4):
# <P * dH/dP> = <2 A1 P^2> = kT, <Q * dH/dQ> = <2 B1 Q^2> = kT, <P * dH/dQ> = 0
mean_P_dHdP = np.mean(P_samples * (2.0 * A1 * P_samples))
mean_Q_dHdQ = np.mean(Q_samples * (2.0 * B1 * Q_samples))
mean_cross_PQ = np.mean(P_samples * (2.0 * B1 * Q_samples))

# --- Key Metrics Row ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("⟨A₁ P²⟩ (Kinetic Term)", f"{running_kin[-1]:.4f} ε₀", f"Exact (1/2)kT = {0.5*kT_val:.4f}")
c2.metric("⟨B₁ Q²⟩ (Potential Term)", f"{running_pot[-1]:.4f} ε₀", f"Exact (1/2)kT = {0.5*kT_val:.4f}")
c3.metric("⟨P ∂H/∂P⟩ & ⟨Q ∂H/∂Q⟩", f"{mean_P_dHdP:.3f} & {mean_Q_dHdQ:.3f}", f"Exact δ_ii kT = {kT_val:.3f}")
c4.metric("Cross Term ⟨P ∂H/∂Q⟩", f"{mean_cross_PQ:+.4f}", "Exact δ_ij kT = 0 (i ≠ j)")

# --- Plotting ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.2, 4.7), dpi=150)

# Panel 1: Canonical Phase-Space Cloud (Q, P) Colored by H(Q, P) = A1*P^2 + B1*Q^2
sc = ax1.scatter(Q_samples[:1200], P_samples[:1200], c=H_samples[:1200], cmap="plasma", s=14, alpha=0.75)
cbar = plt.colorbar(sc, ax=ax1, fraction=0.046, pad=0.04)
cbar.set_label(r"Hamiltonian $H(Q,P)$")

# Overlay constant-energy contour H = kT (mean energy of 1D oscillator, f = 2)
theta = np.linspace(0, 2 * np.pi, 300)
q_ell = np.sqrt(kT_val / B1) * np.cos(theta)
p_ell = np.sqrt(kT_val / A1) * np.sin(theta)
ax1.plot(q_ell, p_ell, color="#111111", lw=1.8, linestyle="--", label=r"Mean Energy Contour $H = kT$")
ax1.set_xlabel(r"Generalized Coordinate $Q$")
ax1.set_ylabel(r"Generalized Momentum $P$")
ax1.set_title(rf"Canonical Phase Cloud ($A_1={A1:.1f}, B_1={B1:.1f}$)")
ax1.legend(loc="upper right", fontsize=8.5, framealpha=0.95)

# Panel 2: Running Ensemble Averages Converging to (1/2)kT and f*(1/2)kT
ax2.plot(idx, running_kin, color="#1f77b4", lw=2.0, label=rf"$\langle A_1 P^2 \rangle$ ($A_1 = {A1:.1f}$)")
ax2.plot(idx, running_pot, color="#2ca02c", lw=2.0, label=rf"$\langle B_1 Q^2 \rangle$ ($B_1 = {B1:.1f}$)")
ax2.plot(idx, running_tot, color="#9467bd", lw=2.2, label=r"Total $\langle H \rangle = U$ ($f = 2$)")

ax2.axhline(0.5 * kT_val, color="#d62728", linestyle="--", lw=1.6, label=rf"$\frac{{1}}{{2}}kT = {0.5*kT_val:.2f}$ per term")
ax2.axhline(kT_val, color="#111111", linestyle=":", lw=1.6, label=rf"$U = \frac{{1}}{{2}}(2)kT = {kT_val:.2f}$")

ax2.set_xlabel("Number of Canonical Samples")
ax2.set_ylabel(r"Running Ensemble Average ($\varepsilon_0$)")
ax2.set_title(r"Invariance to $A_1, B_1$: Each Term $\to \frac{1}{2}kT$")
ax2.legend(loc="right", fontsize=8.2, framealpha=0.95)

# Panel 3: Comparison of Systems Covered in Lecture Notes (U and C_V vs Temperature)
T_axis = np.linspace(0.1, 5.0, 200)
# 1D Harmonic Oscillator: f = 2 => U = kT, C_V = k
U_osc = 1.0 * T_axis
# Monatomic Ideal Gas (per particle): f = 3 => U/N = (3/2)kT, C_V/N = (3/2)k
U_gas = 1.5 * T_axis

ax3.plot(T_axis, U_osc, color="#1f77b4", lw=2.3,
         label=r"1D Harmonic Oscillator ($f = 2$): $U = kT,\; C_V = k$")
ax3.plot(T_axis, U_gas, color="#d62728", lw=2.3, linestyle="--",
         label=r"Monatomic Ideal Gas ($f = 3N$): $\frac{U}{N} = \frac{3}{2}kT,\; \frac{C_V}{N} = \frac{3}{2}k$")
ax3.scatter([kT_val, kT_val], [kT_val, 1.5 * kT_val], color="#111111", s=45, zorder=5)

ax3.set_xlabel(r"Thermal Energy $kT$ ($\varepsilon_0$)")
ax3.set_ylabel(r"Mean Energy per Entity ($\varepsilon_0$)")
ax3.set_title(r"Equipartition Scaling: $U = \frac{1}{2}fkT,\; C_V = \frac{1}{2}fk$")
ax3.legend(loc="upper left", fontsize=8.2, framealpha=0.95)

plt.tight_layout()
st.pyplot(fig)

with st.expander("Classroom Derivation Reference (Equations from Lecture Notes)", expanded=False):
    st.latex(r"\left\langle x_i \frac{\partial H}{\partial x_j} \right\rangle = \delta_{ij} kT \qquad (3.7.2)")
    st.latex(r"\left\langle p_i \frac{\partial H}{\partial p_i} \right\rangle = \langle p_i \dot{q}_i \rangle = kT, \qquad \left\langle q_i \frac{\partial H}{\partial q_i} \right\rangle = -\langle q_i \dot{p}_i \rangle = kT \qquad (3.7.3,\; 3.7.4)")
    st.latex(r"H = \sum_j A_j P_j^2 + \sum_j B_j Q_j^2 \implies \langle H \rangle = U = \frac{1}{2} f kT, \qquad C_V = \frac{1}{2} f k \qquad (3.7.7,\; 3.7.9)")

render_sidebar_footer()