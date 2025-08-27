import streamlit as st

# Import all modules
from modules import (
    home, process_recommender, material_analyzer, liu_plot_analyzer, 
    thermal_effects_calculator, beam_profile_visualizer, mask_finder, 
    pulse_energy_calculator, fluence_calculator
)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    layout="wide", 
    page_title="Laser Dashboard",
    initial_sidebar_state="expanded"
)

# --- NEW CSS WITH HOVER ANIMATIONS & PROFESSIONAL STYLING ---
st.markdown("""
<style>
    /* Main App Styling */
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    body { background-color: #F0F2F6; } /* Soft gray background */
    [data-testid="stSidebar"] {
        padding-top: 1.5rem;
        background-color: #FFFFFF;
        border-right: 1px solid #E0E0E0;
    }

    /* Home Button Styling */
    [data-testid="stSidebar"] .stButton button[data-testid="stButton-Home"] {
        font-size: 1.5rem; font-weight: 700; text-align: left !important;
        background-color: transparent; color: #111827; border: none;
        transition: color 0.2s ease-in-out, background-color 0.2s ease-in-out;
    }
    [data-testid="stSidebar"] .stButton button[data-testid="stButton-Home"]:hover {
        background-color: #F3F4F6; color: #4F46E5; /* Indigo hover color */
    }

    /* Sidebar Expanders */
    [data-testid="stSidebar"] .stExpander {
        border: none !important; box-shadow: none !important;
    }
    [data-testid="stSidebar"] .stExpander summary {
        padding: 10px 15px; border-radius: 8px; font-weight: 500; font-size: 1rem;
    }
    
    /* Sidebar Tool Buttons with Hover Animation */
    [data-testid="stSidebar"] .stButton button {
        text-align: left !important; font-weight: 500;
        padding: 10px 15px; border-radius: 8px;
        transition: all 0.2s ease-in-out; /* Smooth transition for all properties */
    }
    [data-testid="stSidebar"] .stButton button:hover {
        transform: translateY(-2px); /* LIFT EFFECT */
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); /* Add shadow on hover */
    }
    
    /* Selected (primary) button style */
    [data-testid="stSidebar"] .stButton button[kind="primary"] {
        background-color: #4F46E5; /* Indigo for selected */
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# --- APP STATE AND NAVIGATION (This logic is stable and correct) ---
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Home"

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

# --- SIDEBAR RENDERING (This logic is stable and correct) ---
with st.sidebar:
    if st.button("Laser Dashboard", use_container_width=True, key="stButton-Home"):
        st.session_state.app_mode = "Home"
        st.rerun()

    st.markdown("---")
    
    for category_name, tools in TOOL_CATEGORIES.items():
        with st.expander(category_name, expanded=True):
            for tool_name, tool_module in tools.items():
                is_selected = (st.session_state.app_mode == tool_name)
                if st.button(tool_name, use_container_width=True, type="primary" if is_selected else "secondary"):
                    st.session_state.app_mode = tool_name
                    st.rerun()

# --- MAIN PANEL DISPATCHER (This logic is stable and correct) ---
selected_module = home
if st.session_state.app_mode != "Home":
    for category in TOOL_CATEGORIES.values():
        if st.session_state.app_mode in category:
            selected_module = category[st.session_state.app_mode]
            break

if selected_module:
    selected_module.render()
else:
    st.session_state.app_mode = "Home"
    st.rerun()
