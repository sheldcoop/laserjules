import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from utils import UJ_TO_J, UM_TO_CM

def render():
    st.markdown("### Beam & Threshold Analyzer (Liu Plot Method)")
    st.info("This method determines the ablation threshold and effective beam spot size by measuring the **diameter** of ablated craters at different pulse energies.")
    st.markdown("---")

    # --- Engineer's Workbench Layout ---
    col_inputs, col_outputs = st.columns([2, 3], gap="large")

    # ---================== COLUMN 1: CONTROL PANEL ==================---
    with col_inputs:
        st.subheader("Control Panel")

        with st.container(border=True):
            st.markdown("<h5>Data Entry</h5>", unsafe_allow_html=True)
            input_method = st.radio(
                "Input Method", ["Manual Entry", "Upload CSV"],
                label_visibility="collapsed", horizontal=True
            )

            if input_method == "Manual Entry":
                st.caption("Edit the example data below or add your own points.")
                example_data = {
                    "Pulse Energy (µJ)": [10.0, 15.0, 20.0, 25.0, 30.0],
                    "Measured Diameter (µm)": [12.5, 18.2, 22.4, 25.8, 28.6]
                }
                initial_df = pd.DataFrame(example_data)
                edited_df = st.data_editor(
                    initial_df,
                    num_rows="dynamic",
                    use_container_width=True
                )
            else:
                uploaded_file = st.file_uploader(
                    "Upload a CSV file",
                    type="csv",
                    help="Your CSV should contain a 'energy' column and a 'diameter' column."
                )

        analyze_button = st.button("Analyze Liu Plot", type="primary", use_container_width=True)

    # ---================== COLUMN 2: RESULTS CANVAS ==================---
    with col_outputs:
        st.subheader("Results Canvas")

        if analyze_button:
            data_to_process = None
            if input_method == "Manual Entry":
                data_to_process = edited_df.dropna(how="any")
            elif uploaded_file is not None:
                data_to_process = pd.read_csv(uploaded_file)
            
            if data_to_process is not None and not data_to_process.empty:
                with st.spinner("Analyzing data..."):
                    try:
                        # Standardize column names
                        rename_map = {col: 'Pulse Energy (µJ)' for col in data_to_process.columns if 'energy' in col.lower()}
                        rename_map.update({col: 'Measured Diameter (µm)' for col in data_to_process.columns if 'diameter' in col.lower()})
                        data_to_process.rename(columns=rename_map, inplace=True)
                        
                        data_to_fit = data_to_process[
                            (data_to_process['Pulse Energy (µJ)'] > 0) & 
                            (data_to_process['Measured Diameter (µm)'] > 0)
                        ].copy()

                        if len(data_to_fit) < 2:
                            st.error("Analysis requires at least two valid data points.")
                        else:
                            # --- Core Liu Plot Calculations ---
                            data_to_fit['Diameter Squared (µm²)'] = data_to_fit['Measured Diameter (µm)']**2
                            data_to_fit['Log Energy'] = np.log(data_to_fit['Pulse Energy (µJ)'])
                            
                            slope, intercept, r_value, _, _ = stats.linregress(data_to_fit['Log Energy'], data_to_fit['Diameter Squared (µm²)'])
                            r_squared = r_value**2
                            
                            # From slope = 2 * w₀², calculate beam radius w₀
                            w0_squared_um2 = slope / 2
                            w0_um = np.sqrt(w0_squared_um2)
                            beam_spot_diameter_um = 2 * w0_um
                            
                            # From intercept = -slope * ln(E_th), calculate threshold energy E_th
                            threshold_energy_uJ = np.exp(-intercept / slope) if slope != 0 else 0
                            
                            # From E_th and w₀, calculate threshold fluence F_th
                            threshold_energy_J = threshold_energy_uJ * UJ_TO_J
                            w0_cm = w0_um * UM_TO_CM
                            threshold_fluence_j_cm2 = (2 * threshold_energy_J) / (np.pi * w0_cm**2) if w0_cm > 0 else 0
                            
                            st.markdown("<h6>Analysis Results</h6>", unsafe_allow_html=True)
                            res1, res2, res3 = st.columns(3)
                            res1.metric("Calculated Ablation Threshold", f"{threshold_fluence_j_cm2:.3f} J/cm²")
                            res2.metric("Calculated Beam Spot Diameter", f"{beam_spot_diameter_um:.2f} µm")
                            res3.metric("Goodness of Fit (R²)", f"{r_squared:.4f}")

                            st.markdown("<hr>", unsafe_allow_html=True)
                            st.markdown("<h6>Liu Plot: D² vs. ln(Energy)</h6>", unsafe_allow_html=True)
                            
                            fig = px.scatter(
                                data_to_fit, x='Log Energy', y='Diameter Squared (µm²)',
                                labels={'Log Energy': 'ln(Pulse Energy)', 'Diameter Squared (µm²)': 'Diameter² (µm²)'}
                            )
                            fit_x = np.linspace(data_to_fit['Log Energy'].min(), data_to_fit['Log Energy'].max(), 100)
                            fit_y = slope * fit_x + intercept
                            fig.add_trace(go.Scatter(x=fit_x, y=fit_y, mode='lines', name='Linear Fit', line=dict(color='#ef4444')))
                            st.plotly_chart(fig, use_container_width=True)

                            # --- Workflow Integration ---
                            st.markdown("---")
                            st.markdown("<h5>Next Steps</h5>", unsafe_allow_html=True)
                            if st.button("➡️ Use these parameters in Microvia Simulator", use_container_width=True):
                                st.session_state.sim_params = {
                                    'beam_diameter': beam_spot_diameter_um,
                                    'ablation_threshold': threshold_fluence_j_cm2
                                }
                                st.session_state.app_mode = "Microvia Process Simulator"
                                st.rerun()

                    except Exception as e:
                        st.error(f"An error occurred during analysis: {e}")
            else:
                st.warning("Please provide data before clicking 'Analyze Liu Plot'.")
        
        else:
            st.info("Your Liu Plot analysis, including the calculated beam spot size and ablation threshold, will appear here.")