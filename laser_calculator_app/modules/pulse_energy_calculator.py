import streamlit as st
from utils import parse_text_input, convert_df_to_csv
from core.pulse_energy import calculate_pulse_energy

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
            if calculate_button:
                try:
                    power_list = parse_text_input(avg_power_str)
                    rate_list = parse_text_input(rep_rate_str)
                    
                    if not power_list or not rate_list:
                        st.warning("Please enter values for both average power and repetition rate.")
                        st.session_state.pe_results_df = None
                        return

                    with st.spinner("Calculating..."):
                        results_df = calculate_pulse_energy(power_list, rate_list)
                        st.session_state.pe_results_df = results_df

                except ValueError as e:
                    st.error(f"Error: {e}")
                    st.session_state.pe_results_df = None
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    st.session_state.pe_results_df = None
            
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
