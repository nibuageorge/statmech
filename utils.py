import base64
import os
import matplotlib.pyplot as plt
import streamlit as st

MODULES = [
    ("Home", "🏠 Home — Syllabus Overview"),
    ("01_Thermal_Contact.py", "01. Thermal Contact & Sharpness of Ω⁽⁰⁾"),
    ("02_Gibbs_Paradox.py", "02. Entropy of Mixing & Gibbs Paradox"),
    ("03_Hypersphere_and_Processes.py", "03. 3N Hypersphere & Gas Processes"),
    ("04_Liouville_Theorem.py", "04. Liouville's Theorem & Phase Fluid"),
    ("05_Harmonic_Oscillator_Phase_Space.py", "05. 1D Oscillator & Planck Cells"),
    ("06_Canonical_Energy_Fluctuations.py", "06. Canonical Energy Fluctuations"),
    ("07_Equipartition_Theorem.py", "07. The Equipartition Theorem"),
    ("08_Grand_Canonical_Models.py", "08. Grand Canonical Gas & Lattice"),
    ("09_Solid_Vapor_Equilibrium.py", "09. Solid–Vapor Equilibrium"),
    ("10_Grand_Canonical_Fluctuations.py", "10. Open-System Fluctuations"),
]

INTERPRETATIONS = {
    "01_Thermal_Contact.py": {
        "title": "Physical Interpretation: Thermal Contact & Sharpness of Ω⁽⁰⁾",
        "metrics": (
            "The top metrics compare the equilibrium energy split (E₁*, E₂*) where β₁ = β₂ "
            "against the relative fluctuation width ΔE₁ / E₁*."
        ),
        "plots": (
            "• **Left Panel (Product of Microstates Ω₁Ω₂):** Shows that while Ω₁(E₁) rises steeply with E₁ and "
            "Ω₂(E⁽⁰⁾ − E₁) falls steeply, their product forms an extraordinarily sharp peak at E₁*.\n"
            "• **Center Panel (Logarithmic Entropy Balance):** Shows the slopes ∂ ln Ω₁ / ∂E₁ = β₁ and "
            "∂ ln Ω₂ / ∂E₂ = β₂ intersecting at equal temperature T₁ = T₂.\n"
            "• **Right Panel (1/√N Sharpness Scaling):** Demonstrates that as particle numbers N₁, N₂ increase, "
            "the relative width ΔE₁ / E₁* shrinks as 1/√N, proving why macroscopic thermal fluctuations are unobservable."
        ),
        "takeaway": (
            "Increase N₁ and N₂ in the sidebar to observe the equilibrium peak collapse into a Dirac-delta-like spike—"
            "justifying why the most probable macrostate equals the thermodynamic equilibrium state."
        ),
    },
    "02_Gibbs_Paradox.py": {
        "title": "Physical Interpretation: Entropy of Mixing & the Gibbs Paradox",
        "metrics": (
            "The top metrics contrast the uncorrected classical mixing entropy ΔS_classical against the "
            "quantum-corrected value ΔS_corrected obtained after dividing Ω by N!."
        ),
        "plots": (
            "• **Left Panel (Mixing Entropy vs. Mole Fraction):** Shows ΔS_mix peaking at 50%–50% composition "
            "(ΔS = 2Nk ln 2) for distinct gases, whereas for identical gases the classical formula erroneously predicts "
            "the same non-zero jump.\n"
            "• **Center Panel (Extensivity Test S(N) vs. N):** Demonstrates that without the 1/N! factor, entropy grows "
            "super-linearly (S ∝ N ln V), violating thermodynamic extensivity; with 1/N!, S scales strictly linearly with N.\n"
            "• **Right Panel (Entropy per Particle s = S/N):** Confirms that specific entropy depends only on intensive "
            "ratios (V/N and E/N) once indistinguishability is accounted for."
        ),
        "takeaway": (
            "Toggle between 'Distinct Gases' and 'Identical Gases' in the sidebar to see how Gibbs' ad-hoc 1/N! factor "
            "eliminates the spurious entropy jump upon removing a partition between identical fluids."
        ),
    },
    "03_Hypersphere_and_Processes.py": {
        "title": "Physical Interpretation: 3N-Dimensional Hypersphere & Ideal Gas Processes",
        "metrics": (
            "The top metrics report the total accessible phase-space volume Ω(E) and the fraction of that volume "
            "residing inside a thin outer shell of thickness δR / R."
        ),
        "plots": (
            "• **Left Panel (Shell Volume Concentration):** Shows that in high dimensions (3N ≫ 1), nearly 100% of a "
            "hypersphere's volume is concentrated right at its outer surface R = √(2mE)—explaining why Ω(E) ≈ Σ(E).\n"
            "• **Center Panel (Sackur–Tetrode Entropy Surface):** Visualizes how entropy S(E, V) grows logarithmically "
            "with volume V and thermal energy E.\n"
            "• **Right Panel (Isothermal vs. Adiabatic Paths):** Contrasts constant-T expansion (PV = const) with "
            "constant-S reversible adiabatic expansion (PV^γ = const, γ = 5/3)."
        ),
        "takeaway": (
            "Raise N in the sidebar from 1 to 100 to watch the shell volume fraction jump to 1.000—"
            "demonstrating the geometric origin of microcanonical state counting in 3N momentum space."
        ),
    },
    "04_Liouville_Theorem.py": {
        "title": "Physical Interpretation: Liouville's Theorem & Incompressible Phase Fluid",
        "metrics": (
            "The top metrics track the initial phase-space area Γ(0), evolved area Γ(t), and relative area drift "
            "|Γ(t) − Γ(0)| / Γ(0), confirming exact conservation."
        ),
        "plots": (
            "• **Left Panel (Phase-Space Swarm Evolution):** Tracks an ensemble patch of initial conditions (q₀, p₀) "
            "evolving under Hamilton's equations; even as the patch stretches or rotates, its enclosed area stays invariant.\n"
            "• **Center Panel (Density Conservation dρ/dt = 0):** Shows that local phase-point density ρ(q, p, t) "
            "remains constant along any dynamical trajectory, behaving like an incompressible fluid.\n"
            "• **Right Panel (Area Conservation Verification):** Plots Γ(t)/Γ(0) = 1 across time steps."
        ),
        "takeaway": (
            "Increase the evolution time t or anharmonicity in the sidebar: although the phase patch filaments and "
            "deforms strongly, Liouville's theorem guarantees exact preservation of phase-space volume."
        ),
    },
    "05_Harmonic_Oscillator_Phase_Space.py": {
        "title": "Physical Interpretation: 1D Harmonic Oscillator & Planck Quantum Cells",
        "metrics": (
            "The top metrics compare the classical phase-space ellipse area ∮ p dq = E / ν with the semiclassical "
            "number of enclosed quantum states n = E / (hν)."
        ),
        "plots": (
            "• **Left Panel (Nested Elliptical Trajectories):** Displays constant-energy ellipses q²/(2E/mω²) + p²/(2mE) = 1 "
            "in the (q, p) plane.\n"
            "• **Center Panel (Planck Cell Partitioning):** Divides phase space into quantized shells of equal area "
            "Δ(∮ p dq) = h, bridging classical phase integrals with Bohr–Sommerfeld quantization E_n = (n + 1/2)ħω.\n"
            "• **Right Panel (Cumulative States Σ(E) vs. Energy):** Shows the staircase quantum state count tracked "
            "smoothly by the classical area ratio E / (hν)."
        ),
        "takeaway": (
            "Adjust the oscillator frequency ω and maximum energy E to verify that adjacent energy shells always "
            "enclose the universal quantum of action h = 2πħ."
        ),
    },
    "06_Canonical_Energy_Fluctuations.py": {
        "title": "Physical Interpretation: Canonical Energy Fluctuations & Ensemble Equivalence",
        "metrics": (
            "The top metrics display mean energy U = ⟨E⟩, constant-volume heat capacity C_V, and the relative RMS "
            "energy fluctuation √⟨ΔE²⟩ / U."
        ),
        "plots": (
            "• **Left Panel (Canonical Probability Peak P(E) ∝ g(E)e^(-βE)):** Although the Boltzmann factor e^(-βE) "
            "decays monotonically, multiplying by the rapidly rising density of states g(E) ∝ E^(3N/2) creates a narrow "
            "Gaussian peak centered at U.\n"
            "• **Center Panel (Competing Factors on Log Scale):** Illustrates the exact balance point ∂ ln g / ∂E = β "
            "where the peak occurs.\n"
            "• **Right Panel (1/√N Relative Fluctuation Scaling):** Shows √⟨ΔE²⟩ / U = √(2 / 3N) → 0 as N grows."
        ),
        "takeaway": (
            "Increase N in the sidebar to see P(E) sharpen around U—proving that canonical and microcanonical "
            "ensembles yield identical thermodynamics in the macroscopic limit."
        ),
    },
    "07_Equipartition_Theorem.py": {
        "title": "Physical Interpretation: The Equipartition Theorem in Classical Phase Space",
        "metrics": (
            "The top metrics show the mean thermal energy per quadratic degree of freedom ⟨ε_i⟩ in units of ½kT "
            "and compare classical vs. quantum heat capacities."
        ),
        "plots": (
            "• **Left Panel (Thermal Distribution Over Quadratic Coordinates):** Shows Gaussian Boltzmann distributions "
            "exp(−β c_i x_i²) whose variance widens linearly with temperature T.\n"
            "• **Center Panel (Mean Energy per Degree of Freedom):** Confirms that every independent quadratic term "
            "(p²/2m or ½κq²) carries exactly ½kT classically, regardless of mass m or spring constant κ.\n"
            "• **Right Panel (Quantum Freeze-Out Departure):** Shows how vibrational modes freeze out below the Einstein "
            "temperature Θ_E = ħω / k, explaining why classical equipartition fails at low T."
        ),
        "takeaway": (
            "Lower the temperature T in the sidebar to observe the crossover from the classical ½kT plateau "
            "into the quantum freeze-out regime where kT ≪ ħω."
        ),
    },
    "08_Grand_Canonical_Models.py": {
        "title": "Physical Interpretation: Grand Canonical Ideal Gas vs. Localised Lattice Sites",
        "metrics": (
            "The top metrics report fugacity z = e^(βμ), mean particle occupancy N̄, and the grand partition "
            "potential ln 𝒬 = PV / (kT)."
        ),
        "plots": (
            "• **Left Panel (Grand Canonical Particle Distribution P(N)):** Shows Poissonian particle-number "
            "fluctuations around N̄ = zV / λ³ in an open volume exchanging particles with a reservoir.\n"
            "• **Center Panel (Ideal Gas vs. Localised Langmuir Adsorption):** Contrasts unbounded gas occupation "
            "with single-site saturation θ = z e^(βε₀) / [1 + z e^(βε₀)] on a lattice.\n"
            "• **Right Panel (Equation of State PV vs. N̄kT):** Confirms PV = N̄kT for the ideal gas alongside "
            "site-saturation compression at high chemical potential μ."
        ),
        "takeaway": (
            "Increase chemical potential μ in the sidebar to watch mean particle count N̄ rise unboundedly in the "
            "gas while saturating asymptotically at 1 particle per site on the lattice."
        ),
    },
    "09_Solid_Vapor_Equilibrium.py": {
        "title": "Physical Interpretation: Solid–Vapor Equilibrium & Sublimation Phase Boundary",
        "metrics": (
            "The top metrics identify the condensation threshold temperature T_c, equilibrium vapor fraction N_g/N, "
            "condensed solid fraction N_s/N, and vessel pressure P."
        ),
        "plots": (
            "• **Left Panel (Sublimation Coexistence Curve P_vapor(T)):** Tracks the exponential vapor pressure "
            "P_vapor(T) ∝ e^(−ε/kT); when T < T_c, vessel pressure is pinned to P_vapor(T), while for T ≥ T_c all "
            "solid has sublimated and pressure follows the ideal gas line P = (N/V)kT.\n"
            "• **Center Panel (Phase Split N_g/N vs. N_s/N):** Shows solid condensing out of the vapor as soon as "
            "temperature drops below T_c.\n"
            "• **Right Panel (Arrhenius / Clausius–Clapeyron Plot):** Plots ln P_vapor vs. ħω/(kT), whose linear "
            "slope directly measures the sublimation binding energy −ε."
        ),
        "takeaway": (
            "Sweep the vessel temperature kT/(ħω) across T_c in the sidebar to watch the solid phase appear and "
            "disappear cleanly at the phase boundary."
        ),
    },
    "10_Grand_Canonical_Fluctuations.py": {
        "title": "Physical Interpretation: Open-System Density & Energy Fluctuations",
        "metrics": (
            "The top metrics report particle variance ⟨ΔN²⟩, the closed-system canonical energy variance kT²C_V, "
            "and the extra particle-exchange variance [(∂U/∂N̄)_{T,V}]² ⟨ΔN²⟩."
        ),
        "plots": (
            "• **Left Panel (Open-System Particle Distribution P(N)):** Compares the narrow ideal-gas Poisson width "
            "(κ_T = κ_ideal) with the broadened distribution when isothermal compressibility κ_T is enhanced.\n"
            "• **Center Panel (Decomposition of Energy Variance ⟨ΔE²⟩):** Separates constant-N thermal fluctuations "
            "from particle-exchange fluctuations, showing why ⟨ΔE²⟩ diverges near a critical point (critical opalescence).\n"
            "• **Right Panel (1/√N̄ Ensemble Equivalence):** Shows that for any finite κ_T, both relative density and "
            "energy fluctuations vanish as 1/√N̄ in the thermodynamic limit."
        ),
        "takeaway": (
            "Increase the compressibility ratio κ_T / κ_ideal in the sidebar to simulate approaching a critical point "
            "and observe the particle-exchange fluctuation term dominate total energy fluctuations."
        ),
    },
}

