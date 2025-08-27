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

# --- NEW, ROBUST CSS FOR SVG ICONS AND BUTTONS ---
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
    
    /* --- NEW CSS for Icon Links --- */
    /* We will now use Markdown links to create our buttons, which is more flexible */
    a.icon-button-link {
        display: flex;
        align-items: center;
        padding: 10px 15px;
        border-radius: 8px;
        text-decoration: none;
        color: #374151; /* Default text color */
        transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
        margin-bottom: 5px; /* Add some space between links */
    }
    a.icon-button-link:hover {
        background-color: #F3F4F6;
    }
    a.icon-button-link.selected {
        background-color: #ef4444; /* Your primary red color */
        color: white;
    }
    a.icon-button-link svg {
        width: 18px;
        height: 18px;
        margin-right: 12px;
        stroke-width: 2.5; /* Makes the icons look bold and clear */
        stroke: #6B7280; /* Default icon color */
        transition: stroke 0.2s ease-in-out;
    }
    a.icon-button-link.selected svg {
        stroke: white; /* Make the icon white when selected */
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# --- APP STATE AND NAVIGATION ---
# This logic is now simpler and more robust
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Home"

# Check URL query params to handle navigation from our new links
if "page_request" in st.query_params:
    st.session_state.app_mode = st.query_params["page_request"]


# --- NEW DICTIONARY WITH PROFESSIONAL SVG ICONS ---
TOOL_CATEGORIES = {
    "Core Workflow": {
        "Material Analyzer": {"module": material_analyzer, "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path></svg>"""},
        "Process Recommender": {"module": process_recommender, "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>"""},
        "Microvia Process Simulator": {"module": beam_profile_visualizer, "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>"""},
    },
    "Advanced Analysis": {
        "Liu Plot Analyzer": {"module": liu_plot_analyzer, "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>"""},
        "Thermal Effects Calculator": {"module": thermal_effects_calculator, "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M14.5 4.5c.3-.3.8-.3 1 0l6 6c.3.3.3.8 0 1l-6 6c-.3.3-.8.3-1 0l-6-6c-.3-.3-.3-.8 0-1l6-6z"></path><path d="M9.5 9.5c.3-.3.8-.3 1 0l6 6c.3.3.3.8 0 1l-6 6c-.3.3-.8.3-1 0l-6-6c-.3-.3-.3-.8 0-1l6-6z"></path></svg>"""},
    },
    "Fundamental Calculators": {
        "Mask Finder": {"module": mask_finder, "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line><line x1="15" y1="3" x2="15" y2="21"></line><line x1="3" y1="9" x2="21" y2="9"></line><line x1="3" y1="15" x2="21" y2="15"></line></svg>"""},
        "Pulse Energy": {"module": pulse_energy_calculator, "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>"""},
        "Fluence (Energy Density)": {"module": fluence_calculator, "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>"""},
    }
}


# --- SIDEBAR RENDERING ---
with st.sidebar:
    # Home button remains a stable st.button
    if st.button("Laser Dashboard", use_container_width=True, key="stButton-Home"):
        st.session_state.app_mode = "Home"
        st.query_params.clear() # Clear the URL when going home
        st.rerun()

    st.markdown("---")
    
    # --- NEW: We now build the navigation using styled Markdown links ---
    for category_name, tools in TOOL_CATEGORIES.items():
        with st.expander(category_name, expanded=True):
            for tool_name, tool_details in tools.items():
                is_selected = (st.session_state.app_mode == tool_name)
                # This markdown link structure is the key to making this work
                st.markdown(
                    f"""
                    <a href="?page_request={tool_name}" target="_self" class="icon-button-link {'selected' if is_selected else ''}">
                        {tool_details['svg']}
                        <span>{tool_name}</span>
                    </a>
                    """,
                    unsafe_allow_html=True
                )

# --- MAIN PANEL DISPATCHER ---
# This logic is now cleaner and defaults to home
selected_module = home
if st.session_state.app_mode != "Home":
    for category in TOOL_CATEGORIES.values():
        if st.session_state.app_mode in category:
            selected_module = category[st.session_state.app_mode]["module"]
            break

selected_module.render()
