import streamlit as st
import pandas as pd
from utils import parse_text_input, convert_df_to_csv

def render():
    st.header("Calculate Pulse Energy")
    st.markdown("---")
    avg_power_str = st.text_input("Average Power (mW)", placeholder="e.g., 80, 90, 100")
    rep_rate_str = st.text_input("Repetition Rate (kHz)", placeholder="e.g., 50, 50, 60")
    with st.expander("Show Formula"): st.latex(r'''\text{Pulse Energy (µJ)} = \frac{\text{Average Power (mW)}}{\text{Repetition Rate (kHz)}}''')
    
    if st.button("Calculate Pulse Energy", type="primary", use_container_width=True):
        with st.spinner("Calculating..."):
            power_list = parse_text_input(avg_power_str)
            rate_list = parse_text_input(rep_rate_str)
            if not power_list or not rate_list:
                st.warning("Please enter values in all fields.")
            elif len(power_list) != len(rate_list):
                st.warning("Please enter the same number of data points for all inputs.")
            else:
                df = pd.DataFrame({'Avg. Power (mW)': power_list, 'Rep. Rate (kHz)': rate_list})
                df['Pulse Energy (µJ)'] = df['Avg. Power (mW)'] / df['Rep. Rate (kHz)']
                st.session_state.results_df = df

    if st.session_state.app_mode in ["Pulse Energy"] and st.session_state.get('results_df') is not None:
        st.markdown("---"); st.markdown(f'<p class="results-header">Calculation Results</p>', unsafe_allow_html=True)
        df = st.session_state.results_df
        ideal_order = ['Avg. Power (mW)', 'Rep. Rate (kHz)', 'Pulse Energy (µJ)']
        cols_to_show = [col for col in ideal_order if col in df.columns]
        formatters = {'Pulse Energy (µJ)': '{:.3f}'}
        st.dataframe(df[cols_to_show].style.format(formatters), use_container_width=True, hide_index=True)
        st.download_button("Download Results as CSV", convert_df_to_csv(df[cols_to_show]), "calculator_results.csv", "text/csv", use_container_width=True)