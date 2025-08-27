import streamlit as st

def render():
    st.header("Find Required Mask Size")
    st.markdown("---")

    # --- MAIN TWO-COLUMN LAYOUT ---
    col_inputs, col_outputs = st.columns([2, 3], gap="large")

    # --- LEFT COLUMN: THE CONTROL PANEL ---
    with col_inputs:
        st.subheader("Control Panel")
        
        with st.container(border=True):
            hole_size_um = st.number_input("Target Via Diameter (µm)", min_value=0.1, value=14.0, step=1.0)
            demag_factor = st.number_input("System Demagnification Factor (e.g., 60x)", min_value=0.1, value=60.0, step=1.0)
            
            with st.expander("Show Formula"):
                st.latex(r'''\text{Mask Size (mm)} = \frac{\text{Target Via Diameter (µm)} \times \text{Demag. Factor}}{1000}''')

            # The calculate button is now part of the control panel
            calculate_button = st.button("Calculate Mask Size", type="primary", use_container_width=True)

    # --- RIGHT COLUMN: THE RESULTS CANVAS ---
    with col_outputs:
        st.subheader("Results Canvas")
        
        with st.container(border=True, height=250):
            # We use session state to remember the last result
            if calculate_button:
                if demag_factor > 0:
                    required_mask_size_mm = (hole_size_um * demag_factor) / 1000
                    st.session_state.mask_finder_result = required_mask_size_mm
                else:
                    st.session_state.mask_finder_result = None

            if 'mask_finder_result' in st.session_state and st.session_state.mask_finder_result is not None:
                st.markdown("<h6>Calculated Mask Size</h6>", unsafe_allow_html=True)
                st.metric(label="Required Mask Diameter", value=f"{st.session_state.mask_finder_result:.3f} mm")
            else:
                st.info("Your calculated mask size will appear here.")
