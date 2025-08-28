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

# --- FINAL, STABLE CSS (Includes Hover Animations) ---
st.markdown("""
<style>
    /* Main App Styling */
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    [data-testid="stSidebar"] { padding-top: 1.5rem; }

    /* Home Button Styling */
    [data-testid="stSidebar"] .stButton button[data-testid="stButton-Home"] {
        font-size: 1.5rem; font-weight: 700; text-align: left !important;
        background-color: transparent; color: #111827; border: none;
    }
    [data-testid="stSidebar"] .stButton button[data-testid="stButton-Home"]:hover {
        background-color: #F3F4F6; color: #ef4444;
    }

    /* Sidebar Expanders */
    [data-testid="stSidebar"] .stExpander {
        border: none !important; box-shadow: none !important;
    }
    [data-testid="stSidebar"] .stExpander summary {
        padding: 10px 15px; border-radius: 8px; font-weight: 500; font-size: 1rem;
    }
    
    /* Styling for the tool buttons to look like links */
    [data-testid="stSidebar"] .stButton button {
        text-align: left !important;
        font-weight: 500;
        padding: 10px 15px;
        border-radius: 8px;
        background-color: transparent;
        color: #374151;
        border: none;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #F3F4F6;
    }
    /* Style for the selected (primary) button */
    [data-testid="stSidebar"] .stButton button[kind="primary"] {
        background-color: #ef4444;
        color: white;
    }

    /* --- NEW: HOME PAGE CARD HOVER ANIMATION --- */
    /* This class will be applied to containers in home.py */
    .home-card {
        transition: all 0.2s ease-in-out;
    }
    .home-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# --- APP STATE AND NAVIGATION ---
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Home"


# --- PROFESSIONAL SVG ICONS DICTIONARY ---
TOOL_CATEGORIES = {
    "Core Workflow": {
        "Material Analyzer": {"module": material_analyzer, "svg": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path></svg>"""},
        "Process Recommender": {"module": process_recommender, "svg": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>"""},
        "Microvia Process Simulator": {"module": beam_profile_visualizer, "svg": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>"""},
    },
    "Advanced Analysis": {
        "Liu Plot Analyzer": {"module": liu_plot_analyzer, "svg": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>"""},
        "Thermal Effects Calculator": {"module": thermal_effects_calculator, "svg": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 4.5l-4-4L2 9.5l4 4 8.5-8.5z"></path><path d="M5.5 16.5l-4 4L10.5 22l4-4-8.5-8.5z"></path></svg>"""},
    },
    "Fundamental Calculators": {
        "Mask Finder": {"module": mask_finder, "svg": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line><line x1="15" y1="3" x2="15" y2="21"></line><line x1="3" y1="9" x2="21" y2="9"></line><line x1="3" y1="15" x2="21" y2="15"></line></svg>"""},
        "Pulse Energy": {"module": pulse_energy_calculator, "svg": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>"""},
        "Fluence (Energy Density)": {"module": fluence_calculator, "svg": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>"""},
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
                # Use st.markdown to render the icon and text
                st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 5px;">
                        {tool_details['svg']}
                        <span style="margin-left: 12px;">{tool_name}</span>
                    </div>
                """, unsafe_allow_html=True)
                # This button is now invisible but provides the click functionality
                if st.button(" ", use_container_width=True, key=tool_name, type="primary" if is_selected else "secondary"):
                    st.session_state.app_mode = tool_name
                    st.rerun()
    
    st.markdown("---")
    is_doc_selected = (st.session_state.app_mode == "Scientific Reference")
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
            <span style="margin-left: 12px;">Scientific Reference</span>
        </div>
    """, unsafe_allow_html=True)
    if st.button(" ", use_container_width=True, key="Scientific Reference", type="primary" if is_doc_selected else "secondary"):
        st.session_state.app_mode = "Scientific Reference"
        st.rerun()


# --- MAIN PANEL DISPATCHER ---
selected_module = home
if st.session_state.app_mode == "Scientific Reference":
    selected_module = documentation
elif st.session_state.app_mode != "Home":
    for category in TOOL_CATEGORIES.values():
        if st.session_state.app_mode in category:
            selected_module = category[st.session_state.app_mode]["module"]
            break

if selected_module:
    selected_module.render()
else:
    st.session_state.app_mode = "Home"
    st.rerun()
