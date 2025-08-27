import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils import UM_TO_CM, UJ_TO_J

# ======================================================================================
# MASTER RENDER FUNCTION
# ======================================================================================
def render():
    st.markdown("### Microvia Process Simulator")
    st.info("Interactively simulate a laser drilling process or generate a starting recipe for a specific goal.")
    st.markdown("---")

    col_inputs, col_outputs = st.columns([2, 3], gap="large")

    with col_inputs:
        st.subheader("Control Panel")
        params = render_inputs()

    with col_outputs:
        st.subheader("Results Canvas")
        render_outputs(params)

# ======================================================================================
# INPUT RENDERING FUNCTIONS (These are already perfect)
# ======================================================================================
def render_inputs():
    # ... (Your render_inputs function is correct and does not need to be changed) ...
    if st.session_state.get("switch_to_simulator", False):
        st.session_state.simulator_mode = "Interactive Simulator"
        st.session_state.switch_to_simulator = False
    
    mode_options = ["Interactive Simulator", "Recipe Goal Seeker"]
    current_mode_index = mode_options.index(st.session_state.get("simulator_mode", "Interactive Simulator"))
    calc_mode = st.radio(
        "Select Mode", options=mode_options, index=current_mode_index, 
        key="simulator_mode", horizontal=True
    )

    if calc_mode == "Interactive Simulator":
        # Clear any old goal seeker results when switching modes
        if "goal_seeker_results" in st.session_state:
            del st.session_state.goal_seeker_results
        return render_interactive_simulator_inputs()
    else:
        return render_goal_seeker_inputs()

def render_interactive_simulator_inputs():
    # ... (This function is correct and does not need to be changed) ...
    params = st.session_state.get("sim_params", {})
    p = {}

    with st.container(border=True):
        st.markdown("<h5>Laser Parameters</h5>", unsafe_allow_html=True)
        p["beam_profile"] = st.selectbox("Beam Profile", ["Gaussian", "Top-Hat"])
        c1, c2 = st.columns([3, 1])
        with c1: pe_slider = st.slider("Pulse Energy (µJ)", 0.1, 50.0, float(params.get("pulse_energy", 10.0)), 0.1, key="pe_sl")
        with c2: p["pulse_energy_uJ"] = st.number_input("PE", value=pe_slider, label_visibility="collapsed", key="pe_num")
        with c1: bd_slider = st.slider("Beam Spot Diameter (µm)", 5.0, 50.0, float(params.get("beam_diameter", 25.0)), 0.5, key="bd_sl")
        with c2: p["beam_diameter_um"] = st.number_input("BD", value=bd_slider, label_visibility="collapsed", key="bd_num")

    with st.container(border=True):
        st.markdown("<h5>Material Properties</h5>", unsafe_allow_html=True)
        c1, c2 = st.columns([3, 1])
        with c1: at_slider = st.slider("Ablation Threshold (J/cm²)", 0.1, 10.0, float(params.get("ablation_threshold", 1.0)), 0.1, key="at_sl")
        with c2: p["ablation_threshold_j_cm2"] = st.number_input("AT", value=at_slider, label_visibility="collapsed", key="at_num")
        with c1: ai_slider = st.slider("Penetration Depth (α⁻¹) (µm)", 0.1, 5.0, float(params.get("alpha_inv", 0.5)), 0.05, key="ai_sl")
        with c2: p["alpha_inv"] = st.number_input("AI", value=ai_slider, label_visibility="collapsed", key="ai_num")

    with st.container(border=True):
        st.markdown("<h5>Process Goal</h5>", unsafe_allow_html=True)
        c1, c2 = st.columns([3, 1])
        with c1: ns_slider = st.slider("Number of Shots", 1, 300, int(params.get("number_of_shots", 75)), key="ns_sl")
        with c2: p["number_of_shots"] = st.number_input("NS", value=ns_slider, label_visibility="collapsed", key="ns_num")
        p["material_thickness"] = st.number_input("Material Thickness (µm)", 1.0, 200.0, float(params.get("material_thickness", 50.0)), key="mt_num")
    
    return p

