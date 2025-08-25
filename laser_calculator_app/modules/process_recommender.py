import streamlit as st
import numpy as np
import pandas as pd
from utils import UM_TO_CM, UJ_TO_J

def render():
    st.header("Generate a Process Recipe")
    st.markdown("---"); st.info("Input your goal and material properties to generate a recommended starting recipe.")
    col1, col2, col3 = st.columns(3)
    with col1: 
        st.subheader("🎯 Your Goal")
        target_via_um = st.number_input("Target Via Diameter (µm)", 1.0, value=12.0, step=1.0)
        material_thickness_um = st.number_input("Material Thickness (µm)", 1.0, value=25.0, step=1.0)
    with col2: 
        st.subheader("🔬 Material Properties")
        st.caption("_(Use the 'Material Analyzer' to find these values)_")
        optimal_fluence = st.number_input("Optimal Peak Fluence (J/cm²)", 0.1, value=2.0, format="%.3f", step=0.1)
        ablation_rate = st.number_input("Ablation Rate @ Optimal Fluence (µm/pulse)", 0.01, value=0.9, format="%.3f", step=0.01)
    with col3: 
        st.subheader("⚙️ Machine Settings")
        beam_spot_um = st.number_input("Beam Spot Diameter (1/e²) (µm)", 1.0, value=15.0, step=1.0)
        rep_rate_khz = st.number_input("Repetition Rate (kHz)", 1.0, value=50.0, step=1.0)
        
    if st.button("Generate Recipe", type="primary", use_container_width=True):
        with st.spinner("Calculating recipe..."):
            radius_cm = (beam_spot_um / 2) * UM_TO_CM
            area_cm2 = np.pi * (radius_cm ** 2)
            required_energy_J = (optimal_fluence * area_cm2) / 2 # Peak fluence formula F = 2E/A
            required_energy_uJ = required_energy_J / UJ_TO_J
            required_shots = np.ceil(material_thickness_um / ablation_rate)
            required_power_mW = required_energy_uJ * rep_rate_khz
            st.session_state.recipe = {
                "Target Via Diameter (µm)": target_via_um, "Beam Spot Diameter (µm)": beam_spot_um, "Repetition Rate (kHz)": rep_rate_khz,
                "Material Thickness (µm)": material_thickness_um, "Optimal Peak Fluence (J/cm²)": optimal_fluence, 
                "Required Pulse Energy (µJ)": required_energy_uJ, "Required Average Power (mW)": required_power_mW,
                "Required Number of Shots": int(required_shots)
            }

    if st.session_state.app_mode == "Process Recommender" and st.session_state.get('recipe'):
        st.markdown("---"); st.markdown(f'<p class="results-header">Recommended Process Recipe</p>', unsafe_allow_html=True)
        recipe = st.session_state.recipe
        col1, col2, col3 = st.columns(3)
        col1.metric("Required Pulse Energy", f"{recipe['Required Pulse Energy (µJ)']:.3f} µJ")
        col2.metric("Required Average Power", f"{recipe['Required Average Power (mW)']:.1f} mW")
        col3.metric("Required Number of Shots", f"{recipe['Required Number of Shots']} pulses")
        st.subheader("Complete Recipe Summary")
        recipe_df = pd.DataFrame.from_dict({k: f"{v:.3f}" if isinstance(v, float) else str(v) for k, v in recipe.items()}, orient='index', columns=['Value'])
        st.table(recipe_df)