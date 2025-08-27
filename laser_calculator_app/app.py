import streamlit as st

# (Your imports remain the same)
from modules import (
    home, process_recommender, material_analyzer, liu_plot_analyzer, 
    thermal_effects_calculator, beam_profile_visualizer, mask_finder, 
    pulse_energy_calculator, fluence_calculator
)

# --- PAGE CONFIGURATION (Remains the same) ---
st.set_page_config(
    layout="wide", 
    page_title="Laser Dashboard",
    initial_sidebar_state="expanded"
)

# --- UPGRADED CSS FOR PROFESSIONAL STYLING ---
st.markdown("""
<style>
    /* Main App Styling */
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    /* Sidebar Styling (Unchanged) */
    [data-testid="stSidebar"] { padding-top: 1.5rem; }
    [data-testid="stSidebar"] .stButton button[data-testid="stButton-Home"] {
        font-size: 1.5rem; font-weight: 700; padding: 10px 15px; text-align: left !important;
        background-color: transparent; color: #111827; border: none;
    }
    [data-testid="stSidebar"] .stButton button[data-testid="stButton-Home"]:hover {
        background-color: #F3F4F6; color: #ef4444;
    }
    [data-testid="stSidebar"] .stButton button[data-testid="stButton-Home"]:focus { box-shadow: none; }
    [data-testid="stSidebar"] .stButton button {
        text-align: left !important; font-weight: 500; padding: 10px 15px; border-radius: 8px;
    }
    [data-testid="stSidebar"] .stExpander {
        border: none !important; box-shadow: none !important;
    }
    [data-testid="stSidebar"] .stExpander summary {
        padding: 10px 15px; border-radius: 8px; font-weight: 500; font-size: 1rem;
    }

    /* --- NEW: Modern Card Styling for Home Page Containers --- */
    /* This targets the containers you created with st.container(border=True) */
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: #FFFFFF; /* Ensure a white background */
        border-radius: 12px;       /* Softer, more modern rounded corners */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1); /* Professional shadow */
        border: none;              /* Remove the default border */
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; /* Smooth transition for hover */
        padding: 1.5rem;           /* Consistent internal padding */
    }

    /* --- NEW: Hover Animation for the Cards --- */
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
        transform: translateY(-5px); /* Subtly lift the card on hover */
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1); /* Deeper shadow on hover */
    }

    /* Hide Streamlit Branding (Unchanged) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# (The rest of your app.py, including the navigation logic, remains EXACTLY THE SAME)
# --- APP STATE AND NAVIGATION ---
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Home"

# --- HIERARCHICAL MODULE DICTIONARY ---
TOOL_CATEGORIES = {
    "Core Workflow": {
        "Material Analyzer": material_analyzer,
        "Process Recommender": process_recommender,
        "Microvia Process Simulator": beam_profile_visualizer,
    },
    "Advanced Analysis": {
        "Liu Plot Analyzer": liu_plot_analyzer,
        "Thermal Effects Calculator": thermal_effects_calculator,
    },
    "Fundamental Calculators": {
        "Mask Finder": mask_finder,
        "Pulse Energy": pulse_energy_calculator,
        "Fluence (Energy Density)": fluence_calculator,
    }
}

# --- SIDEBAR RENDERING ---
with st.sidebar:
    if st.button("Laser Dashboard", use_container_width=True, key="stButton-Home"):
        st.session_state.app_mode = "Home"
        st.rerun()
    st.markdown("---")
    for category_name, tools in TOOL_CATEGORIES.items():
        with st.expander(category_name, expanded=True):
            for tool_name, tool_module in tools.items():
                btn_type = "primary" if st.session_state.app_mode == tool_name else "secondary"
                if st.button(tool_name, use_container_width=True, type=btn_type):
                    st.session_state.app_mode = tool_name
                    st.rerun()

# --- MAIN PANEL DISPATCHER ---
selected_module = None
if st.session_state.app_mode == "Home":
    selected_module = home
else:
    for category in TOOL_CATEGORIES.values():
        if st.session_state.app_mode in category:
            selected_module = category[st.session_state.app_mode]
            break

if selected_module:
    selected_module.render()
else:
    st.session_state.app_mode = "Home"
    st.rerun()