LOGO_SVG = """
<svg width="100%" viewBox="0 0 320 120" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b1324"/>
      <stop offset="100%" stop-color="#17233b"/>
    </linearGradient>
    <linearGradient id="ellipseGrad" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22d3ee"/>
      <stop offset="55%" stop-color="#818cf8"/>
      <stop offset="100%" stop-color="#c084fc"/>
    </linearGradient>
    <linearGradient id="peakGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22d3ee"/>
      <stop offset="50%" stop-color="#a855f7"/>
      <stop offset="100%" stop-color="#fb923c"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="316" height="116" rx="14" fill="url(#bgGrad)" stroke="#38bdf8" stroke-width="2.5"/>
  <g stroke="#334155" stroke-width="0.9" stroke-dasharray="3,3">
    <line x1="22" y1="60" x2="152" y2="60"/>
    <line x1="87" y1="14" x2="87" y2="106"/>
    <line x1="30" y1="95" x2="144" y2="25"/>
  </g>
  <g transform="translate(87, 60) rotate(-28)">
    <ellipse cx="0" cy="0" rx="58" ry="30" fill="none" stroke="url(#ellipseGrad)" stroke-width="1.6" stroke-opacity="0.95"/>
    <ellipse cx="0" cy="0" rx="45" ry="23" fill="none" stroke="url(#ellipseGrad)" stroke-width="1.5" stroke-opacity="0.85"/>
    <ellipse cx="0" cy="0" rx="33" ry="16.5" fill="none" stroke="url(#ellipseGrad)" stroke-width="1.4" stroke-opacity="0.75"/>
    <ellipse cx="0" cy="0" rx="22" ry="11" fill="none" stroke="url(#ellipseGrad)" stroke-width="1.4" stroke-opacity="0.7"/>
    <ellipse cx="0" cy="0" rx="12" ry="6" fill="none" stroke="#38bdf8" stroke-width="1.4" stroke-opacity="0.9"/>
  </g>
  <path d="M 48 96 Q 82 95 94 64 Q 103 38 112 64 Q 124 95 154 96"
        fill="none" stroke="url(#peakGrad)" stroke-width="2.6" stroke-linecap="round"/>
  <text x="236" y="54" text-anchor="middle" fill="#ffffff"
        font-family="Segoe UI, Arial, sans-serif" font-size="40" font-weight="800" letter-spacing="2">NAG</text>
  <text x="236" y="77" text-anchor="middle" fill="#38bdf8"
        font-family="Segoe UI, Arial, sans-serif" font-size="16" font-weight="700" letter-spacing="1.4">STAT MECH</text>
  <text x="236" y="96" text-anchor="middle" fill="#cbd5e1"
        font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="500" letter-spacing="1">VIRTUAL LAB</text>
</svg>
"""


