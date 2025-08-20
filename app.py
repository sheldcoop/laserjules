import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Laser Process Calculator")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        body { font-family: 'Inter', sans-serif; }
        .stApp { background-color: #f6f6f7; }
        [data-testid="stSidebar"] { border-right: 1px solid #dcdcdc; padding: 20px; }
        h1 { padding-top: 20px; padding-bottom: 10px; }

        /* Sidebar button styles */
        [data-testid="stSidebar"] .stButton button {
            text-align: left !important; font-weight: 500; padding: 10px 15px; border-radius: 8px;
        }
        /* Data Table & Results Styling */
        .stDataFrame thead th { background-color: #e9ecef; color: #212529; font-weight: 600; }
        .results-header { font-size: 22px; font-weight: 600; color: #16a34a; }
        hr { margin: 2rem 0; border-color: #e0e0e0; }
    </style>
""", unsafe_allow_html=True)

# --- Initialize session state ---
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Process Recommender"
if 'results_df' not in st.session_state:
    st.session_state.results_df = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'recipe' not in st.session_state:
    st.session_state.recipe = None
    
# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.header("App Mode")
    modes = ["Process Recommender", "Material Analyzer", "Mask Finder", "Pulse Energy", "Fluence (Energy Density)"]
    
    for mode in modes:
        btn_type = "primary" if st.session_state.app_mode == mode else "secondary"
        if st.button(mode, use_container_width=True, type=btn_type):
            st.session_state.app_mode = mode; st.session_state.results_df = None; st.session_state.analysis_results = None; st.session_state.recipe = None; st.rerun()

# --- MAIN PANEL ---
st.title("Advanced Laser Process Calculator")

# --- MASTER MODE: PROCESS RECOMMENDER (FIXED) ---
if st.session_state.app_mode == "Process Recommender":
    st.header("Generate a Process Recipe")
    st.markdown("---"); st.info("Input your goal and material properties to generate a recommended starting recipe.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🎯 Your Goal"); target_via_um = st.number_input("Target Via Diameter (µm)", 1.0, value=12.0); material_thickness_um = st.number_input("Material Thickness (µm)", 1.0, value=25.0)
    with col2:
        st.subheader("🔬 Material Properties"); st.caption("_(Use the 'Material Analyzer' to find these values)_"); optimal_fluence = st.number_input("Optimal Fluence (J/cm²)", 0.1, value=2.0, format="%.3f"); ablation_rate = st.number_input("Ablation Rate at Optimal Fluence (µm/pulse)", 0.01, value=0.9, format="%.3f")
    with col3:
        st.subheader("⚙️ Machine Settings"); beam_spot_um = st.number_input("Beam Spot Size (µm)", 1.0, value=15.0); rep_rate_khz = st.number_input("Repetition Rate (kHz)", 1.0, value=50.0)

    if st.button("Generate Recipe", type="primary"):
        radius_cm = (beam_spot_um / 2) * 1e-4; area_cm2 = np.pi * (radius_cm ** 2); required_energy_J = (optimal_fluence * area_cm2) / 2; required_energy_uJ = required_energy_J * 1e6
        required_shots = np.ceil(material_thickness_um / ablation_rate)
        required_power_mW = required_energy_uJ * rep_rate_khz
        
        # ******** THIS IS THE BUG FIX ********
        # Save the raw numbers, NOT formatted strings.
        st.session_state.recipe = {
            "Target Via Diameter (µm)": target_via_um,
            "Beam Spot Size (µm)": beam_spot_um,
            "Repetition Rate (kHz)": rep_rate_khz,
            "Material Thickness (µm)": material_thickness_um,
            "Optimal Fluence (J/cm²)": optimal_fluence,
            "Required Pulse Energy (µJ)": required_energy_uJ,
            "Required Average Power (mW)": required_power_mW,
            "Required Number of Shots": int(required_shots)
        }
        # ***********************************

    if st.session_state.recipe:
        st.markdown("---"); st.markdown(f'<p class="results-header">Recommended Process Recipe</p>', unsafe_allow_html=True)
        recipe = st.session_state.recipe
        col1, col2, col3 = st.columns(3)
        # We can format the display here with f-strings, which is safe
        col1.metric("Required Pulse Energy", f"{recipe['Required Pulse Energy (µJ)']:.3f} µJ")
        col2.metric("Required Average Power", f"{recipe['Required Average Power (mW)']:.1f} mW")
        col3.metric("Required Number of Shots", f"{recipe['Required Number of Shots']} pulses")
        
        st.subheader("Complete Recipe Summary")
        recipe_df = pd.DataFrame.from_dict(recipe, orient='index', columns=['Value'])
        
        # ******** THIS IS THE BUG FIX ********
        # Apply formatting to the DataFrame right before displaying it
        st.table(recipe_df.style.format(precision=3))
        # ***********************************

# --- ALL OTHER MODES ... ---
# (The rest of the file is identical to the last working version)
elif st.session_state.app_mode == "Material Analyzer":
    st.header("Analyze Material Ablation Rate")
    st.markdown("---"); st.info("Upload or paste your experimental data to characterize a new material.")
    number_of_shots = st.number_input("Number of Shots (used in experiment)", 1, value=50)
    input_method = st.radio("Select Data Input Method", ["Paste Data", "Upload CSV"], horizontal=True)
    if input_method == "Paste Data":
        col1, col2 = st.columns(2); fluence_str = col1.text_area("Paste Fluence Data (J/cm²)", placeholder="1.5\n2.0\n2.5\n3.0"); depth_str = col2.text_area("Paste Measured Depth Data (µm)", placeholder="15\n45\n70\n90")
    else: uploaded_file = st.file_uploader("Upload CSV file", type="csv"); st.markdown("Your CSV should have two columns: 'Fluence' and 'Depth'")
    if st.button("Analyze Material", type="primary"):
        data = None
        if input_method == "Paste Data":
            if fluence_str and depth_str:
                fluence_list = [float(f) for f in fluence_str.strip().split()]; depth_list = [float(d) for d in depth_str.strip().split()]
                if len(fluence_list) == len(depth_list): data = pd.DataFrame({'Fluence (J/cm²)': fluence_list, 'Depth (µm)': depth_list})
                else: st.warning("Please ensure you paste the same number of data points for fluence and depth.")
        elif input_method == "Upload CSV":
            if uploaded_file is not None:
                try:
                    data = pd.read_csv(uploaded_file)
                    if 'Fluence' not in data.columns or 'Depth' not in data.columns: st.error("CSV must contain columns named 'Fluence' and 'Depth'."); data = None
                    else: data = data.rename(columns={'Fluence': 'Fluence (J/cm²)', 'Depth': 'Depth (µm)'})
                except Exception as e: st.error(f"Error reading CSV file: {e}")
        if data is not None:
            data['Ablation Rate (µm/pulse)'] = data['Depth (µm)'] / number_of_shots
            data_to_fit = data[data['Ablation Rate (µm/pulse)'] > 0].copy()
            if len(data_to_fit) > 1:
                data_to_fit['Log Fluence'] = np.log(data_to_fit['Fluence (J/cm²)'])
                fit = np.polyfit(data_to_fit['Log Fluence'], data_to_fit['Ablation Rate (µm/pulse)'], 1)
                slope, intercept = fit; ablation_threshold = np.exp(-intercept / slope)
            else: ablation_threshold = "N/A (Not enough data points)"
            st.session_state.analysis_results = {"data": data, "threshold": ablation_threshold}
elif st.session_state.app_mode == "Mask Finder":
    st.header("Find Required Mask Size"); st.markdown("---")
    hole_size_um = st.number_input("Target Via Diameter (µm)", 1.0, value=14.0, step=1.0); demag_factor = st.number_input("System Demagnification Factor (e.g., 60x)", 1.0, value=60.0, step=0.1)
    with st.expander("Show Formula"): st.latex(r'''\text{Mask Size (mm)} = \frac{\text{Target Via Diameter (µm)} \times \text{Demagnification Factor}}{1000}''')
    if demag_factor > 0:
        required_mask_size_mm = (hole_size_um * demag_factor) / 1000
        st.markdown("---"); st.markdown(f'<p class="results-header" style="color: #007aff;">Calculated Mask Size</p>', unsafe_allow_html=True); st.metric(label="Required Mask Diameter", value=f"{required_mask_size_mm:.3f} mm")
elif st.session_state.app_mode == "Pulse Energy":
    st.header("Calculate Pulse Energy"); st.markdown("---")
    avg_power_str = st.text_input("Average Power (mW)", placeholder="e.g., 80, 90, 140"); rep_rate_str = st.text_input("Repetition Rate (kHz)", placeholder="e.g., 50, 50, 50")
    with st.expander("Show Formula"): st.latex(r'''\text{Pulse Energy (µJ)} = \frac{\text{Average Power (mW)}}{\text{Repetition Rate (kHz)}}''')
    if st.button("Calculate Pulse Energy", type="primary"):
        if not avg_power_str or not rep_rate_str: st.warning("Please enter values in all fields.")
        else:
            try:
                power_list = [float(p.strip()) for p in avg_power_str.split(',')]; rate_list = [float(r.strip()) for r in rep_rate_str.split(',')]
                if len(power_list) == len(rate_list):
                    df = pd.DataFrame({'Avg. Power (mW)': power_list, 'Rep. Rate (kHz)': rate_list}); df['Pulse Energy (µJ)'] = df['Avg. Power (mW)'] / df['Rep. Rate (kHz)']; st.session_state.results_df = df
                else: st.warning("Please enter the same number of data points for all inputs.")
            except Exception as e: st.error(f"An error occurred: {e}")
elif st.session_state.app_mode == "Fluence (Energy Density)":
    st.header("Calculate Fluence & Cumulative Dose"); st.markdown("---")
    use_avg_power = st.toggle("Input using Average Power instead of Pulse Energy")
    if use_avg_power:
        avg_power_str = st.text_input("Average Power (mW)", placeholder="e.g., 80, 90, 140"); rep_rate_str = st.text_input("Repetition Rate (kHz)", placeholder="e.g., 50, 50, 50"); pulse_energy_str = ""
    else:
        pulse_energy_str = st.text_input("Pulse Energy (µJ)", placeholder="e.g., 1.6, 1.8, 2.8"); avg_power_str, rep_rate_str = "", ""
    diameter_str = st.text_input("Beam Spot Diameter (µm)", placeholder="e.g., 9, 10, 14"); shots_str = st.text_input("Number of Shots", placeholder="e.g., 22, 22, 22")
    with st.expander("Show Formulas"): st.latex(r'''\text{Peak Fluence (J/cm²)} = 2 \times \frac{\text{Pulse Energy (J)}}{\text{Area (cm²)}}''')
    if st.button("Calculate Fluence", type="primary"):
        if (not pulse_energy_str and not avg_power_str) or not diameter_str or not shots_str: st.warning("Please enter values in all required fields.")
        else:
            try:
                if use_avg_power:
                    power_list = [float(p.strip()) for p in avg_power_str.split(',')]; rate_list = [float(r.strip()) for r in rep_rate_str.split(',')];
                    if len(power_list) != len(rate_list): st.warning("Power and Repetition Rate must have the same number of data points."); st.stop()
                    energy_list = [p / r for p, r in zip(power_list, rate_list)]
                else: energy_list = [float(e.strip()) for e in pulse_energy_str.split(',')]
                diameter_list = [float(d.strip()) for d in diameter_str.split(',')]; shots_list = [int(s.strip()) for s in shots_str.split(',')]
                if not (len(energy_list) == len(diameter_list) == len(shots_list)): st.warning("Please ensure all inputs have the same number of data points.")
                else:
                    df = pd.DataFrame({'Pulse Energy (µJ)': energy_list, 'Diameter (µm)': diameter_list, 'Number of Shots': shots_list})
                    if use_avg_power: df['Avg. Power (mW)'] = power_list; df['Rep. Rate (kHz)'] = rate_list
                    df['Energy (J)'] = df['Pulse Energy (µJ)'] * 1e-6; df['Area (cm²)'] = np.pi * (((df['Diameter (µm)'] / 2) * 1e-4) ** 2); df['Peak Fluence (J/cm²)'] = 2 * (df['Energy (J)'] / df['Area (cm²)']); df['Cumulative Dose (J/cm²)'] = df['Peak Fluence (J/cm²)'] * df['Number of Shots']; st.session_state.results_df = df
            except Exception as e: st.error(f"An error occurred: {e}")

if st.session_state.results_df is not None:
    st.markdown("---"); st.markdown(f'<p class="results-header">Calculation Results</p>', unsafe_allow_html=True)
    cols_to_show = list(st.session_state.results_df.columns); st.dataframe(st.session_state.results_df[cols_to_show].style.format(precision=3), use_container_width=True, hide_index=True)
if st.session_state.analysis_results is not None:
    results = st.session_state.analysis_results; st.markdown("---"); st.markdown(f'<p class="results-header">Material Analysis Results</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    threshold_val = results['threshold']
    if isinstance(threshold_val, float): col1.metric("Calculated Ablation Threshold", f"{threshold_val:.3f} J/cm²")
    else: col1.metric("Calculated Ablation Threshold", threshold_val)
    fig = px.scatter(results['data'], x='Fluence (J/cm²)', y='Ablation Rate (µm/pulse)', title="Ablation Rate vs. Fluence", trendline="ols", log_x=True)
    fig.update_traces(marker=dict(size=10, color='#ef4444')); fig.update_layout(xaxis_title="Fluence (J/cm²) [Log Scale]", yaxis_title="Ablation Rate (µm/pulse)"); st.plotly_chart(fig, use_container_width=True)
    st.subheader("Processed Data"); st.dataframe(results['data'].style.format(precision=3), use_container_width=True, hide_index=True)