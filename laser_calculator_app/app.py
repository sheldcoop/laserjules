import streamlit as st

# Step 1: Import all the modules you will create
from modules import (
    process_recommender,
    material_analyzer,
    liu_plot_analyzer,
    taper_angle_calculator,
    thermal_effects_calculator,
    beam_profile_visualizer,
    mask_finder,
    pulse_energy_calculator,
    fluence_calculator
)

# --- PAGE CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Laser Process Calculator")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        body { font-family: 'Inter', sans-serif; }
        [data-testid="stSidebar"] { padding: 20px; }
        h1 { padding-top: 20px; padding-bottom: 10px; }
        [data-testid="stSidebar"] .stButton button {
            text-align: left !important; font-weight: 500; padding: 10px 15px; border-radius: 8px;
        }
        div[data-testid="stTextInput"] > div > div > input, 
        div[data-testid="stNumberInput"] > div > div > input {
            background-color: #ffffff; border: 1px solid #ced4da; border-radius: 8px; padding: 10px; transition: all 0.2s ease-in-out;
        }
        div[data-testid="stTextInput"] > div > div > input:focus, 
        div[data-testid="stNumberInput"] > div > div > input:focus {
            border-color: #ef4444; box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2); outline: none;
        }
        .stDataFrame thead th { background-color: #e9ecef; color: #212529; font-weight: 600; }
        .results-header { font-size: 22px; font-weight: 600; color: #16a34a; }
        hr { margin: 2rem 0; border-color: #e0e0e0; }
    </style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Process Recommender"

def clear_results():
    """Clears all result-related session state variables."""
    for key in list(st.session_state.keys()):
        if key.endswith('_results') or key in ['results_df', 'recipe', 'liu_results', 'analysis_results']:
            del st.session_state[key]

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.header("App Mode")

    # Step 2: Create a dictionary mapping the name of the mode to the imported module
    MODES = {
        "Process Recommender": process_recommender,
        "Material Analyzer": material_analyzer,
        "Liu Plot Analyzer": liu_plot_analyzer,
        #"Taper Angle Calculator": taper_angle_calculator,
        "Thermal Effects Calculator": thermal_effects_calculator,
        "Beam Profile Visualizer": beam_profile_visualizer,
        "Mask Finder": mask_finder,
        "Pulse Energy": pulse_energy_calculator,
        "Fluence (Energy Density)": fluence_calculator,
    }

    for mode_name in MODES.keys():
        btn_type = "primary" if st.session_state.app_mode == mode_name else "secondary"
        if st.button(mode_name, use_container_width=True, type=btn_type):
            if st.session_state.app_mode != mode_name:
                st.session_state.app_mode = mode_name
                clear_results()
                st.rerun()

# --- MAIN PANEL & FUNCTION DISPATCHER ---
st.title("Advanced Laser Process Calculator")

# Step 3: Get the correct module from the dictionary and call its .render() function
selected_module = MODES.get(st.session_state.app_mode)
if selected_module:
    selected_module.render()
else:
    st.error("Selected mode not found.")