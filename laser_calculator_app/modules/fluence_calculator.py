import streamlit as st
import pandas as pd
import numpy as np
from utils import parse_text_input, convert_df_to_csv, UJ_TO_J, UM_TO_CM

def render():
    st.header("Calculate Fluence & Cumulative Dose")
    st.markdown("---")
    use_avg_power = st.toggle("Input using Average Power instead of Pulse Energy")
    
    if use_avg_power:
        avg_power_str = st.text_input("Average Power (mW)", placeholder="e.g., 80, 90, 100")
        rep_rate_str = st.text_input("Repetition Rate (kHz)", placeholder="e.g., 50, 50, 60")
    else:
        pulse_energy_str = st.text_input("Pulse Energy (µJ)", placeholder="e.g., 1.6, 1.8, 2.0")
        
    diameter_str = st.text_input("Beam Spot Diameter (1/e²) (µm)", placeholder="e.g., 10, 12, 15")
    shots_str = st.text_input("Number of Shots", placeholder="e.g., 40, 50, 60")
    with st.expander("Show Formulas"): st.latex(r'''\text{Peak Fluence (J/cm²)} = 2 \times \frac{\text{Pulse Energy (J)}}{\text{Area (cm²)}}''')

    if st.button("Calculate Fluence", type="primary", use_container_width=True):
        with st.spinner("Calculating..."):
            diameter_list = parse_text_input(diameter_str)
            shots_list = [int(s) for s in parse_text_input(shots_str)]
            
            if use_avg_power:
                power_list = parse_text_input(avg_power_str)
                rate_list = parse_text_input(rep_rate_str)
                if not all([power_list, rate_list, diameter_list, shots_list]):
                    st.warning("Please enter values in all fields."); return
                if not (len(power_list) == len(rate_list) == len(diameter_list) == len(shots_list)):
                    st.warning("Please ensure all inputs have the same number of data points."); return
                energy_list = [p / r for p, r in zip(power_list, rate_list)]
                df = pd.DataFrame({'Avg. Power (mW)': power_list, 'Rep. Rate (kHz)': rate_list, 'Pulse Energy (µJ)': energy_list, 'Diameter (µm)': diameter_list, 'Number of Shots': shots_list})
            else:
                energy_list = parse_text_input(pulse_energy_str)
                if not all([energy_list, diameter_list, shots_list]):
                    st.warning("Please enter values in all fields."); return
                if not (len(energy_list) == len(diameter_list) == len(shots_list)):
                    st.warning("Please ensure all inputs have the same number of data points."); return
                df = pd.DataFrame({'Pulse Energy (µJ)': energy_list, 'Diameter (µm)': diameter_list, 'Number of Shots': shots_list})
            
            df['Energy (J)'] = df['Pulse Energy (µJ)'] * UJ_TO_J
            df['Area (cm²)'] = np.pi * (((df['Diameter (µm)'] / 2) * UM_TO_CM) ** 2)
            df['Peak Fluence (J/cm²)'] = 2 * (df['Energy (J)'] / df['Area (cm²)'])
            df['Cumulative Dose (J/cm²)'] = df['Peak Fluence (J/cm²)'] * df['Number of Shots']
            st.session_state.results_df = df

    if st.session_state.app_mode in ["Fluence (Energy Density)"] and st.session_state.get('results_df') is not None:
        st.markdown("---"); st.markdown(f'<p class="results-header">Calculation Results</p>', unsafe_allow_html=True)
        df = st.session_state.results_df
        ideal_order = ['Avg. Power (mW)', 'Rep. Rate (kHz)', 'Pulse Energy (µJ)', 'Diameter (µm)', 'Number of Shots', 'Peak Fluence (J/cm²)', 'Cumulative Dose (J/cm²)']
        cols_to_show = [col for col in ideal_order if col in df.columns]
        formatters = {'Pulse Energy (µJ)': '{:.3f}', 'Peak Fluence (J/cm²)': '{:.3f}', 'Cumulative Dose (J/cm²)': '{:.3f}', 'Area (cm²)': '{:.4e}'}
        st.dataframe(df[cols_to_show].style.format(formatters), use_container_width=True, hide_index=True)
        st.download_button("Download Results as CSV", convert_df_to_csv(df[cols_to_show]), "calculator_results.csv", "text/csv", use_container_width=True)