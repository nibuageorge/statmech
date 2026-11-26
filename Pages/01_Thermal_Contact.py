import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from utils import apply_plot_style, render_sidebar_footer

st.set_page_config(
    page_title="01 — Thermal Contact",
    layout="wide"
)

apply_plot_style()

st.title("01. Thermal Contact & Sharpness of Composite Multiplicity $\\Omega^{(0)}(E^{(0)}, E_1)$")
st.markdown(
    "Based on **Chapter 1: Connection Between Thermodynamics and Statistics** "
    "(Eqs. 1.2.1–1.2.7 & Eq. 1.4.14)"
)

# --- Sidebar Controls ---
st.sidebar.header("Composite System Parameters")
N1 = st.sidebar.slider("Particles in Subsystem A₁ (N₁)", min_value=2, max_value=500, value=20, step=2)
N2 = st.sidebar.slider("Particles in Subsystem A₂ (N₂)", min_value=2, max_value=500, value=30, step=2)
E0 = st.sidebar.slider("Total Conserved Energy E⁽⁰⁾ (units of ε₀)", min_value=10.0, max_value=1000.0, value=100.0, step=10.0)

show_tangent = st.sidebar.checkbox("Show Equilibrium Intersection (β₁ = β₂)", value=True)
show_fwhm = st.sidebar.checkbox("Highlight Peak Width (FWHM)", value=True)

# --- Analytical Calculations from Lecture Notes ---
E1 = np.linspace(1e-4 * E0, (1.0 - 1e-4) * E0, 2000)
E2 = E0 - E1

# Multiplicities: ln(Omega_i) = (3*N_i / 2) * ln(E_i) (up to additive volume/mass constants)
f1 = 1.5 * N1
f2 = 1.5 * N2

ln_omega1 = f1 * np.log(E1)
ln_omega2 = f2 * np.log(E2)
ln_omega_total = ln_omega1 + ln_omega2

# Shift by max value to prevent floating-point overflow for large N
ln_omega_max = np.max(ln_omega_total)
omega_total_norm = np.exp(ln_omega_total - ln_omega_max)

# Equilibrium values (Eqs. 1.2.3 & 1.4.21)
E1_bar = (N1 / (N1 + N2)) * E0
E2_bar = E0 - E1_bar
beta_eq = f1 / E1_bar  # Equals f2 / E2_bar = 1 / (kT)
kT_eq = 1.0 / beta_eq

# Standard deviation and relative width of E1 around E1_bar
sigma_E1 = E0 * np.sqrt((f1 * f2) / ((f1 + f2) ** 3))
rel_width = sigma_E1 / E1_bar

# --- Key Metrics Row ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Equilibrium Energy Ē₁", f"{E1_bar:.2f} ε₀", f"{100*N1/(N1+N2):.1f}% of E⁽⁰⁾")
c2.metric("Equilibrium Energy Ē₂", f"{E2_bar:.2f} ε₀", f"{100*N2/(N1+N2):.1f}% of E⁽⁰⁾")
c3.metric("Common β = 1/(kT)", f"{beta_eq:.4f} ε₀⁻¹", f"kT = {kT_eq:.3f} ε₀")
c4.metric("Relative Peak Width (σ_E₁ / Ē₁)", f"{rel_width:.4f}", "Scales as 1/√N")

# --- Plotting ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4.6), dpi=150)

# Panel 1: ln Omega_1, ln Omega_2, and ln Omega^(0)
ax1.plot(E1, ln_omega1, color="#1f77b4", lw=2, label=r"$\ln \Omega_1(E_1)$")
ax1.plot(E1, ln_omega2, color="#d62728", lw=2, label=r"$\ln \Omega_2(E^{(0)}-E_1)$")
ax1.plot(E1, ln_omega_total, color="#2ca02c", lw=2.3, linestyle="--", label=r"$\ln \Omega^{(0)} = \ln\Omega_1 + \ln\Omega_2$")
ax1.axvline(E1_bar, color="#444444", linestyle=":", lw=1.3)
ax1.scatter([E1_bar], [f1 * np.log(E1_bar) + f2 * np.log(E2_bar)], color="#2ca02c", zorder=5)
ax1.set_title(r"Logarithmic Multiplicities $\ln \Omega$ vs. $E_1$")
ax1.set_xlabel(r"Subsystem Energy $E_1$ ($\varepsilon_0$)")
ax1.set_ylabel(r"$\ln \Omega$ (shifted constant)")
ax1.legend(loc="lower center", fontsize=9, framealpha=0.95)

