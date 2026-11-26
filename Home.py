import streamlit as st
from utils import render_sidebar_header

st.set_page_config(
    page_title="Statistical Mechanics Virtual Lab",
    layout="wide"
)

render_sidebar_header()

st.title("Statistical Mechanics Virtual Laboratory")
st.subheader("M.Sc. Physics — Mahatma Gandhi University, Kottayam")
st.markdown(
    "Interactive numerical simulations accompanying the lecture notes based on "
    "*Statistical Mechanics* by **R. K. Pathria & Paul D. Beale**."
)

st.markdown("---")

st.markdown("""
### Syllabus Modules (Chapters 1–4)

* **Chapter 1: The Statistical Basis of Thermodynamics**
  * **01 — Thermal Contact & Sharpness of $\\Omega^{(0)}(E^{(0)}, E_1)$** *(Eqs. 1.2.1–1.2.7 & 1.4.14)*
  * **02 — Entropy of Mixing, Gibbs Paradox & the $1/N!$ Correction** *(Eqs. 1.5.1–1.5.6)*
  * **03 — $3N$-Dimensional Hypersphere State Counting & Ideal Gas Processes** *(Eqs. 1.4.5–1.4.29)*
* **Chapter 2: Elements of Ensemble Theory & Liouville's Theorem**
  * **04 — Liouville's Theorem: Incompressible Phase Fluid Flow** *(Eqs. 2.1.1–2.2.17)*
  * **05 — 1D Harmonic Oscillator Phase Space & Planck Quantum Cells** *(Eqs. 2.3.18–2.3.21)*
* **Chapter 3: Introduction to the Canonical Ensemble**
  * **06 — Canonical Energy Fluctuations & Equivalence with Microcanonical Ensemble** *(Eqs. 3.6.3–3.6.10)*
  * **07 — The Equipartition Theorem in Classical Phase Space** *(Eqs. 3.7.1–3.7.9)*
* **Chapter 4: The Grand Canonical Ensemble Formalism**
  * **08 — Classical Ideal Gas vs. Localised Particles in the Grand Canonical Ensemble** *(Eqs. 4.4.1–4.4.24)*
  * **09 — Solid–Vapor Equilibrium & Sublimation Phase Boundary** *(Eqs. 4.4.25–4.4.34)*
  * **10 — Open-System Density & Energy Fluctuations** *(Eqs. 4.5.3–4.5.14)*
""")

st.info("Select any simulation module from the left sidebar to launch the interactive plots.")

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #94a3b8; font-size: 0.9rem;">
        <strong>Developed by:</strong> Dr. Nibu A George, Associate Professor of Physics, Baselius College Kottayam (Autonomous) | <em>An IQAC Initiative</em>
    </div>
    """,
    unsafe_allow_html=True
)