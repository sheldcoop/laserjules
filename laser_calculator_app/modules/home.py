import streamlit as st

def render():
    # --- A dictionary to store the information for our pop-ups ---
    TOOL_INFO = {
        "Material Analyzer": {
            "title": "Launch Material Analyzer",
            "description": "This tool characterizes your material by fitting a line to your experimental data. It calculates the two most important properties for laser processing.",
            "what_you_need": "You will need a set of corresponding Fluence (J/cm²) and measured Depth (µm) data points."
        },
        "Process Recommender": {
            "title": "Launch Process Recommender",
            "description": "This tool calculates a starting recipe based on your material properties and process goals.",
            "what_you_need": "You will need the Ablation Threshold and Ablation Rate from the Material Analyzer, along with your target via dimensions."
        },
        "Beam Profile Visualizer": {
            "title": "Launch Microvia Process Simulator",
            "description": "This tool provides an interactive simulation to visualize the final microvia geometry based on a full set of process parameters.",
            "what_you_need": "A complete recipe, including Pulse Energy, Beam Diameter, and Material Properties."
        }
    }

    # --- HEADER ---
    st.title("Welcome to the Advanced Laser Process Calculator")
    st.markdown(
        "An integrated suite of tools for laser micro-machining process development and simulation. "
        "Follow the recommended workflow below or select a specific tool from the sidebar to begin."
    )
    st.markdown("---")

    # --- RECOMMENDED WORKFLOW SECTION ---
    st.header("Recommended Workflow")
    
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        with st.container(border=True):
            st.markdown("<h5>Step 1: Characterize Material</h5>", unsafe_allow_html=True)
            st.markdown(
                "Start by analyzing your experimental data to determine your material's "
                "fundamental properties: the **Ablation Threshold** and **Effective Penetration Depth**."
            )
            if st.button("Go to Material Analyzer", use_container_width=True):
                st.session_state.show_dialog = "Material Analyzer"

    with col2:
        with st.container(border=True):
            st.markdown("<h5>Step 2: Generate a Recipe</h5>", unsafe_allow_html=True)
            st.markdown(
                "Use your material properties and process goals to calculate a recommended "
                "starting recipe, including the required **Pulse Energy** and **Number of Shots**."
            )
            if st.button("Go to Process Recommender", use_container_width=True):
                st.session_state.show_dialog = "Process Recommender"

    with col3:
        with st.container(border=True):
            st.markdown("<h5>Step 3: Simulate & Visualize</h5>", unsafe_allow_html=True)
            st.markdown(
                "Load your recipe into the interactive simulator to visualize the predicted microvia "
                "geometry, including **Top/Bottom Diameters** and **Taper Angle**."
            )
            if st.button("Go to Beam Profile Visualizer", use_container_width=True):
                st.session_state.show_dialog = "Beam Profile Visualizer"
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # --- DIRECT TOOL ACCESS SECTION ---
    # THIS FUNCTION IS NOW CORRECT
    def set_app_mode(mode_name):
        st.session_state.app_mode = mode_name
        st.rerun() # <-- This line fixes the navigation

    st.header("Direct Tool Access")
    colA, colB = st.columns(2, gap="large")
    with colA:
        with st.container(border=True):
            st.markdown("<h5>Advanced Analysis Tools</h5>", unsafe_allow_html=True)
            st.button("Liu Plot Analyzer", on_click=set_app_mode, args=("Liu Plot Analyzer",), use_container_width=True)
            st.button("Thermal Effects Calculator", on_click=set_app_mode, args=("Thermal Effects Calculator",), use_container_width=True)
    with colB:
        with st.container(border=True):
            st.markdown("<h5>Fundamental Calculators</h5>", unsafe_allow_html=True)
            st.button("Pulse Energy", on_click=set_app_mode, args=("Pulse Energy",), use_container_width=True)
            st.button("Fluence (Energy Density)", on_click=set_app_mode, args=("Fluence (Energy Density)",), use_container_width=True)
            st.button("Mask Finder", on_click=set_app_mode, args=("Mask Finder",), use_container_width=True)


    # --- DIALOG (POP-UP) LOGIC ---
    if "show_dialog" in st.session_state and st.session_state.show_dialog:
        tool_key = st.session_state.show_dialog
        tool_info = TOOL_INFO.get(tool_key)

        if tool_info:
            @st.dialog(tool_info["title"])
            def show_tool_dialog():
                st.info(tool_info["description"])
                st.warning(f"**What you'll need:** {tool_info['what_you_need']}")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Continue to Tool", use_container_width=True, type="primary"):
                        st.session_state.app_mode = tool_key
                        del st.session_state.show_dialog
                        st.rerun()
                with col2:
                    if st.button("Cancel", use_container_width=True):
                        del st.session_state.show_dialog
                        st.rerun()

            show_tool_dialog()