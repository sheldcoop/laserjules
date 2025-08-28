import streamlit as st

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
# Your existing CSS is good, we will just add the hover effects later.
st.markdown("""
<style>
    /* ... Your existing stable CSS ... */
</style>
""", unsafe_allow_html=True)


# --- APP STATE AND NAVIGATION ---
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Home"

# --- HIERARCHICAL MODULE & ICON DICTIONARY ---
# This structure is correct.
TOOL_CATEGORIES = {
    "Core Workflow": {
        "Material Analyzer": {"module": material_analyzer, "icon": "🔬"},
        "Process Recommender": {"module": process_recommender, "icon": "🧪"},
        "Microvia Process Simulator": {"module": beam_profile_visualizer, "icon": "🎯"},
    },
    "Advanced Analysis": {
        "Liu Plot Analyzer": {"module": liu_plot_analyzer, "icon": "📈"},
        "Thermal Effects Calculator": {"module": thermal_effects_calculator, "icon": "🔥"},
    },
    "Fundamental Calculators": {
        "Mask Finder": {"module": mask_finder, "icon": "🔳"},
        "Pulse Energy": {"module": pulse_energy_calculator, "icon": "⚡"},
        "Fluence (Energy Density)": {"module": fluence_calculator, "icon": "☀️"},
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
            for tool_name, tool_details in tools.items():
                is_selected = (st.session_state.app_mode == tool_name)
                icon = tool_details["icon"]
                label = f"{icon} {tool_name}"
                
                if st.button(label, use_container_width=True, type="primary" if is_selected else "secondary"):
                    st.session_state.app_mode = tool_name
                    st.rerun()
    
    st.markdown("---")
    doc_btn_type = "primary" if st.session_state.app_mode == "Scientific Reference" else "secondary"
    if st.button("🔬 Scientific Reference", use_container_width=True, type=doc_btn_type):
        st.session_state.app_mode = "Scientific Reference"
        st.rerun()


# --- MAIN PANEL DISPATCHER (THIS IS THE CORRECTED LOGIC) ---
selected_module = None

if st.session_state.app_mode == "Home":
    selected_module = home
elif st.session_state.app_mode == "Scientific Reference":
    selected_module = documentation
else:
    # Iterate through all categories to find the selected tool
    for category in TOOL_CATEGORIES.values():
        if st.session_state.app_mode in category:
            # --- THIS IS THE FIX ---
            # We correctly access the module from the nested dictionary
            selected_module = category[st.session_state.app_mode]["module"]
            break

# Render the found module
if selected_module:
    selected_module.render()
else:
    # Safe fallback if something goes wrong
    st.session_state.app_mode = "Home"
    st.rerun()
