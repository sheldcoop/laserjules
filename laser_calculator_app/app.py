import streamlit as st
from streamlit_option_menu import option_menu

# Import all modules
from modules import (
    home, process_recommender, material_analyzer, liu_plot_analyzer, 
    thermal_effects_calculator, beam_profile_visualizer, mask_finder, 
    pulse_energy_calculator, fluence_calculator, documentation
)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    layout="wide", 
    page_title="Laser Dashboard",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
# Adjusted to support streamlit-option-menu and general aesthetic improvements
st.markdown("""
<style>
    /* Main App Styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        padding-top: 1.5rem;
    }

    /* streamlit-option-menu adjustments */
    .nav-item .nav-link {
        font-weight: 500;
    }
    .nav-item .nav-link[aria-current="page"] {
        font-weight: 700;
        background-color: #ef4444 !important; /* Theme color */
        color: white !important;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- MODULE & NAVIGATION SETUP ---
# Combine all tools and modules into one dictionary for easier lookup
ALL_MODULES = {
    "Home": home,
    "Material Analyzer": material_analyzer,
    "Process Recommender": process_recommender,
    "Microvia Process Simulator": beam_profile_visualizer,
    "Liu Plot Analyzer": liu_plot_analyzer,
    "Thermal Effects Calculator": thermal_effects_calculator,
    "Mask Finder": mask_finder,
    "Pulse Energy": pulse_energy_calculator,
    "Fluence (Energy Density)": fluence_calculator,
    "Scientific Reference": documentation
}

# --- SIDEBAR RENDERING ---
with st.sidebar:
    st.markdown("<h1 style='text-align: left; font-size: 1.75rem; font-weight: 700;'>Laser Dashboard</h1>", unsafe_allow_html=True)
    
    selected_option = option_menu(
        menu_title=None,  # Hides the menu title
        options=["Home", "Core Workflow", "Advanced Analysis", "Fundamental Calculators", "Scientific Reference"],
        icons=["house-door-fill", "kanban-fill", "graph-up-arrow", "calculator-fill", "book-fill"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important"},
            "icon": {"font-size": "1.2rem"},
            "nav-link": {"font-size": "1rem", "text-align": "left", "margin":"0px"},
            "nav-link-selected": {"background-color": "#ef4444"},
        }
    )

    # Sub-menu logic
    sub_selection = None
    if selected_option == "Core Workflow":
        sub_selection = option_menu(menu_title=None, options=["Material Analyzer", "Process Recommender", "Microvia Process Simulator"], icons=["🔬", "⚙️", "🌀"])
    elif selected_option == "Advanced Analysis":
        sub_selection = option_menu(menu_title=None, options=["Liu Plot Analyzer", "Thermal Effects Calculator"], icons=["📈", "🔥"])
    elif selected_option == "Fundamental Calculators":
        sub_selection = option_menu(menu_title=None, options=["Mask Finder", "Pulse Energy", "Fluence (Energy Density)"], icons=["🎭", "⚡", "🎯"])

    # Determine the final selected page
    final_selection = sub_selection if sub_selection else selected_option
    
    # Update session state
    if 'app_mode' not in st.session_state or st.session_state.app_mode != final_selection:
        st.session_state.app_mode = final_selection
        st.rerun()

# --- MAIN PANEL DISPATCHER ---
# Use the unified dictionary to render the selected module
if st.session_state.app_mode in ALL_MODULES:
    ALL_MODULES[st.session_state.app_mode].render()
else:
    # Default to home if something goes wrong
    st.session_state.app_mode = "Home"
    st.rerun()
