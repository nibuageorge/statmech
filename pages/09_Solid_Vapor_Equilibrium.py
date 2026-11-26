import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.optimize import brentq
from utils import apply_plot_style, render_sidebar_footer

st.set_page_config(
    page_title="09 — Solid-Vapor Equilibrium",
    layout="wide"
)

apply_plot_style()

st.title("09. Solid–Vapor Equilibrium & Sublimation Phase Boundary")
st.markdown(
    "Based on **Chapter 4: Application to Solid-Vapor Equilibrium** "
    "(Eqs. 4.4.25–4.4.34)"
)

# --- Sidebar Controls (Dimensionless units scaled to Einstein temperature Theta_E = hbar*omega/k) ---
st.sidebar.header("Solid & Vapor Parameters")
eps_ratio = st.sidebar.slider(
    "Sublimation Binding Energy Ratio ε / (ħω)",
    min_value=2.0, max_value=15.0, value=6.0, step=0.5
)
mass_factor = st.sidebar.slider(
    "Dimensionless Quantum Mass Factor Λ₀ = (2π m ħω / h²)^(3/2) V₀",
    min_value=1.0, max_value=50.0, value=10.0, step=1.0
)
rho_total = st.sidebar.slider(
    "Total Particle Density N / V (in units of 1/V₀)",
    min_value=0.05, max_value=5.0, value=0.80, step=0.05
)
T_current = st.sidebar.slider(
    "Vessel Temperature kT / (ħω)",
    min_value=0.20, max_value=2.50, value=0.75, step=0.02
)

# --- Exact Functions from Lecture Notes (Eqs. 4.4.27 - 4.4.34) ---
# Let tau = kT / (hbar * omega)
def saturation_density(tau, eps_r, m_fac):
    # n_sat(T) = f(T) / phi_actual(T)
    # f(T) = m_fac * tau^(3/2)
    # phi_actual(T) = [2 * sinh(1 / (2*tau))]^(-3) * exp(eps_r / tau)
    u = 1.0 / tau
    # Use log-space for numerical stability at low temperatures
    ln_n_sat = (
        np.log(m_fac)
        + 1.5 * np.log(tau)
        + 3.0 * np.log(2.0 * np.sinh(0.5 * u))
        - eps_r * u
    )
    return np.exp(ln_n_sat)

def vapor_pressure(tau, eps_r, m_fac):
    # Eq. (4.4.28) & (4.4.31): P_vapor = kT * n_sat(T)
    return tau * saturation_density(tau, eps_r, m_fac)

# Solve Eq. (4.4.34) for Critical Temperature T_c: n_sat(T_c) = N / V
tau_low_bound = 0.05
tau_high_bound = 10.0
try:
    if saturation_density(tau_low_bound, eps_ratio, mass_factor) >= rho_total:
        tau_c = tau_low_bound
    elif saturation_density(tau_high_bound, eps_ratio, mass_factor) <= rho_total:
        tau_c = None
    else:
        tau_c = brentq(
            lambda t: saturation_density(t, eps_ratio, mass_factor) - rho_total,
            tau_low_bound,
            tau_high_bound
        )
except ValueError:
    tau_c = None

# Evaluate current state at T_current
n_sat_curr = saturation_density(T_current, eps_ratio, mass_factor)
if n_sat_curr >= rho_total:
    # Unsaturated vapor regime (T >= T_c): all particles are in vapor phase (Eq. 4.4.32)
    frac_vapor = 1.0
    frac_solid = 0.0
    P_actual = rho_total * T_current  # Ideal gas law P = (N/V) kT
    regime_label = "Pure Vapor Phase (T ≥ T_c)"
else:
    # Two-phase coexistence (T < T_c): vapor saturates at n_sat, excess forms solid
    frac_vapor = n_sat_curr / rho_total
    frac_solid = 1.0 - frac_vapor
    P_actual = vapor_pressure(T_current, eps_ratio, mass_factor)
    regime_label = "Solid–Vapor Coexistence (T < T_c)"

# --- Key Metrics Row ---
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Critical Temp kT_c / (ħω)",
    f"{tau_c:.3f}" if tau_c is not None else "> 10.0",
    regime_label
)
c2.metric("Vapor Fraction N_g / N", f"{frac_vapor*100:.1f}%", f"n_g = {frac_vapor*rho_total:.3f}")
c3.metric("Solid Fraction N_s / N", f"{frac_solid*100:.1f}%", f"n_s = {frac_solid*rho_total:.3f}")
c4.metric("Vessel Pressure P", f"{P_actual:.4f}", "Saturated P_vapor" if frac_solid > 0 else "Unsaturated Ideal Gas")

# --- Plotting ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.2, 4.7), dpi=150)

tau_grid = np.linspace(0.20, 2.50, 400)
n_sat_grid = saturation_density(tau_grid, eps_ratio, mass_factor)
P_vap_grid = vapor_pressure(tau_grid, eps_ratio, mass_factor)

