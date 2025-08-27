import streamlit as st
from streamlit_option_menu import option_menu

# --- Step 1: Update imports - remove liu_plot_analyzer ---
from modules import (
    home, process_recommender, material_analyzer,
    taper_angle_calculator, thermal_effects_calculator, beam_profile_visualizer,
    mask_finder, pulse_energy_calculator, fluence_calculator
)

# (Your Page Config and CSS remain the same)
st.set_page_config(layout="wide", page_title="Laser Process Calculator")
st.markdown("""
    <style>
        /* ... Your existing CSS ... */
    </style>
""", unsafe_allow_html=True)

if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Home"

# --- Step 2: Update the MODES dictionary - remove Liu Plot Analyzer ---
MODES = {
    "Home": home,
    "Process Recommender": process_recommender,
    "Material Analyzer": material_analyzer,
    "Thermal Effects Calculator": thermal_effects_calculator,
    "Beam Profile Visualizer": beam_profile_visualizer,
    "Mask Finder": mask_finder,
    "Pulse Energy": pulse_energy_calculator,
    "Fluence (Energy Density)": fluence_calculator,
}

with st.sidebar:
    st.header("App Mode")
    
    # --- Step 3: Update the navigation menu - remove Liu Plot Analyzer ---
    main_tools = ["Home", "Process Recommender", "Material Analyzer", "Beam Profile Visualizer"]
    main_icons = ["house-door-fill", "card-checklist", "key", "bullseye"] 
    
    # "Liu Plot Analyzer" is removed from this list
    adv_tools = ["Thermal Effects Calculator", "Mask Finder"]
    adv_icons = ["thermometer-half", "aspect-ratio"]

    fund_tools = ["Pulse Energy", "Fluence (Energy Density)"]
    fund_icons = ["lightning-charge-fill", "brightness-high-fill"]

    selected = option_menu(
        menu_title=None,
        options=main_tools + ["---"] + adv_tools + ["---"] + fund_tools,
        icons=main_icons + [""] + adv_icons + [""] + fund_icons,
        menu_icon="cast",
        default_index=main_tools.index(st.session_state.app_mode) if st.session_state.app_mode in main_tools else 0
    )

    if selected and selected != "---" and st.session_state.app_mode != selected:
        st.session_state.app_mode = selected
        st.rerun()

# (The main panel logic remains the same)
selected_module = MODES.get(st.session_state.app_mode)
if selected_module:
    selected_module.render()
else:
    st.error("Selected mode not found.")