import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from utils import apply_plot_style, render_sidebar_footer

st.set_page_config(
    page_title="04 — Liouville's Theorem & Phase Fluid",
    layout="wide"
)

apply_plot_style()

st.title("04. Liouville's Theorem: Incompressible Phase Fluid Flow")
st.markdown(
    "Based on **Chapter 2: Phase Space of a Classical System** & "
    "**Liouville's Theorem and the Equation of Continuity** (Eqs. 2.1.1–2.2.17)"
)

# --- Sidebar Controls ---
st.sidebar.header("1D Harmonic Oscillator Parameters")
mass = st.sidebar.slider("Particle Mass m", min_value=0.5, max_value=4.0, value=1.0, step=0.1)
k_spring = st.sidebar.slider("Spring Constant k", min_value=0.5, max_value=4.0, value=1.5, step=0.1)
omega = np.sqrt(k_spring / mass)

st.sidebar.markdown("---")
st.sidebar.header("Ensemble Patch & Time Evolution")
t_val = st.sidebar.slider("Evolution Time t (units of 1/ω₀)", min_value=0.0, max_value=6.28, value=1.20, step=0.05)
q0_center = st.sidebar.slider("Initial Patch Center q₀", min_value=0.5, max_value=3.0, value=1.8, step=0.1)
p0_center = st.sidebar.slider("Initial Patch Center p₀", min_value=-2.0, max_value=2.0, value=0.6, step=0.1)
dq_init = st.sidebar.slider("Initial Width Δq₀", min_value=0.2, max_value=1.2, value=0.6, step=0.05)
dp_init = st.sidebar.slider("Initial Height Δp₀", min_value=0.2, max_value=1.2, value=0.6, step=0.05)

ensemble_type = st.sidebar.radio(
    "Stationary Ensemble Overlay ([ρ, H] = 0)",
    options=[
        "Approach 1: Microcanonical Shell (ρ = const)",
        "Approach 2: Canonical Distribution (ρ ∝ exp(-H/kT))"
    ]
)

# --- Exact Hamiltonian Evolution (Eqs. 2.3.16a & 2.3.16b) ---
# For H = (1/2)kq^2 + p^2/(2m), exact symplectic evolution over time t:
# q(t) = q(0) cos(wt) + (p(0)/(m*w)) sin(wt)
# p(t) = -m*w*q(0) sin(wt) + p(0) cos(wt)
def evolve_phase_points(q_in, p_in, t, m, w):
    c = np.cos(w * t)
    s = np.sin(w * t)
    q_out = q_in * c + (p_in / (m * w)) * s
    p_out = -m * w * q_in * s + p_in * c
    return q_out, p_out

# Create a 20x20 grid of N_ens = 400 representative points inside [q0 - dq/2, q0 + dq/2] x [p0 - dp/2, p0 + dp/2]
n_side = 20
q_lin = np.linspace(q0_center - 0.5 * dq_init, q0_center + 0.5 * dq_init, n_side)
p_lin = np.linspace(p0_center - 0.5 * dp_init, p0_center + 0.5 * dp_init, n_side)
Q0, P0 = np.meshgrid(q_lin, p_lin)
q0_pts = Q0.ravel()
p0_pts = P0.ravel()
N_ens = len(q0_pts)

# Boundary loop of the initial patch (for exact polygon area via Shoelace formula)
n_edge = 80
top_q = np.linspace(q0_center - 0.5 * dq_init, q0_center + 0.5 * dq_init, n_edge)
top_p = np.full(n_edge, p0_center + 0.5 * dp_init)
right_q = np.full(n_edge, q0_center + 0.5 * dq_init)
right_p = np.linspace(p0_center + 0.5 * dp_init, p0_center - 0.5 * dp_init, n_edge)
bot_q = np.linspace(q0_center + 0.5 * dq_init, q0_center - 0.5 * dq_init, n_edge)
bot_p = np.full(n_edge, p0_center - 0.5 * dp_init)
left_q = np.full(n_edge, q0_center - 0.5 * dq_init)
left_p = np.linspace(p0_center - 0.5 * dp_init, p0_center + 0.5 * dp_init, n_edge)