# Actual vessel pressure across temperature: min(P_vapor(T), (N/V)*kT)
P_vessel_grid = np.minimum(P_vap_grid, rho_total * tau_grid)

# Panel 1: Equilibrium Vapor Pressure Curve P_vapor(T) vs Vessel Pressure (Eq. 4.4.31)
ax1.plot(tau_grid, P_vap_grid, color="#1f77b4", lw=2.3, label=r"Coexistence $P_{\mathrm{vapor}}(T)$ (Eq. 4.4.31)")
ax1.plot(tau_grid, P_vessel_grid, color="#d62728", lw=2.0, linestyle="--", label=r"Actual Vessel Pressure $P(T)$")
if tau_c is not None and 0.20 <= tau_c <= 2.50:
    ax1.axvline(tau_c, color="#2ca02c", linestyle=":", lw=1.6, label=rf"Critical $T_c$ ($kT_c/\hbar\omega = {tau_c:.2f}$)")
ax1.scatter([T_current], [P_actual], color="#111111", s=50, zorder=5)
ax1.set_ylim(0, max(2.5 * rho_total, P_actual * 1.4))
ax1.set_xlabel(r"Reduced Temperature $kT / (\hbar\omega)$")
ax1.set_ylabel(r"Pressure $P$")
ax1.set_title(r"Solid–Vapor Coexistence Curve $P_{\mathrm{vapor}}(T)$")
ax1.legend(loc="upper left", fontsize=8.2, framealpha=0.95)

# Panel 2: Phase Population Split N_g / N and N_s / N Across Temperature (Eq. 4.4.34)
fg_curve = np.minimum(1.0, n_sat_grid / rho_total)
fs_curve = 1.0 - fg_curve

ax2.plot(tau_grid, fg_curve * 100.0, color="#1f77b4", lw=2.3, label=r"Vapor Phase $N_g / N$ (%)")
ax2.plot(tau_grid, fs_curve * 100.0, color="#ff7f0e", lw=2.3, linestyle="--", label=r"Solid Phase $N_s / N$ (%)")
ax2.fill_between(tau_grid, 0, fs_curve * 100.0, color="#ff7f0e", alpha=0.16)
if tau_c is not None and 0.20 <= tau_c <= 2.50:
    ax2.axvline(tau_c, color="#2ca02c", linestyle=":", lw=1.6, label=rf"Condensation Onset $T_c = {tau_c:.2f}$")
ax2.axvline(T_current, color="#444444", linestyle="-.", lw=1.2)
ax2.set_ylim(-3, 108)
ax2.set_xlabel(r"Reduced Temperature $kT / (\hbar\omega)$")
ax2.set_ylabel("Particle Fraction (%)")
ax2.set_title(r"Vapor Saturation & Solid Formation ($T < T_c$)")
ax2.legend(loc="center right", fontsize=8.2, framealpha=0.95)

# Panel 3: Clausius-Clapeyron Arrhenius View: ln(P_vapor) vs (hbar*omega)/(kT)
inv_tau = 1.0 / tau_grid
ax3.plot(inv_tau, np.log(P_vap_grid), color="#6a3d9a", lw=2.3,
         label=r"$\ln P_{\mathrm{vapor}}$ vs. $\frac{\hbar\omega}{kT}$ (Slope $\approx -\epsilon/\hbar\omega$)")
ax3.scatter([1.0 / T_current], [np.log(vapor_pressure(T_current, eps_ratio, mass_factor))],
            color="#d62728", s=50, zorder=5, label=rf"Current $T$ ($\ln P_{{vap}} = {np.log(vapor_pressure(T_current, eps_ratio, mass_factor)):.2f}$)")
ax3.set_xlabel(r"Inverse Reduced Temperature $\hbar\omega / (kT)$")
ax3.set_ylabel(r"$\ln P_{\mathrm{vapor}}$")
ax3.set_title(r"Sublimation Exponential Factor $e^{-\epsilon/kT}$")
ax3.legend(loc="upper right", fontsize=8.2, framealpha=0.95)

plt.tight_layout()
st.pyplot(fig)

with st.expander("Classroom Derivation Reference (Equations from Lecture Notes)", expanded=False):
    st.latex(r"z_g = z_s \implies \frac{N_g}{V_g f(T)} = \frac{1}{\phi_{\text{actual}}(T)} \implies P_{\text{vapor}} = kT\frac{f(T)}{\phi_{\text{actual}}(T)} \qquad (4.4.25\text{–}4.4.28)")
    st.latex(r"P_{\text{vapor}} = kT\left(\frac{2\pi mkT}{h^2}\right)^{3/2}\left[2\sinh\left(\frac{\hbar\omega}{2kT}\right)\right]^3 e^{-\epsilon/kT} \qquad (4.4.31)")
    st.latex(r"\frac{f(T_c)}{\phi_{\text{actual}}(T_c)} = \frac{N}{V}, \qquad N_s = N - N_g \quad (T < T_c) \qquad (4.4.34)")

render_sidebar_footer()