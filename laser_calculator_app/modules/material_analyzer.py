import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from utils import convert_df_to_csv, UJ_TO_J, UM_TO_CM

def render_depth_method_inputs():
    """Renders the UI for the Depth Method in the control panel."""
    with st.container(border=True):
        st.markdown("<h5>Experiment Setup</h5>", unsafe_allow_html=True)
        st.number_input("Number of Shots (per data point)", min_value=1, value=50, key="depth_shots")
    with st.container(border=True):
        st.markdown("<h5>Data Entry (Fluence vs. Depth)</h5>", unsafe_allow_html=True)
        input_method = st.radio("Input Method", ["Manual Entry", "Upload CSV"], key="depth_input_method", horizontal=True)
        if input_method == "Manual Entry":
            example_data = {"Fluence (J/cm²)": [1.5, 2.0, 2.5, 3.0], "Total Depth (µm)": [15.0, 45.0, 70.0, 90.0]}
            st.session_state.edited_df_depth = st.data_editor(pd.DataFrame(example_data), num_rows="dynamic", use_container_width=True, key="depth_editor")
        else:
            st.session_state.uploaded_file_depth = st.file_uploader("Upload Fluence vs. Depth CSV", type="csv", key="depth_uploader")
    st.button("Analyze Material", type="primary", use_container_width=True, key="analyze_depth")

def render_diameter_method_inputs():
    """Renders the UI for the Diameter Method (Liu Plot) in the control panel."""
    with st.container(border=True):
        st.markdown("<h5>Data Entry (Energy vs. Diameter)</h5>", unsafe_allow_html=True)
        input_method = st.radio("Input Method", ["Manual Entry", "Upload CSV"], key="diameter_input_method", horizontal=True)
        if input_method == "Manual Entry":
            example_data = {"Pulse Energy (µJ)": [10.0, 15.0, 20.0, 25.0, 30.0], "Measured Diameter (µm)": [12.5, 18.2, 22.4, 25.8, 28.6]}
            st.session_state.edited_df_diameter = st.data_editor(pd.DataFrame(example_data), num_rows="dynamic", use_container_width=True, key="diameter_editor")
        else:
            st.session_state.uploaded_file_diameter = st.file_uploader("Upload Energy vs. Diameter CSV", type="csv", key="diameter_uploader")
    st.button("Analyze Beam & Threshold", type="primary", use_container_width=True, key="analyze_diameter")

def process_depth_method_results():
    if not st.session_state.get('analyze_depth'):
        st.info("Your analysis results will appear here.")
        return
    data = get_data_from_input('depth')
    if data is None: return
    
    with st.spinner("Analyzing..."):
        data.rename(columns={c: 'Fluence (J/cm²)' for c in data.columns if 'fluence' in c.lower()}, inplace=True)
        data.rename(columns={c: 'Total Depth (µm)' for c in data.columns if 'depth' in c.lower()}, inplace=True)
        data['Ablation Rate (µm/pulse)'] = data['Total Depth (µm)'] / st.session_state.depth_shots
        data_to_fit = data[data['Ablation Rate (µm/pulse)'] > 0].copy()
        
        if len(data_to_fit) < 2:
            st.error("Need at least two valid data points.")
            return
            
        data_to_fit['Log Fluence'] = np.log(data_to_fit['Fluence (J/cm²)'])
        slope, intercept, r_value, _, _ = stats.linregress(data_to_fit['Log Fluence'], data_to_fit['Ablation Rate (µm/pulse)'])
        pen_depth, abl_thresh, r_sq = slope, np.exp(-intercept / slope), r_value**2
        
        display_common_results(abl_thresh, pen_depth, r_sq, "Penetration Depth (α⁻¹)", data, "Fluence (J/cm²)", "Ablation Rate (µm/pulse)", True, slope, intercept)

