import streamlit as st

def render():
    st.header("Find Required Mask Size")
    st.markdown("---")
    hole_size_um = st.number_input("Target Via Diameter (µm)", 1.0, value=14.0, step=1.0)
    demag_factor = st.number_input("System Demagnification Factor (e.g., 60x)", 1.0, value=60.0, step=1.0)
    with st.expander("Show Formula"): st.latex(r'''\text{Mask Size (mm)} = \frac{\text{Target Via Diameter (µm)} \times \text{Demag. Factor}}{1000}''')
    if demag_factor > 0:
        required_mask_size_mm = (hole_size_um * demag_factor) / 1000
        st.markdown("---")
        st.markdown(f'<p class="results-header" style="color: #007aff;">Calculated Mask Size</p>', unsafe_allow_html=True)
        st.metric(label="Required Mask Diameter", value=f"{required_mask_size_mm:.3f} mm")