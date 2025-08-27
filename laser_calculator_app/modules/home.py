import streamlit as st

def render():
    # --- Inject CSS specific to this page for the cards ---
    st.markdown("""
        <style>
            .home-card {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                padding: 1.5rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.04);
                transition: all 0.2s ease-in-out;
                height: 100%; /* Ensure cards in a row have same height */
            }
            .home-card:hover {
                box-shadow: 0 10px 15px rgba(0,0,0,0.08);
                transform: translateY(-3px);
            }
        </style>
    """, unsafe_allow_html=True)

    # ... (Your TOOL_INFO dictionary here) ...
    TOOL_INFO = {
        "Material Analyzer": {
            "description": "Start by analyzing your experimental data to determine your material's fundamental properties: the **Ablation Threshold** and **Effective Penetration Depth**."
        },
        "Process Recommender": {
            "description": "Use your material properties and process goals to calculate a recommended starting recipe, including the required **Pulse Energy** and **Number of Shots**."
        },
        "Microvia Process Simulator": {
            "description": "Load your recipe into the interactive simulator to visualize the predicted microvia geometry, including **Top/Bottom Diameters** and **Taper Angle**."
        }
    }

    st.title("Welcome to the Advanced Laser Process Calculator")
    st.markdown(...) # Your markdown intro

    # --- RECOMMENDED WORKFLOW WITH CARD STYLING ---
    st.header("Recommended Workflow")
    st.markdown(
        """
        <div class="row">
            <div class="col-md-4">
                <div class="home-card">
                    <h5>Step 1: Characterize Material</h5>
                    <p>Start by analyzing your experimental data...</p>
                    # You'll need to embed the button logic within this HTML structure
                    # This part is more complex, let's simplify for now
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True
    )
    # The pure HTML/CSS injection for cards is complex with Streamlit buttons.
    # Let's use a simpler, more robust method with st.container and a border.
    
    col1, col2, col3 = st.columns(3, gap="large")
    workflow_keys = ["Material Analyzer", "Process Recommender", "Microvia Process Simulator"]
    workflow_steps = ["Step 1: Characterize Material", "Step 2: Generate a Recipe", "Step 3: Simulate & Visualize"]
    
    for i, col in enumerate([col1, col2, col3]):
        tool_key = workflow_keys[i]
        with col:
            # Using st.container with a border is a simpler way to achieve a "card" look
            with st.container(border=True):
                st.markdown(f"<h5>{workflow_steps[i]}</h5>", unsafe_allow_html=True)
                st.markdown(TOOL_INFO[tool_key]["description"])
                if st.button(f"Go to {tool_key}", use_container_width=True, key=f"workflow_{tool_key}"):
                    st.session_state.app_mode = tool_key
                    st.rerun()

    # --- DIRECT TOOL ACCESS WITH CARD STYLING ---
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
            for tool in ["Mask Finder", "Pulse Energy", "Fluence (Energy Density)"]:
                if st.button(tool, use_container_width=True, key=f"direct_{tool}"):
                    st.session_state.app_mode = tool
                    st.rerun()