def apply_plot_style():
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#333333",
        "axes.grid": True,
        "grid.alpha": 0.25,
        "font.size": 11
    })


def render_sidebar_header():
    if st.session_state.get("_header_rendered", False):
        return st.session_state.get("_selected_file", "Home")
    st.session_state["_header_rendered"] = True

    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] { display: none; }
        </style>
        """,
        unsafe_allow_html=True
    )

    root_dir = os.path.dirname(os.path.abspath(__file__))
    logo_png = os.path.join(root_dir, "logo.png")

    if os.path.exists(logo_png):
        st.sidebar.image(logo_png, use_container_width=True)
    else:
        b64_svg = base64.b64encode(LOGO_SVG.encode("utf-8")).decode("utf-8")
        st.sidebar.markdown(
            f'<img src="data:image/svg+xml;base64,{b64_svg}" style="width:100%; border-radius:10px; display:block;"/>',
            unsafe_allow_html=True
        )

    st.sidebar.markdown(
        """
        <div style="background-color: #1e293b; color: #ffffff; padding: 10px 12px; border-radius: 8px; font-size: 0.84rem; line-height: 1.45; margin-top: 8px; margin-bottom: 10px;">
            <div style="font-weight: 700; color: #ffffff;">Developed by:</div>
            <div style="color: #ffffff;">Dr. Nibu A George, Associate Professor of Physics, Baselius College Kottayam (Autonomous)</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("### Simulations")
    labels = [label for _, label in MODULES]
    selected_label = st.sidebar.radio(
        "Select Module",
        options=labels,
        label_visibility="collapsed",
        key="active_sim_module"
    )
    st.sidebar.markdown("---")

    label_to_file = {label: fname for fname, label in MODULES}
    chosen = label_to_file[selected_label]
    st.session_state["_selected_file"] = chosen
    return chosen