def process_diameter_method_results():
    if not st.session_state.get('analyze_diameter'):
        st.info("Your analysis results will appear here.")
        return
    data = get_data_from_input('diameter')
    if data is None: return

    with st.spinner("Analyzing..."):
        data.rename(columns={c: 'Pulse Energy (µJ)' for c in data.columns if 'energy' in c.lower()}, inplace=True)
        data.rename(columns={c: 'Measured Diameter (µm)' for c in data.columns if 'diameter' in c.lower()}, inplace=True)
        data['D_squared (µm²)'] = data['Measured Diameter (µm)']**2
        data['Log Energy'] = np.log(data['Pulse Energy (µJ)'])
        
        if len(data) < 2:
            st.error("Need at least two valid data points.")
            return

        slope, intercept, r_value, _, _ = stats.linregress(data['Log Energy'], data['D_squared (µm²)'])
        beam_diam_um = np.sqrt(slope * 2)
        eth_uJ = np.exp(-intercept / slope)
        r_sq = r_value**2
        
        fth_j_cm2 = (2 * eth_uJ * UJ_TO_J) / (np.pi * ( (beam_diam_um / 2 * UM_TO_CM)**2) )
        
        display_common_results(fth_j_cm2, beam_diam_um, r_sq, "Beam Spot Diameter (µm)", data, "Pulse Energy (µJ)", "D_squared (µm²)", True, slope, intercept)

def get_data_from_input(method_prefix):
    input_method = st.session_state.get(f'{method_prefix}_input_method', 'Manual Entry')
    data = None
    if input_method == "Manual Entry":
        data = st.session_state.get(f'edited_df_{method_prefix}', pd.DataFrame()).dropna(how="any")
    elif st.session_state.get(f'uploaded_file_{method_prefix}') is not None:
        data = pd.read_csv(st.session_state.get(f'uploaded_file_{method_prefix}'))
    
    if data is None or data.empty:
        st.error("Please provide data before analyzing.")
        return None
    return data

def display_common_results(val1, val2, r_sq, val2_label, data, x_col, y_col, log_x, slope, intercept):
    st.markdown("<h6>Calculated Properties</h6>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Ablation Threshold", f"{val1:.3f} J/cm²")
    c2.metric(val2_label, f"{val2:.3f} µm")
    c3.metric("Goodness of Fit (R²)", f"{r_sq:.4f}")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h6>Linear Fit Plot</h6>", unsafe_allow_html=True)
    fig = px.scatter(data, x=x_col, y=y_col, log_x=log_x)
    x_fit = np.linspace(data[x_col].min(), data[x_col].max(), 100)
    x_for_fit = np.log(x_fit) if log_x else x_fit
    y_fit = slope * x_for_fit + intercept
    fig.add_trace(go.Scatter(x=x_fit, y=y_fit, mode='lines', name='Fit', line=dict(color='#ef4444')))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h6>Processed Data</h6>", unsafe_allow_html=True)
    st.dataframe(data.style.format(precision=3), use_container_width=True, hide_index=True)

def render():
    st.markdown("### Material & Beam Analyzer")
    st.info("A unified tool to characterize material properties or measure your laser's beam spot size using experimental data.")
    st.markdown("---")
    col_inputs, col_outputs = st.columns([2, 3], gap="large")
    with col_inputs:
        st.subheader("Control Panel")
        with st.container(border=True):
            st.markdown("<h5>Analysis Goal</h5>", unsafe_allow_html=True)
            analysis_mode = st.radio("What do you want to determine?",
                                     ("Ablation Threshold & Penetration Depth (Depth Method)",
                                      "Ablation Threshold & Beam Spot Size (Diameter Method)"),
                                     captions=("Input Fluence vs. Depth data.", "Input Energy vs. Diameter data (Liu Plot)."))
        if "Depth Method" in analysis_mode:
            render_depth_method_inputs()
        else:
            render_diameter_method_inputs()
    with col_outputs:
        st.subheader("Results Canvas")
        if "Depth Method" in analysis_mode:
            process_depth_method_results()
        else:
            process_diameter_method_results()