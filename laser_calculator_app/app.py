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

# --- CUSTOM CSS FOR DUOTONE ICONS AND CLICKABLE LINKS ---
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
    [data-testid="stSidebar"] .stButton button[data-testid="stButton-Home"]:focus {
        box-shadow: none;
    }

    /* Sidebar Expanders */
    [data-testid="stSidebar"] .stExpander {
        border: none !important; box-shadow: none !important;
    }
    [data-testid="stSidebar"] .stExpander summary {
        padding: 10px 15px; border-radius: 8px; font-weight: 500; font-size: 1rem;
    }
    
    /* --- NEW, ROBUST STYLING FOR CUSTOM ICON LINKS --- */
    a.icon-button-link {
        display: flex;
        align-items: center;
        padding: 10px 15px;
        border-radius: 8px;
        text-decoration: none;
        color: #374151; /* Default text color */
        transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
        margin-bottom: 5px; /* Spacing between links */
    }
    a.icon-button-link:hover {
        background-color: #F3F4F6; /* Light gray hover */
    }
    a.icon-button-link.selected {
        background-color: #ef4444; /* Primary red color */
        color: white;
    }

    /* Duotone Icon Styling */
    a.icon-button-link svg {
        width: 20px;
        height: 20px;
        margin-right: 12px;
    }
    /* Default State Colors */
    a.icon-button-link svg .duotone-bg { fill: #E5E7EB; }
    a.icon-button-link svg .duotone-fg { fill: #4B5563; }

    /* Selected State Colors */
    a.icon-button-link.selected svg .duotone-bg { fill: #ef4444; opacity: 0.3; }
    a.icon-button-link.selected svg .duotone-fg { fill: #ef4444; }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# --- APP STATE AND NAVIGATION ---
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Home"

# The navigation logic is now driven by URL query parameters, which is a robust method.
if "page_request" in st.query_params:
    st.session_state.app_mode = st.query_params["page_request"]


# --- HIERARCHICAL MODULE DICTIONARY WITH DUOTONE ICONS ---
TOOL_CATEGORIES = {
    "Core Workflow": {
        "Material Analyzer": {"module": material_analyzer, "svg": """<svg viewBox="0 0 256 256"><rect width="256" height="256" fill="none"/><path class="duotone-bg" d="M128,24A104,104,0,1,0,232,128,104.1,104.1,0,0,0,128,24Z"/><path class="duotone-fg" d="M216,40.2A103.8,103.8,0,0,1,128,120V24a104.1,104.1,0,0,0,88,16.2Z"/></svg>"""},
        "Process Recommender": {"module": process_recommender, "svg": """<svg viewBox="0 0 256 256"><rect width="256" height="256" fill="none"/><path class="duotone-bg" d="M48,160V48a8,8,0,0,1,8-8H160"/><path class="duotone-fg" d="M216,96v96a8,8,0,0,1-8,8H88a8,8,0,0,1-8-8V96a8,8,0,0,1,8-8H208A8,8,0,0,1,216,96ZM160,40H56a8,8,0,0,0-8,8V160"/></svg>"""},
        "Microvia Process Simulator": {"module": beam_profile_visualizer, "svg": """<svg viewBox="0 0 256 256"><rect width="256" height="256" fill="none"/><circle class="duotone-bg" cx="128" cy="128" r="60"/><path class="duotone-fg" d="M128,216a88,88,0,1,0-88-88A88.1,88.1,0,0,0,128,216Zm0-128a40,40,0,1,0,40,40A40,40,0,0,0,128,88Z"/></svg>"""},
    },
    "Advanced Analysis": {
        "Liu Plot Analyzer": {"module": liu_plot_analyzer, "svg": """<svg viewBox="0 0 256 256"><rect width="256" height="256" fill="none"/><path class="duotone-bg" d="M24,184H224V72Z"/><path class="duotone-fg" d="M224,72,128,152,80,120,24,184Z"/></svg>"""},
        "Thermal Effects Calculator": {"module": thermal_effects_calculator, "svg": """<svg viewBox="0 0 256 256"><rect width="256" height="256" fill="none"/><path class="duotone-bg" d="M104,32h48a8,8,0,0,1,8,8v97.6a48,48,0,1,1-64,0V40A8,8,0,0,1,104,32Z"/><circle class="duotone-fg" cx="128" cy="184" r="28"/></svg>"""},
    },
    "Fundamental Calculators": {
        "Mask Finder": {"module": mask_finder, "svg": """<svg viewBox="0 0 256 256"><rect width="256" height="256" fill="none"/><path class="duotone-bg" d="M96,40V216"/><path class="duotone-fg" d="M216,40H40a8,8,0,0,0-8,8V208a8,8,0,0,0,8,8H216a8,8,0,0,0,8-8V48A8,8,0,0,0,216,40ZM96,216V40h64V216Z"/></svg>"""},
        "Pulse Energy": {"module": pulse_energy_calculator, "svg": """<svg viewBox="0 0 256 256"><rect width="256" height="256" fill="none"/><path class="duotone-bg" d="M96,24,32,152h80l-16,80L224,96H128Z"/></svg>"""},
        "Fluence (Energy Density)": {"module": fluence_calculator, "svg": """<svg viewBox="0 0 256 256"><rect width="256" height="256" fill="none"/><circle class="duotone-bg" cx="128" cy="128" r="44"/><path class="duotone-fg" d="M128,64V24m0,208v-40m64-64h40m-208,0H64m98.8-34.8L216,32m-120,4.7L44.7,88m126.6,83.3L216,224m-126.6-4.7L44.7,168M128,172a44,44,0,1,0-44-44A44,44,0,0,0,128,172Z"/></svg>"""},
    }
}
# Add the documentation module separately for clarity
TOOL_CATEGORIES["Scientific Reference"] = {"module": documentation, "svg": """<svg viewBox="0 0 256 256"><rect width="256" height="256" fill="none"/><path class="duotone-bg" d="M48.2,208a8,8,0,0,1-6.2-12.8L120,128,42,60.8a8,8,0,0,1,12.4-10.1l88,80a8,8,0,0,1,0,10.1l-88,80A8,8,0,0,1,48.2,208Z"/><path class="duotone-fg" d="M144,48a8,8,0,0,0,8,8h56a8,8,0,0,0,0-16H152A8,8,0,0,0,144,48Zm64,152H152a8,8,0,0,0,0,16h56a8,8,0,0,0,0-16Z"/></svg>"""}

# --- SIDEBAR RENDERING ---
with st.sidebar:
    if st.button("Laser Dashboard", use_container_width=True, key="stButton-Home"):
        st.session_state.app_mode = "Home"
        st.query_params.clear() # Clear the URL when going home
        st.rerun()

    st.markdown("---")
    
    for category_name, tools in TOOL_CATEGORIES.items():
        # Handle the special case for the single 'Scientific Reference' tool
        if not isinstance(tools, dict):
            continue

        with st.expander(category_name, expanded=True):
            for tool_name, tool_details in tools.items():
                is_selected = (st.session_state.app_mode == tool_name)
                # This markdown link is the key to a stable and beautiful navigation
                st.markdown(
                    f"""
                    <a href="?page_request={tool_name}" target="_self" class="icon-button-link {'selected' if is_selected else ''}">
                        {tool_details['svg']}
                        <span>{tool_name}</span>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
    
    st.markdown("---")
    # Render the Scientific Reference link separately at the bottom
    is_selected = (st.session_state.app_mode == "Scientific Reference")
    st.markdown(
        f"""
        <a href="?page_request=Scientific Reference" target="_self" class="icon-button-link {'selected' if is_selected else ''}">
            {TOOL_CATEGORIES['Scientific Reference']['svg']}
            <span>Scientific Reference</span>
        </a>
        """,
        unsafe_allow_html=True
    )


# --- MAIN PANEL DISPATCHER ---
selected_module = home # Default to home
if st.session_state.app_mode != "Home":
    if st.session_state.app_mode == "Scientific Reference":
        selected_module = documentation
    else:
        for category in TOOL_CATEGORIES.values():
            if isinstance(category, dict) and st.session_state.app_mode in category:
                selected_module = category[st.session_state.app_mode]["module"]
                break

if selected_module:
    selected_module.render()
else:
    # Safe fallback if something goes wrong
    st.session_state.app_mode = "Home"
    st.query_params.clear()
    st.rerun()
