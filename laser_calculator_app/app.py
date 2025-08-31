import streamlit as st

# Import the UI modules
from modules import pulse_energy_calculator, fluence_calculator, material_analyzer

# --- PAGE CONFIGURATION ---
st.set_page_config(
    layout="wide",
    page_title="Laser Calculator",
    initial_sidebar_state="expanded"
)

# --- APP STATE AND NAVIGATION ---
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Home"

# --- TOOL DICTIONARY ---
TOOLS = {
    "Pulse Energy Calculator": pulse_energy_calculator,
    "Fluence Calculator": fluence_calculator,
    "Material Analyzer": material_analyzer,
}

# --- SIDEBAR RENDERING ---
with st.sidebar:
    st.title("Laser Calculator")
    st.markdown("---")
    
    # Home button
    if st.button("Home"):
        st.session_state.app_mode = "Home"
        st.rerun()

    st.markdown("---")

    # Tool selection
    for tool_name in TOOLS.keys():
        if st.button(tool_name):
            st.session_state.app_mode = tool_name
            st.rerun()

# --- MAIN PANEL DISPATCHER ---
if st.session_state.app_mode == "Home":
    st.header("Welcome to the Laser Calculator!")
    st.markdown("""
    This application provides a suite of calculators for laser processing applications.
    Select a tool from the sidebar to get started.
    """)
elif st.session_state.app_mode in TOOLS:
    selected_tool = TOOLS[st.session_state.app_mode]
    selected_tool.render()
else:
    st.session_state.app_mode = "Home"
    st.rerun()
