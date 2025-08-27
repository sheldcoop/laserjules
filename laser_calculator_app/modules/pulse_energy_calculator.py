import streamlit as st
import pandas as pd
from utils import parse_text_input, convert_df_to_csv

def render():
    st.header("Calculate Pulse Energy")
    st.markdown("---")

    # --- MAIN TWO-COLUMN LAYOUT ---
    col_inputs, col_outputs = st.columns([2, 3], gap="large")

    # --- LEFT COLUMN: THE CONTROL PANEL ---
    with col_inputs:
        st.subheader("Control Panel")
        
        with st.container(border=True):
            st.markdown("<h6>Data Entry</h6>", unsafe_allow_html=True)
            avg_power_str = st.text_input("Average Power (mW)", placeholder="e.g., 80, 90, 100")
            rep_rate_str = st.text_input("Repetition Rate (kHz)", placeholder="e.g., 50, 50, 60")
            
            with st.expander("Show Formula"):
                st.latex(r'''\text{Pulse Energy (µJ)} = \frac{\text{Average Power (mW)}}{\text{Repetition Rate (kHz)}}''')
            
            calculate_button = st.button("Calculate Pulse Energy", type="primary", use_container_width=True)

    # --- RIGHT COLUMN: THE RESULTS CANVAS ---
    with col_outputs:
        st.subheader("Results Canvas")

        with st.container(border=True):
            # We check if the button was pressed in this script run
            if calculate_button:
                with st.spinner("Calculating..."):
                    power_list = parse_text_input(avg_power_str)
                    rate_list = parse_text_input(rep_rate_str)
                    
                    # Error handling and calculation
                    if not power_list or not rate_list:
                        st.warning("Please enter values in all fields.")
                        st.session_state.pe_results_df = None # Clear previous results
                    elif len(power_list) != len(rate_list):
                        st.warning("Please enter the same number of data points for all inputs.")
                        st.session_state.pe_results_df = None # Clear previous results
                    else:
                        df = pd.DataFrame({'Avg. Power (mW)': power_list, 'Rep. Rate (kHz)': rate_list})
                        df['Pulse Energy (µJ)'] = df['Avg. Power (mW)'] / df['Rep. Rate (kHz)']
                        st.session_state.pe_results_df = df # Save results to session state
            
            # This part always runs, displaying the current results or the placeholder
            if 'pe_results_df' in st.session_state and st.session_state.pe_results_df is not None:
                st.markdown("<h6>Calculation Results</h6>", unsafe_allow_html=True)
                df_to_show = st.session_state.pe_results_df
                
                formatters = {'Pulse Energy (µJ)': '{:.3f}'}
                st.dataframe(df_to_show.style.format(formatters), use_container_width=True, hide_index=True)
                
                csv_data = convert_df_to_csv(df_to_show)
                st.download_button(
                    "Download Results as CSV", 
                    csv_data, 
                    "pulse_energy_results.csv", 
                    "text/csv", 
                    use_container_width=True
                )
            else:
                st.info("Your calculation results will appear here.")
