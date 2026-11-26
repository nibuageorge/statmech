import os
import matplotlib.pyplot as plt
import streamlit as st

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
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)

    st.sidebar.markdown(
        """
        <div style="background-color: #1e293b; color: #ffffff; padding: 10px 12px; border-radius: 8px; font-size: 0.84rem; line-height: 1.45; margin-top: 6px; margin-bottom: 10px;">
            <div style="font-weight: 700; color: #ffffff;">Developed by:</div>
            <div style="color: #ffffff;">Dr. Nibu A George, Associate Professor of Physics, Baselius College Kottayam (Autonomous)</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.markdown("---")