def run_module_file(filename):
    st.session_state["_current_module_file"] = filename
    root_dir = os.path.dirname(os.path.abspath(__file__))
    candidate_paths = [
        os.path.join(root_dir, "pages", filename),
        os.path.join(root_dir, "Pages", filename),
        os.path.join(root_dir, filename),
    ]
    target_path = next((p for p in candidate_paths if os.path.exists(p)), None)

    if target_path is None:
        st.error(f"Could not find `{filename}` in `pages/`. Please verify the file is uploaded.")
        return

    with open(target_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    cleaned_lines = []
    skip_paren = 0
    for line in source_code.splitlines():
        if "st.set_page_config" in line:
            skip_paren += line.count("(") - line.count(")")
            continue
        if skip_paren > 0:
            skip_paren += line.count("(") - line.count(")")
            continue
        cleaned_lines.append(line)

    exec_globals = {"__name__": "__main__", "__file__": target_path}
    exec("\n".join(cleaned_lines), exec_globals)


def render_sidebar_footer():
    current_file = st.session_state.get("_current_module_file")
    if not current_file:
        # Fallback if a page script is ever executed directly
        import inspect
        for frame_info in inspect.stack():
            fname = os.path.basename(frame_info.filename)
            if fname in INTERPRETATIONS:
                current_file = fname
                break

    guide = INTERPRETATIONS.get(current_file)
    if guide:
        st.markdown("---")
        with st.expander(f"📘 {guide['title']}", expanded=True):
            st.markdown(f"**1. How to Read the Top Metric Cards:** {guide['metrics']}")
            st.markdown("**2. How to Read the Three Plots:**")
            st.markdown(guide["plots"])
            st.info(f"**Classroom Experiment:** {guide['takeaway']}")