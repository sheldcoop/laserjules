import streamlit as st

def render():
    # ... (Your TOOL_INFO dictionary and dialog logic remain here, unchanged) ...
    TOOL_INFO = {
        "Material Analyzer": {
            "title": "Launch Material Analyzer",
            "description": "Start by analyzing your experimental data...",
            "what_you_need": "A set of corresponding Fluence (J/cm²) and measured Depth (µm) data points."
        },
        "Process Recommender": {
            "title": "Launch Process Recommender",
            "description": "Use your material properties and process goals...",
            "what_you_need": "The Ablation Threshold and Penetration Depth..."
        },
        "Microvia Process Simulator": {
            "title": "Launch Microvia Process Simulator",
            "description": "Load your recipe into the interactive simulator...",
            "what_you_need": "A complete recipe, including Pulse Energy..."
        }
    }

    # --- MAIN HOME PAGE UI ---
    st.title("Welcome to the Advanced Laser Process Calculator")
    st.markdown(...) # Your intro markdown

    st.header("Recommended Workflow")
    col1, col2, col3 = st.columns(3, gap="large")
    workflow_keys = ["Material Analyzer", "Process Recommender", "Microvia Process Simulator"]
    workflow_steps = ["Step 1: Characterize Material", "Step 2: Generate a Recipe", "Step 3: Simulate & Visualize"]
    
    for i, col in enumerate([col1, col2, col3]):
        tool_key = workflow_keys[i]
        with col:
            # --- THIS IS THE FIX: We wrap the container in a div ---
            st.markdown('<div class="home-card">', unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown(f"<h5>{workflow_steps[i]}</h5>", unsafe_allow_html=True)
                st.markdown(TOOL_INFO[tool_key]["description"])
                if st.button(f"Go to {tool_key}", use_container_width=True, key=f"workflow_{tool_key}"):
                    st.session_state.show_dialog = tool_key
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.header("Direct Tool Access & Resources")
    colA, colB, colC = st.columns(3, gap="large")
    
    with colA:
        st.markdown('<div class="home-card">', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h5>Advanced Analysis Tools</h5>", unsafe_allow_html=True)
            for tool in ["Liu Plot Analyzer", "Thermal Effects Calculator"]:
                if st.button(tool, use_container_width=True, key=f"direct_{tool}"):
                    st.session_state.app_mode = tool
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
                
    with colB:
        st.markdown('<div class="home-card">', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h5>Fundamental Calculators</h5>", unsafe_allow_html=True)
            for tool in ["Mask Finder", "Pulse Energy", "Fluence (Energy Density)"]:
                if st.button(tool, use_container_width=True, key=f"direct_{tool}"):
                    st.session_state.app_mode = tool
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with colC:
        st.markdown('<div class="home-card">', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h5>🔬 Scientific Reference</h5>", unsafe_allow_html=True)
            st.markdown("Understand the core physics, models, and formulas used in this dashboard.")
            if st.button("Read the Documentation", use_container_width=True):
                st.session_state.app_mode = "Scientific Reference"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- DIALOG (POP-UP) LOGIC ---
    # This logic is correct and does not need to change.
    if "show_dialog" in st.session_state and st.session_state.show_dialog:
        # ... (your existing dialog code)
        pass
