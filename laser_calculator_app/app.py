import streamlit as st
from streamlit_option_menu import option_menu

# All modules are imported correctly
from modules import (
    home, process_recommender, material_analyzer, liu_plot_analyzer,
    thermal_effects_calculator, beam_profile_visualizer,
    mask_finder, pulse_energy_calculator, fluence_calculator
)

st.set_page_config(layout="wide", page_title="Laser Process Calculator")
# Your custom CSS can remain here if you wish

# The complete registry of all tools in the application
MODES = {
    "Home": home,
    "Process Recommender": process_recommender,
    "Material Analyzer": material_analyzer,
    "Microvia Process Simulator": beam_profile_visualizer,
    "Liu Plot Analyzer": liu_plot_analyzer,
    "Thermal Effects Calculator": thermal_effects_calculator,
    "Mask Finder": mask_finder,
    "Pulse Energy": pulse_energy_calculator,
    "Fluence (Energy Density)": fluence_calculator,
}

# --- STATE MANAGEMENT ---
# Initialize the app_mode to "Home" on first run
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Home"

# The "Listener" logic: This is the core of the navigation fix.
# It checks for a message from the home page at the start of every rerun.
if "page_request" in st.session_state:
    st.session_state.app_mode = st.session_state.page_request
    del st.session_state.page_request # Consume the request so it doesn't fire again

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.header("App Mode")
    
    # Define the structure of the navigation menu
    main_tools = ["Home", "Process Recommender", "Material Analyzer", "Microvia Process Simulator"]
    main_icons = ["house-door-fill", "card-checklist", "key-fill", "bullseye"] 
    
    adv_tools = ["Liu Plot Analyzer", "Thermal Effects Calculator", "Mask Finder"]
    adv_icons = ["graph-up-arrow", "thermometer-half", "aspect-ratio-fill"]

    fund_tools = ["Pulse Energy", "Fluence (Energy Density)"]
    fund_icons = ["lightning-charge-fill", "brightness-high-fill"]
    
    all_options = main_tools + ["---"] + adv_tools + ["---"] + fund_tools
    all_icons = main_icons + [""] + adv_icons + [""] + fund_icons

    # The default_index is now robustly calculated based on the final app_mode
    try:
        current_index = all_options.index(st.session_state.app_mode)
    except ValueError:
        current_index = 0 

    selected = option_menu(
        menu_title=None,
        options=all_options,
        icons=all_icons,
        menu_icon="cast",
        default_index=current_index,
    )

    # The sidebar remains the "source of truth" for its own clicks
    if selected and selected != "---" and st.session_state.app_mode != selected:
        st.session_state.app_mode = selected
        st.rerun()

# --- MAIN PANEL ---
# This part is now simple and reliable
selected_module = MODES.get(st.session_state.app_mode)
if selected_module:
    selected_module.render()
else:
    # Provide a more helpful error message if a mode fails to load
    st.error(f"Error: Could not load the selected mode ('{st.session_state.app_mode}'). Please check if it is correctly registered in app.py.")