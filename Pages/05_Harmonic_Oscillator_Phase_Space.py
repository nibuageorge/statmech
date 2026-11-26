import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from utils import apply_plot_style, render_sidebar_footer

st.set_page_config(
    page_title="05 — 1D Harmonic Oscillator & Planck Cells",
    layout="wide"
)

apply_plot_style()

st.title("05. 1D Harmonic Oscillator Phase Space & Planck Quantum Cells ($\\omega_0 = h$)")
st.markdown(
    "Based on **Chapter 2: Phase Space of a 1D Harmonic Oscillator** & "
    "**Quantum States and the Phase Space** (Eqs. 2.3.18–2.3.21)"
)

# --- Sidebar Controls ---
st.sidebar.header("Oscillator & Quantization Parameters")
omega = st.sidebar.slider("Angular Frequency ω (natural units, ħ = 1)", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
mass = st.sidebar.slider("Oscillator Mass m (natural units)", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
n_max_plot = st.sidebar.slider("Maximum Quantum Level n Shown", min_value=3, max_value=8, value=4, step=1)
selected_n = st.sidebar.slider("Highlight Annular Cell Between n and n+1", min_value=0, max_value=n_max_plot - 1, value=1, step=1)

st.sidebar.markdown("---")
st.sidebar.header("Classical-to-Quantum State Counting")
E_classical = st.sidebar.slider("Classical Upper Energy Bound E (units of ħω₀)", min_value=1.0, max_value=10.0, value=4.5, step=0.5)

# Working in natural units where h_bar = 1 => h = 2 * pi
hbar = 1.0
h_planck = 2.0 * np.pi

def energy_n(n, w):
    return (n + 0.5) * hbar * w

def semi_axes(E, m, w):
    a = np.sqrt(2.0 * E / (m * (w ** 2)))  # position semi-axis
    b = np.sqrt(2.0 * m * E)              # momentum semi-axis
    return a, b

# Ground-state reference semi-axes (q0, p0 at n=0) matching page 28 notation
q0_ref, p0_ref = semi_axes(energy_n(0, omega), mass, omega)

# Annular shell area between selected_n and selected_n + 1 (Eq. 2.3.19 & 2.3.21)
E_low = energy_n(selected_n, omega)
E_high = energy_n(selected_n + 1, omega)
area_low = 2.0 * np.pi * E_low / omega
area_high = 2.0 * np.pi * E_high / omega
annular_area = area_high - area_low  # Always equals 2*pi*hbar = h

# Classical total area up to E_classical and discrete state count Gamma = omega / h
total_classical_area = 2.0 * np.pi * E_classical / omega
gamma_states = total_classical_area / h_planck  # Equals E_classical / (hbar * omega)

# --- Key Metrics Row ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Level Spacing Δ = E_{n+1} − E_n", f"{hbar * omega:.2f} (ħω)", f"n = {selected_n} → {selected_n + 1}")
c2.metric("Annular Phase Area ω₀", f"{annular_area:.4f} (2πħ)", "Invariant: ω₀ = h (Eq. 2.3.21)")
c3.metric("Semi-Axes (a₀, b₀) at n = 0", f"({q0_ref:.2f}, {p0_ref:.2f})", "Scales as √(2n + 1)")
c4.metric("Quantum States Γ = ω / h", f"{gamma_states:.2f}", f"Up to E = {E_classical:.1f}")

# --- Plotting ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.2, 4.7), dpi=150)

# Panel 1: Concentric Quantized Phase-Space Ellipses (Matching Page 28 Diagram)
theta = np.linspace(0, 2.0 * np.pi, 400)
palette = ["#1f77b4", "#2ca02c", "#d62728", "#9467bd", "#ff7f0e", "#17becf", "#8c564b", "#e377c2", "#7f7f7f"]

for n in range(n_max_plot + 1):
    En = energy_n(n, omega)
    a_n, b_n = semi_axes(En, mass, omega)
    qn = a_n * np.cos(theta)
    pn = b_n * np.sin(theta)
    ax1.plot(qn, pn, color=palette[n % len(palette)], lw=2.0, label=rf"$n={n}$ ($E_{n}={n+0.5:.1f}\hbar\omega$)")

# Shade the annular cell between selected_n and selected_n + 1
a_in, b_in = semi_axes(E_low, mass, omega)
a_out, b_out = semi_axes(E_high, mass, omega)
q_outer = a_out * np.cos(theta)
p_outer = b_out * np.sin(theta)
q_inner = a_in * np.cos(theta[::-1])
p_inner = b_in * np.sin(theta[::-1])

ax1.fill(
    np.concatenate([q_outer, q_inner]),
    np.concatenate([p_outer, p_inner]),
    color="#fde047",
    alpha=0.45,
    label=rf"Cell $\omega_0 = h$ ($n={selected_n}\to{selected_n+1}$)"
)

# Axes crosshairs through origin
max_a, max_b = semi_axes(energy_n(n_max_plot, omega), mass, omega)
lim_q = max(3.5, max_a * 1.18)
lim_p = max(3.5, max_b * 1.18)
ax1.axhline(0, color="#333333", lw=1.0)
ax1.axvline(0, color="#333333", lw=1.0)
ax1.set_xlim(-lim_q, lim_q)
ax1.set_ylim(-lim_p, lim_p)
ax1.set_xlabel(r"Position $q$")
ax1.set_ylabel(r"Momentum $p$")
ax1.set_title("Quantized Phase-Space Ellipses (Eq. 2.3.18)")
ax1.legend(loc="upper right", fontsize=7.8, framealpha=0.95)

# Panel 2: Cumulative Phase-Space Area vs Energy (Classical Straight Line vs Quantum Steps)
E_axis = np.linspace(0, energy_n(n_max_plot, omega) * 1.05, 300)
area_classical_curve = 2.0 * np.pi * E_axis / omega  # Eq. (2.3.18b): Area = 2*pi*E / omega

n_levels = np.arange(0, n_max_plot + 1)
E_levels = energy_n(n_levels, omega)
area_levels = 2.0 * np.pi * E_levels / omega  # Equals (n + 1/2) * h

ax2.plot(E_axis, area_classical_curve / h_planck, color="#1f77b4", lw=2.2,
         label=r"Classical $\omega(E)/h = E/(\hbar\omega)$")
ax2.scatter(E_levels, area_levels / h_planck, color="#d62728", s=50, zorder=5,
            label=r"Quantum States $E_n = (n + \frac{1}{2})\hbar\omega$")

# Highlight step delta E = hbar*omega and delta Area = h
ax2.plot([E_low, E_high], [area_low / h_planck, area_low / h_planck], color="#111111", linestyle="--", lw=1.4)
ax2.plot([E_high, E_high], [area_low / h_planck, area_high / h_planck], color="#111111", linestyle="--", lw=1.4)
ax2.text(E_high + 0.08 * max(E_axis), 0.5 * (area_low + area_high) / h_planck, r"$\Delta\omega = h$",
         va="center", fontsize=9.5, fontweight="bold")

ax2.set_xlabel(r"Total Energy $E$")
ax2.set_ylabel(r"Enclosed Phase Area in Units of $h$ ($\omega / h$)")
ax2.set_title(r"Phase Area Quantization: $\omega_0 = \frac{2\pi\Delta}{\omega} = h$")
ax2.legend(loc="upper left", fontsize=8.5, framealpha=0.95)

# Panel 3: Quantum Cell Volume Scaling omega_0 = h^f Across Systems (Page 29 Table)
systems = [
    "1 Particle\nin 1D\n(f = 1)",
    "1 Particle\nin 3D\n(f = 3)",
    "N = 4 1D\nOscillators\n(f = 4)",
    "N = 2 3D Gas\nParticles\n(f = 6)"
]
exponents = [1, 3, 4, 6]
colors_bar = ["#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd"]

bars = ax3.bar(systems, exponents, color=colors_bar, width=0.52, edgecolor="#222222")
for bar, exp in zip(bars, exponents):
    label_txt = r"$h$" if exp == 1 else rf"$h^{exp}$"
    ax3.text(bar.get_x() + bar.get_width() / 2.0, exp + 0.2, label_txt,
             ha="center", va="bottom", fontsize=11, fontweight="bold")

ax3.set_ylim(0, 7.2)
ax3.set_ylabel(r"Exponent $f$ in Quantum Cell $\omega_0 = h^f$")
ax3.set_title(r"Fundamental Quantum Cell Size $\omega_0 = h^f$ (Page 29)")

plt.tight_layout()
st.pyplot(fig)

with st.expander("Classroom Derivation Reference (Equations from Lecture Notes)", expanded=False):
    st.latex(r"\frac{q^2}{2E / m\omega^2} + \frac{p^2}{2mE} = 1 \implies \text{Area}(E) = \pi a b = \frac{2\pi E}{\omega} \qquad (2.3.18,\; 2.3.18\text{b})")
    st.latex(r"E_n = \left(n + \frac{1}{2}\right)\hbar\omega, \qquad \Delta = E_{n+1} - E_n = \hbar\omega \implies \omega_0 = \frac{2\pi}{\omega}(\hbar\omega) = h \qquad (2.3.20,\; 2.3.21)")
    st.latex(r"\Gamma = \frac{\text{Total classical phase volume } (\omega)}{\text{Size of one quantum cell } (\omega_0 = h^f)} \qquad (\text{Page 29})")

render_sidebar_footer()