def render_goal_seeker_inputs():
    # ... (This function is correct and does not need to be changed) ...
    p = {}
    with st.container(border=True):
        st.markdown("<h5>🎯 Desired Via</h5>", unsafe_allow_html=True)
        p["target_diameter_um"] = st.number_input("Target Top Diameter (µm)", 1.0, 100.0, 25.0, 0.1)
        p["material_thickness"] = st.number_input("Material Thickness (µm)", 1.0, 200.0, 40.0, 1.0)
        p["overkill_shots"] = st.number_input("Overkill Shots", 0, 100, 10)

    with st.container(border=True):
        st.markdown("<h5>⚙️ Machine Constraints</h5>", unsafe_allow_html=True)
        p["beam_diameter_um"] = st.number_input("Beam Spot Diameter (µm)", 1.0, 100.0, 30.0, 0.5)

    with st.container(border=True):
        st.markdown("<h5>🔬 Material Properties</h5>", unsafe_allow_html=True)
        p["ablation_threshold_j_cm2"] = st.number_input("Ablation Threshold (J/cm²)", 0.01, 20.0, 0.9, 0.01)
        p["alpha_inv"] = st.number_input("Penetration Depth (α⁻¹) (µm)", 0.01, 10.0, 0.8, 0.01)

    p["generate_button"] = st.button("Generate Recipe", type="primary", use_container_width=True)
    return p

# ======================================================================================
# OUTPUT RENDERING FUNCTIONS
# ======================================================================================
def render_outputs(params):
    # ... (This function is correct and does not need to be changed) ...
    if st.session_state.simulator_mode == "Interactive Simulator":
        render_interactive_simulator_results(params)
    else:
        render_goal_seeker_results(params)

def render_interactive_simulator_results(p):
    # ... (This function is correct and does not need to be changed) ...
    # ... (All your existing simulator calculation and plotting code goes here) ...
    
# --- THIS IS THE CORRECTED GOAL SEEKER RESULTS FUNCTION ---
def render_goal_seeker_results(p):
    # --- FIX 1: If generate button is clicked, perform calculation AND SAVE the results ---
    if p.get("generate_button"):
        with st.spinner("Calculating recipe..."):
            w0_cm = (p["beam_diameter_um"] / 2.0) * UM_TO_CM
            d_cm = p["target_diameter_um"] * UM_TO_CM
            required_peak_fluence = p["ablation_threshold_j_cm2"] * np.exp((d_cm**2) / (2 * w0_cm**2)) if w0_cm > 0 else 0
            required_energy_J = (required_peak_fluence * np.pi * w0_cm**2) / 2.0
            pulse_energy_uJ = required_energy_J / UJ_TO_J
            max_depth_per_pulse = p["alpha_inv"] * np.log(required_peak_fluence / p["ablation_threshold_j_cm2"]) if required_peak_fluence > p["ablation_threshold_j_cm2"] else 0
            
            if max_depth_per_pulse > 0:
                min_shots = int(np.ceil(p["material_thickness"] / max_depth_per_pulse))
                number_of_shots = min_shots + p["overkill_shots"]
            else: 
                number_of_shots = 0
            
            # Save the results to the session state so they persist across reruns
            st.session_state.goal_seeker_results = {
                "pulse_energy_uJ": pulse_energy_uJ,
                "number_of_shots": number_of_shots,
                "beam_diameter_um": p["beam_diameter_um"],
                "ablation_threshold_j_cm2": p["ablation_threshold_j_cm2"],
                "alpha_inv": p["alpha_inv"],
                "material_thickness": p["material_thickness"]
            }

    # --- FIX 2: Check if saved results exist, and if so, display them ---
    if "goal_seeker_results" in st.session_state:
        results = st.session_state.goal_seeker_results
        
        st.markdown("<h5>Recommended Recipe</h5>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("Required Pulse Energy", f"{results['pulse_energy_uJ']:.3f} µJ")
        c2.metric("Required Number of Shots", f"{int(results['number_of_shots'])} shots")
        
        st.markdown("---")
        st.markdown("<h5>Next Steps</h5>", unsafe_allow_html=True)
        if st.button("➡️ Load this Recipe in the Interactive Simulator", use_container_width=True):
            # Load the SAVED results into the sim_params
            st.session_state.sim_params = {
                "pulse_energy": results['pulse_energy_uJ'], 
                "beam_diameter": results['beam_diameter_um'],
                "ablation_threshold": results['ablation_threshold_j_cm2'], 
                "alpha_inv": results['alpha_inv'],
                "number_of_shots": results['number_of_shots'], 
                "material_thickness": results['material_thickness']
            }
            st.session_state.switch_to_simulator = True
            st.rerun()
    else:
        # This is now the default state if no results have been calculated yet
        st.info("Define your goal and click 'Generate Recipe' to see the results.")
