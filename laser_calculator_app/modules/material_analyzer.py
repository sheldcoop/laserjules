import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics import r2_score
from utils import parse_text_input, convert_df_to_csv

def render():
    st.header("Analyze Material Ablation Rate")
    st.markdown("---"); st.info("Upload or paste experimental data (Fluence vs. Depth) to characterize a material.")
    number_of_shots = st.number_input("Number of Shots (used in experiment)", 1, value=50)
    input_method = st.radio("Select Data Input Method", ["Paste Data", "Upload CSV"], horizontal=True)

    data = None
    if input_method == "Paste Data":
        col1, col2 = st.columns(2)
        fluence_str = col1.text_area("Paste Fluence Data (J/cm²)", "1.5\n2.0\n2.5\n3.0", height=250)
        depth_str = col2.text_area("Paste Measured Depth Data (µm)", "15\n45\n70\n90", height=250)
    else:
        uploaded_file = st.file_uploader("Upload CSV (must contain 'fluence' and 'depth' columns)", type="csv")
        if uploaded_file:
            data = pd.read_csv(uploaded_file)

    if st.button("Analyze Material", type="primary", use_container_width=True):
        with st.spinner("Analyzing data..."):
            try:
                if input_method == "Paste Data":
                    fluence_list = parse_text_input(fluence_str)
                    depth_list = parse_text_input(depth_str)
                    if len(fluence_list) != len(depth_list) or not fluence_list:
                        st.error("Please ensure you paste the same number of valid data points for fluence and depth.")
                        return
                    data = pd.DataFrame({'Fluence (J/cm²)': fluence_list, 'Depth (µm)': depth_list})
                
                if data is not None:
                    rename_map = {col: 'Fluence (J/cm²)' for col in data.columns if 'fluence' in col.lower()}
                    rename_map.update({col: 'Depth (µm)' for col in data.columns if 'depth' in col.lower()})
                    data = data.rename(columns=rename_map)

                    if 'Fluence (J/cm²)' in data.columns and 'Depth (µm)' in data.columns:
                        data['Ablation Rate (µm/pulse)'] = data['Depth (µm)'] / number_of_shots
                        data_to_fit = data[(data['Ablation Rate (µm/pulse)'] > 0) & (data['Fluence (J/cm²)'] > 0)].copy()
                        
                        ablation_threshold, r2, slope, intercept = "N/A", "N/A", "N/A", "N/A"
                        if len(data_to_fit) > 1:
                            data_to_fit['Log Fluence'] = np.log(data_to_fit['Fluence (J/cm²)'])
                            fit = np.polyfit(data_to_fit['Log Fluence'], data_to_fit['Ablation Rate (µm/pulse)'], 1)
                            slope, intercept = fit
                            ablation_threshold = np.exp(-intercept / slope)
                            y_pred = np.polyval(fit, data_to_fit['Log Fluence'])
                            r2 = r2_score(data_to_fit['Ablation Rate (µm/pulse)'], y_pred)
                        
                        st.session_state.analysis_results = {"data": data, "threshold": ablation_threshold, "r2": r2, "slope": slope, "intercept": intercept}
                    else:
                        st.error("Could not find 'Fluence' and 'Depth' columns in your data.")
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
    
    if st.session_state.app_mode == "Material Analyzer" and st.session_state.get('analysis_results'):
        results = st.session_state.analysis_results
        st.markdown("---"); st.markdown(f'<p class="results-header">Material Analysis Results</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        col1.metric("Calculated Ablation Threshold", f"{results['threshold']:.3f} J/cm²" if isinstance(results['threshold'], float) else "N/A")
        col2.metric("Goodness of Fit (R²)", f"{results['r2']:.4f}" if isinstance(results['r2'], float) else "N/A")
        chart_title = (f"Ablation Rate vs. Fluence<br><sup>Fit: y = {results.get('slope', 0):.3f} * ln(x) + ({results.get('intercept', 0):.3f}) | R² = {results.get('r2', 0):.4f}</sup>")
        fig = px.scatter(results['data'], x='Fluence (J/cm²)', y='Ablation Rate (µm/pulse)', title=chart_title, trendline="ols", log_x=True, hover_data=['Fluence (J/cm²)', 'Depth (µm)'])
        fig.update_traces(marker=dict(size=10, color='#ef4444'))
        fig.update_layout(xaxis_title="Fluence (J/cm²) [Log Scale]", yaxis_title="Ablation Rate (µm/pulse)")
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Processed Data")
        st.dataframe(results['data'].style.format(precision=3), use_container_width=True, hide_index=True)
        st.download_button("Download Data as CSV", convert_df_to_csv(results['data']), "material_analysis.csv", "text/csv", use_container_width=True)