import base64
import os
import matplotlib.pyplot as plt
import streamlit as st

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
    st.sidebar.markdown("---")


def render_sidebar_footer():
    pass
