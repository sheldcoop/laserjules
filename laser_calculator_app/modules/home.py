import streamlit as st

def render():
    # This dictionary defines the content for the pop-up dialogs.
    TOOL_INFO = {
        "Material Analyzer": {
            "title": "Launch Material Analyzer",
            "description": "Start by analyzing your experimental data to determine your material's fundamental properties: the **Ablation Threshold** and **Effective Penetration Depth**.",
            "what_you_need": "A set of corresponding Fluence (J/cm²) and measured Depth (µm) data points."
        },
        "Process Recommender": {
            "title": "Launch Process Recommender",
            "description": "Use your material properties and process goals to calculate a recommended starting recipe, including the required **Pulse Energy** and **Number of Shots**.",
            "what_you_need": "The Ablation Threshold and Penetration Depth from the Material Analyzer, along with your target via dimensions."
        },
        "Microvia Process Simulator": {
            "title": "Launch Microvia Process Simulator",
            "description": "Load your recipe into the interactive simulator to visualize the predicted microvia geometry, including **Top/Bottom Diameters** and **Taper Angle**.",
            "what_you_need": "A complete recipe, including Pulse Energy, Beam Diameter, and Material Properties."
        }
    }

    # --- MAIN HOME PAGE UI ---
    st.title("Welcome to the Advanced Laser Process Calculator")
    st.markdown(
        "An integrated suite of tools for laser micro-machining process development and simulation. "
        "Follow the recommended workflow below or select a specific tool from the sidebar to begin."
    )
    st.markdown("---")

    # --- RECOMMENDED WORKFLOW SECTION ---
    st.header("Recommended Workflow")
    col1, col2, col3 = st.columns(3, gap="large")
    workflow_keys = ["Material Analyzer", "Process Recommender", "Microvia Process Simulator"]
    workflow_steps = ["Step 1: Characterize Material", "Step 2: Generate a Recipe", "Step 3: Simulate & Visualize"]
    
    for i, col in enumerate([col1, col2, col3]):
        tool_key = workflow_keys[i]
        with col:
            # Add the CSS class for the hover animation
            with st.container(border=True, class_name="home-card"):
                st.markdown(f"<h5>{workflow_steps[i]}</h5>", unsafe_allow_html=True)
                st.markdown(TOOL_INFO[tool_key]["description"])
                
                # Corrected navigation logic
                if st.button(f"Go to {tool_key}", use_container_width=True, key=f"workflow_{tool_key}"):
                    # For workflow tools, we show the pop-up dialog
                    st.session_state.show_dialog = tool_key
                    st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # --- DIRECT TOOL ACCESS & RESOURCES SECTION ---
    st.header("Direct Tool Access & Resources")
    colA, colB, colC = st.columns(3, gap="large")
    
    with colA:
        with st.container(border=True, class_name="home-card"):
            st.markdown("<h5>Advanced Analysis Tools</h5>", unsafe_allow_html=True)
            for tool in ["Liu Plot Analyzer", "Thermal Effects Calculator"]:
                # Corrected navigation logic
                if st.button(tool, use_container_width=True, key=f"direct_{tool}"):
                    st.session_state.app_mode = tool
                    st.rerun()
                
    with colB:
        with st.container(border=True, class_name="home-card"):
            st.markdown("<h5>Fundamental Calculators</h5>", unsafe_allow_html=True)
            for tool in ["Mask Finder", "Pulse Energy", "Fluence (Energy Density)"]:
                # Corrected navigation logic
                if st.button(tool, use_container_width=True, key=f"direct_{tool}"):
                    st.session_state.app_mode = tool
                    st.rerun()

    with colC:
        with st.container(border=True, class_name="home-card"):
            st.markdown("<h5>🔬 Scientific Reference</h5>", unsafe_allow_html=True)
            st.markdown("Understand the core physics, models, and formulas used in this dashboard.")
            # Corrected navigation logic
            if st.button("Read the Documentation", use_container_width=True):
                st.session_state.app_mode = "Scientific Reference"
                st.rerun()

    # --- DIALOG (POP-UP) LOGIC ---
    # This logic is now correctly triggered by the workflow buttons
    if "show_dialog" in st.session_state and st.session_state.show_dialog:
        tool_key = st.session_state.show_dialog
        tool_info = TOOL_INFO.get(tool_key)

        if tool_info:
            @st.dialog(tool_info["title"])
            def show_tool_dialog():
                st.info(tool_info["description"])
                st.warning(f"**What you'll need:** {tool_info['what_you_need']}")
                
                d_col1, d_col2 = st.columns([1, 1])
                with d_col1:
                    if st.button("Continue to Tool", use_container_width=True, type="primary"):
                        st.session_state.app_mode = tool_key
                        del st.session_state.show_dialog
                        st.rerun()
                with d_col2:
                    if st.button("Cancel", use_container_width=True):
                        del st.session_state.show_dialog
                        st.rerun()

            show_tool_dialog()
