import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics import r2_score
from utils import parse_text_input, convert_df_to_csv, UJ_TO_J, UM_TO_CM

def render():
    st.header("Analyze Ablation Threshold via Liu Plot")
    st.markdown("---")
    st.info("This method determines the ablation threshold and effective beam spot size by measuring the **diameter** of ablated craters at different **pulse energies**.")
    with st.expander("ℹ️ Understanding the Liu Plot Method"):
        st.markdown(r"""The Liu method determines $F_{th}$ and $w_0$ from the relationship: $D^2 = 2w_0^2 \ln\left(\frac{F_0}{F_{th}}\right)$. Substituting the peak fluence $F_0 = 2E / (\pi w_0^2)$ gives a linear relationship between $D^2$ and $\ln(E)$:""")
        st.latex(r'''D^2 = 2w_0^2 \left( \ln(E) - \ln(E_{th}) \right)''')

    input_method = st.radio("Select Data Input Method", ["Paste Data", "Upload CSV"], horizontal=True, key="liu_input")
    data = None
    if input_method == "Paste Data":
        col1, col2 = st.columns(2)
        energy_str = col1.text_area("Paste Pulse Energy Data (µJ)", "10\n15\n20\n25\n30", height=250)
        diameter_str = col2.text_area("Paste Measured Diameter Data (µm)", "12.5\n18.2\n22.4\n25.8\n28.6", height=250)
    else:
        uploaded_file = st.file_uploader("Upload CSV (must contain 'energy' and 'diameter' columns)", type="csv", key="liu_upload")
        if uploaded_file:
            data = pd.read_csv(uploaded_file)
            
    if st.button("Analyze Liu Plot", type="primary", use_container_width=True):
        with st.spinner("Analyzing data and fitting model..."):
            try:
                if input_method == "Paste Data":
                    energy_list = parse_text_input(energy_str)
                    diameter_list = parse_text_input(diameter_str)
                    if len(energy_list) != len(diameter_list) or not energy_list:
                        st.error("Please ensure you paste the same number of valid data points for energy and diameter.")
                        return
                    data = pd.DataFrame({'Pulse Energy (µJ)': energy_list, 'Diameter (µm)': diameter_list})

                if data is not None:
                    rename_map = {col: 'Pulse Energy (µJ)' for col in data.columns if 'energy' in col.lower()}
                    rename_map.update({col: 'Diameter (µm)' for col in data.columns if 'diameter' in col.lower()})
                    data = data.rename(columns=rename_map)
                    
                    if 'Pulse Energy (µJ)' in data.columns and 'Diameter (µm)' in data.columns:
                        data_to_fit = data[(data['Diameter (µm)'] > 0) & (data['Pulse Energy (µJ)'] > 0)].copy()
                        if len(data_to_fit) < 2:
                            st.error("At least two data points with positive energy and diameter are required.")
                            return

                        data_to_fit['Energy (J)'] = data_to_fit['Pulse Energy (µJ)'] * UJ_TO_J
                        data_to_fit['Log Energy (J)'] = np.log(data_to_fit['Energy (J)'])
                        data_to_fit['Diameter² (µm²)'] = data_to_fit['Diameter (µm)']**2
                        
                        fit = np.polyfit(data_to_fit['Log Energy (J)'], data_to_fit['Diameter² (µm²)'], 1)
                        slope, intercept = fit
                        
                        w0_squared_um2 = slope / 2
                        w0_um = np.sqrt(w0_squared_um2) if w0_squared_um2 > 0 else 0
                        beam_diameter_um = 2 * w0_um
                        
                        log_E_th = -intercept / slope
                        E_th_J = np.exp(log_E_th)
                        
                        area_cm2 = np.pi * (w0_um * UM_TO_CM)**2
                        F_th_J_cm2 = (2 * E_th_J) / area_cm2 if area_cm2 > 0 else 0
                        y_pred = np.polyval(fit, data_to_fit['Log Energy (J)'])
                        r2 = r2_score(data_to_fit['Diameter² (µm²)'], y_pred)
                        
                        st.session_state.liu_results = {
                            "data": data_to_fit, "threshold": F_th_J_cm2, "beam_diameter": beam_diameter_um,
                            "r2": r2, "slope": slope, "intercept": intercept
                        }
                    else:
                        st.error("Could not find 'Energy' and 'Diameter' columns in your data.")
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
    
    if st.session_state.app_mode == "Liu Plot Analyzer" and st.session_state.get('liu_results'):
        results = st.session_state.liu_results
        st.markdown("---"); st.markdown(f'<p class="results-header">Liu Plot Analysis Results</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Calculated Ablation Threshold", f"{results['threshold']:.3f} J/cm²" if isinstance(results['threshold'], float) else "N/A")
        col2.metric("Calculated Beam Spot Diameter (1/e²)", f"{results['beam_diameter']:.2f} µm" if isinstance(results['beam_diameter'], float) else "N/A")
        col3.metric("Goodness of Fit (R²)", f"{results['r2']:.4f}" if isinstance(results['r2'], float) else "N/A")
        chart_title = (f"Liu Plot: D² vs. ln(Energy)<br><sup>Fit: y = {results.get('slope', 0):.1f}*x + ({results.get('intercept', 0):.1f}) | R² = {results.get('r2', 0):.4f}</sup>")
        fig = px.scatter(results['data'], x='Log Energy (J)', y='Diameter² (µm²)', title=chart_title, trendline="ols", log_x=False, hover_data=['Pulse Energy (µJ)', 'Diameter (µm)'])
        fig.update_traces(marker=dict(size=10, color='#ef4444'))
        fig.update_layout(xaxis_title="ln(Pulse Energy) [ln(J)]", yaxis_title="Diameter² [µm²]")
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Processed Data")
        st.dataframe(results['data'].style.format(precision=3), use_container_width=True, hide_index=True)
        st.download_button("Download Data as CSV", convert_df_to_csv(results['data']), "liu_plot_analysis.csv", "text/csv", use_container_width=True)