# Panel 2: Inverse Temperature Parameters beta_1(E_1) and beta_2(E_1)
beta1_curve = f1 / E1
beta2_curve = f2 / E2
ax2.plot(E1, beta1_curve, color="#1f77b4", lw=2, label=r"$\beta_1 = \partial \ln\Omega_1 / \partial E_1$")
ax2.plot(E1, beta2_curve, color="#d62728", lw=2, label=r"$\beta_2 = \partial \ln\Omega_2 / \partial E_2$")
if show_tangent:
    ax2.axhline(beta_eq, color="#2ca02c", linestyle="--", lw=1.4, label=rf"Equilibrium $\beta_1 = \beta_2 = {beta_eq:.3f}$")
    ax2.axvline(E1_bar, color="#444444", linestyle=":", lw=1.3)
    ax2.scatter([E1_bar], [beta_eq], color="#2ca02c", s=45, zorder=5)
ax2.set_ylim(0, min(5.0 * beta_eq, np.max(beta1_curve[int(len(E1)*0.05):])))
ax2.set_title(r"Thermal Equilibrium Condition ($\beta_1 = \beta_2$)")
ax2.set_xlabel(r"Subsystem Energy $E_1$ ($\varepsilon_0$)")
ax2.set_ylabel(r"$\beta = 1/(kT)$ ($\varepsilon_0^{-1}$)")
ax2.legend(loc="upper right", fontsize=9, framealpha=0.95)

# Panel 3: Normalized Composite Multiplicity Omega^(0)(E_1)
ax3.plot(E1, omega_total_norm, color="#6a3d9a", lw=2.3, label=r"$\Omega^{(0)}(E_1) / \Omega^{(0)}_{\max}$")
ax3.fill_between(E1, 0, omega_total_norm, color="#6a3d9a", alpha=0.18)
ax3.axvline(E1_bar, color="#d62728", linestyle="--", lw=1.5, label=rf"Most Probable $\overline{{E}}_1 = {E1_bar:.1f}$")

if show_fwhm:
    above_half = np.where(omega_total_norm >= 0.5)[0]
    if len(above_half) > 1:
        e_left, e_right = E1[above_half[0]], E1[above_half[-1]]
        ax3.hlines(0.5, e_left, e_right, color="#111111", lw=1.6, linestyle="-.")
        ax3.text(E1_bar, 0.53, f"FWHM = {e_right - e_left:.2f}", ha="center", fontsize=9, color="#111111")

ax3.set_title(r"Composite Microstate Peak $\Omega^{(0)}(E^{(0)}, E_1)$")
ax3.set_xlabel(r"Subsystem Energy $E_1$ ($\varepsilon_0$)")
ax3.set_ylabel(r"Normalized Multiplicity $\Omega^{(0)} / \Omega^{(0)}_{\max}$")
ax3.set_ylim(0, 1.12)
ax3.legend(loc="upper right", fontsize=9, framealpha=0.95)

plt.tight_layout()
st.pyplot(fig)

with st.expander("Classroom Derivation Reference (Equations from Lecture Notes)", expanded=False):
    st.latex(r"E^{(0)} = E_1 + E_2 = \text{constant} \qquad (1.2.1)")
    st.latex(r"\Omega^{(0)}(E^{(0)}, E_1) = \Omega_1(E_1)\,\Omega_2(E^{(0)} - E_1) \qquad (1.2.2)")
    st.latex(r"\left(\frac{\partial \ln \Omega_1}{\partial E_1}\right)_{E_1=\overline{E}_1} = \left(\frac{\partial \ln \Omega_2}{\partial E_2}\right)_{E_2=\overline{E}_2} \implies \beta_1 = \beta_2 \implies T_1 = T_2 \qquad (1.2.3,\; 1.2.7)")

render_sidebar_footer()