bnd_q0 = np.concatenate([top_q, right_q, bot_q, left_q])
bnd_p0 = np.concatenate([top_p, right_p, bot_p, left_p])

qt_pts, pt_pts = evolve_phase_points(q0_pts, p0_pts, t_val, mass, omega)
bnd_qt, bnd_pt = evolve_phase_points(bnd_q0, bnd_p0, t_val, mass, omega)

def polygon_area(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

area_0 = dq_init * dp_init
area_t = polygon_area(bnd_qt, bnd_pt)
rho_0 = N_ens / area_0
rho_t = N_ens / area_t

# Divergence check (Eq. 2.2.9): d(q_dot)/dq + d(p_dot)/dp
phase_divergence = 0.0

# --- Key Metrics Row ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Initial Phase Area ω(0)", f"{area_0:.4f}", f"N_ens = {N_ens} points")
c2.metric("Evolved Phase Area ω(t)", f"{area_t:.4f}", f"Δω = {area_t - area_0:+.2e}")
c3.metric("Phase Density ρ(t) = N/ω(t)", f"{rho_t:.2f}", f"dρ/dt = 0 (ρ₀ = {rho_0:.2f})")
c4.metric("Phase Velocity Divergence", f"{phase_divergence:.1f}", "∂q̇/∂q + ∂ṗ/∂p = 0 (Eq. 2.2.9)")

# --- Plotting ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.2, 4.7), dpi=150)

# Panel 1: Phase Space Patch Evolution & Velocity Vector Field
lim = 3.8
qg = np.linspace(-lim, lim, 18)
pg = np.linspace(-lim, lim, 18)
QG, PG = np.meshgrid(qg, pg)
U_vel = PG / mass
V_vel = -k_spring * QG
ax1.quiver(QG, PG, U_vel, V_vel, color="#94a3b8", alpha=0.55, scale=45, width=0.0035)

# Plot initial patch
ax1.scatter(q0_pts, p0_pts, s=8, color="#1f77b4", alpha=0.45, label="Patch at t = 0")
ax1.plot(bnd_q0, bnd_p0, color="#1f77b4", lw=1.6, linestyle="--")

# Plot evolved patch at time t
ax1.scatter(qt_pts, pt_pts, s=10, color="#d62728", alpha=0.75, label=f"Patch at t = {t_val:.2f}")
ax1.plot(bnd_qt, bnd_pt, color="#d62728", lw=2.0)

# Trajectory of the center point
t_traj = np.linspace(0, t_val, 150)
qc_traj, pc_traj = evolve_phase_points(q0_center, p0_center, t_traj, mass, omega)
ax1.plot(qc_traj, pc_traj, color="#2ca02c", lw=1.6, label="Center Trajectory")
ax1.scatter([qc_traj[-1]], [pc_traj[-1]], color="#2ca02c", s=40, zorder=5)

ax1.set_xlim(-lim, lim)
ax1.set_ylim(-lim, lim)
ax1.set_xlabel(r"Generalized Position $q$")
ax1.set_ylabel(r"Generalized Momentum $p$")
ax1.set_title("Phase Fluid Motion in $(q, p)$ Space")
ax1.legend(loc="upper right", fontsize=8.5, framealpha=0.95)

# Panel 2: Area ω(t) and Phase Density ρ(t) vs Time
t_scan = np.linspace(0, 2 * np.pi / omega, 120)
areas_scan = []
rhos_scan = []
for ts in t_scan:
    bq, bp = evolve_phase_points(bnd_q0, bnd_p0, ts, mass, omega)
    a_s = polygon_area(bq, bp)
    areas_scan.append(a_s)
    rhos_scan.append(N_ens / a_s)

ax2_twin = ax2.twinx()
l1 = ax2.plot(t_scan, areas_scan, color="#1f77b4", lw=2.2, label=r"Phase Area $\omega(t)$")
l2 = ax2_twin.plot(t_scan, rhos_scan, color="#d62728", lw=2.2, linestyle="--", label=r"Phase Density $\rho(t)$")
ax2.axvline(t_val, color="#444444", linestyle=":", lw=1.3)

ax2.set_ylim(0, area_0 * 1.8)
ax2_twin.set_ylim(0, rho_0 * 1.8)
ax2.set_xlabel(r"Time $t$")
ax2.set_ylabel(r"Enclosed Area $\omega(t)$", color="#1f77b4")
ax2_twin.set_ylabel(r"Density $\rho(q,p;t)$", color="#d62728")
ax2.set_title(r"Invariance of $\omega(t)$ and $\rho(t)$ ($d\rho/dt = 0$)")

lines = l1 + l2
labels = [l.get_label() for l in lines]
ax2.legend(lines, labels, loc="upper right", fontsize=8.5, framealpha=0.95)

# Panel 3: Stationary Equilibrium Ensembles ([ρ, H] = 0, Eqs. 2.2.14 - 2.2.17)
qf = np.linspace(-lim, lim, 220)
pf = np.linspace(-lim, lim, 220)
QF, PF = np.meshgrid(qf, pf)
H_grid = 0.5 * k_spring * (QF ** 2) + (PF ** 2) / (2.0 * mass)

if ensemble_type.startswith("Approach 1"):
    E_center = 0.5 * k_spring * (q0_center ** 2) + (p0_center ** 2) / (2.0 * mass)
    delta_E = 0.35
    rho_eq = np.where(np.abs(H_grid - E_center) <= delta_E, 1.0, 0.0)
    im = ax3.contourf(QF, PF, rho_eq, levels=[-0.1, 0.5, 1.1], colors=["#f8fafc", "#2ca02c"], alpha=0.75)
    ax3.contour(QF, PF, H_grid, levels=[max(0.05, E_center - delta_E), E_center + delta_E], colors="#111111", linewidths=1.3)
    ax3.set_title(r"Microcanonical Shell: $\rho(q,p) = \text{const}$ (Eq. 2.2.14)")
else:
    kT_demo = 1.5
    rho_eq = np.exp(-H_grid / kT_demo)
    im = ax3.contourf(QF, PF, rho_eq, levels=20, cmap="YlOrRd")
    ax3.contour(QF, PF, H_grid, levels=6, colors="#333333", linewidths=0.8, alpha=0.6)
    plt.colorbar(im, ax=ax3, fraction=0.046, pad=0.04, label=r"$\rho \propto e^{-H/kT}$")
    ax3.set_title(r"Canonical Density: $\rho(q,p) \propto e^{-H/kT}$ (Eq. 2.2.17)")

ax3.set_xlabel(r"Generalized Position $q$")
ax3.set_ylabel(r"Generalized Momentum $p$")

plt.tight_layout()
st.pyplot(fig)

with st.expander("Classroom Derivation Reference (Equations from Lecture Notes)", expanded=False):
    st.latex(r"\frac{\partial \rho}{\partial t} + \operatorname{div}(\rho \mathbf{v}) = 0 \qquad (2.2.7)")
    st.latex(r"\frac{\partial \dot{q}_i}{\partial q_i} + \frac{\partial \dot{p}_i}{\partial p_i} = \frac{\partial^2 H}{\partial q_i \partial p_i} - \frac{\partial^2 H}{\partial p_i \partial q_i} = 0 \implies \frac{d\rho}{dt} = \frac{\partial \rho}{\partial t} + [\rho, H] = 0 \qquad (2.2.9,\; 2.2.12)")
    st.latex(r"\text{Equilibrium } \left(\frac{\partial \rho}{\partial t} = 0\right) \implies [\rho, H] = 0 \implies \rho = \text{const} \;\;\text{or}\;\; \rho(q,p) = \rho[H(q,p)] \qquad (2.2.13\text{–}2.2.16)")

render_sidebar_footer()