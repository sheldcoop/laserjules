import streamlit as st

def render():
    # This dictionary holds the information for our pop-up dialogs.
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

    # --- DIALOG (POP-UP) LOGIC ---
    # This block now checks if we need to show our custom dialog.
    if "show_dialog" in st.session_state and st.session_state.show_dialog:
        tool_key = st.session_state.show_dialog
        tool_info = TOOL_INFO.get(tool_key)

        if tool_info:
            # Create a container to act as our dialog box.
            with st.container(border=True):
                st.subheader(tool_info["title"])
                st.info(tool_info["description"])
                st.warning(f"**What you'll need:** {tool_info['what_you_need']}")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Continue to Tool", use_container_width=True, type="primary"):
                        st.session_state.app_mode = tool_key
                        del st.session_state.show_dialog # Close the dialog
                        st.rerun()
                with col2:
                    if st.button("Cancel", use_container_width=True):
                        del st.session_state.show_dialog # Close the dialog
                        st.rerun()
        return # Stop rendering the rest of the home page

    # --- MAIN HOME PAGE UI ---
    # This section will only run if the dialog is not being shown.
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
            with st.container(border=True):
                st.markdown(f"<h5>{workflow_steps[i]}</h5>", unsafe_allow_html=True)
                st.markdown(TOOL_INFO[tool_key]["description"])
                if st.button(f"Go to {tool_key}", use_container_width=True, key=f"workflow_{tool_key}"):
                    # When this button is clicked, we set the session state to show the dialog on the next rerun.
                    st.session_state.show_dialog = tool_key
                    st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # --- DIRECT TOOL ACCESS SECTION ---
    st.header("Direct Tool Access")
    colA, colB = st.columns(2, gap="large")
    
    with colA:
        with st.container(border=True):
            st.markdown("<h5>Advanced Analysis Tools</h5>", unsafe_allow_html=True)
            for tool in ["Liu Plot Analyzer", "Thermal Effects Calculator"]:
                if st.button(tool, use_container_width=True, key=f"direct_{tool}"):
                    st.session_state.app_mode = tool
                    st.rerun()
                
    with colB:
        with st.container(border=True):
            st.markdown("<h5>Fundamental Calculators</h5>", unsafe_allow_html=True)
            for tool in ["Pulse Energy", "Fluence (Energy Density)", "Mask Finder"]:
                if st.button(tool, use_container_width=True, key=f"direct_{tool}"):
                    st.session_state.app_mode = tool
                    st.rerun()