import streamlit as st
import numpy as np

def render():
    st.header("Calculate Via Taper Angle")
    st.markdown("---")
    st.info("Predict the sidewall taper angle based on the material's energy penetration depth and the laser beam radius.")
    
    col1, col2 = st.columns(2)
    with col1:
        alpha_inv = st.number_input("Effective Penetration Depth (α⁻¹) (µm)", 
                                    min_value=0.01, value=1.0, step=0.1,
                                    help="This value is the 'slope' calculated in the 'Material Analyzer' for the fit: Ablation Rate = α⁻¹ * ln(F/F_th).")
        beam_diameter_um = st.number_input("Beam Spot Diameter (1/e²) (µm)", 
                                           min_value=1.0, value=25.0, step=1.0,
                                           help="The 1/e² diameter of the focused laser spot.")
    
    with st.expander("Understanding the Formula"):
        st.markdown("The half-taper angle (`θ`) is determined by the geometry of the beam interacting with the material's ablation characteristics.")
        st.latex(r'''\theta = \arctan\left(\frac{w_0}{\alpha^{-1}}\right)''')
        st.markdown(r"""
        Where:
        - $\theta$: Half-taper angle (angle from the vertical wall).
        - $w_0$: Beam radius (Diameter / 2).
        - $\alpha^{-1}$: The material's effective penetration depth. A smaller $\alpha^{-1}$ leads to a steeper, more vertical wall.
        """)

    if alpha_inv > 0 and beam_diameter_um > 0:
        w0_um = beam_diameter_um / 2
        theta_rad = np.arctan(w0_um / alpha_inv)
        theta_deg = np.rad2deg(theta_rad)
        full_angle_deg = 2 * theta_deg

        st.markdown("---")
        st.markdown(f'<p class="results-header" style="color: #007aff;">Calculated Taper Angle</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric(label="Half-Taper Angle (θ)", value=f"{theta_deg:.2f}°")
        c2.metric(label="Full Taper Angle (2θ)", value=f"{full_angle_deg:.2f}°")