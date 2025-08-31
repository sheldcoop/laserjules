import streamlit as st
import pandas as pd
from utils import parse_text_input, convert_df_to_csv
from core.calculations import calculate_fluence_df

def render():
    """
    Renders the Fluence Calculator page in the Streamlit app.
    Handles user input, calls the core calculation function, and displays results.
    """
    st.header("Calculate Fluence & Cumulative Dose")
    st.markdown("---")

    # --- USER INPUTS ---
    use_avg_power = st.toggle("Input using Average Power instead of Pulse Energy")
    
    if use_avg_power:
        avg_power_str = st.text_input("Average Power (mW)", placeholder="e.g., 80, 90, 100")
        rep_rate_str = st.text_input("Repetition Rate (kHz)", placeholder="e.g., 50, 50, 60")
        # Initialize pulse_energy_str to avoid reference errors
        pulse_energy_str = ""
    else:
        pulse_energy_str = st.text_input("Pulse Energy (µJ)", placeholder="e.g., 1.6, 1.8, 2.0")
        # Initialize power and rate strings to avoid reference errors
        avg_power_str = ""
        rep_rate_str = ""
        
    diameter_str = st.text_input("Beam Spot Diameter (1/e²) (µm)", placeholder="e.g., 10, 12, 15")
    shots_str = st.text_input("Number of Shots", placeholder="e.g., 40, 50, 60")

    with st.expander("Show Formulas"):
        st.latex(r'''
            \text{Peak Fluence (J/cm²)} = 2 \times \frac{\text{Pulse Energy (J)}}{\text{Area (cm²)}}
        ''')
        st.latex(r'''
            \text{Cumulative Dose (J/cm²)} = \text{Peak Fluence} \times \text{Number of Shots}
        ''')

    # --- CALCULATION TRIGGER ---
    if st.button("Calculate Fluence", type="primary", use_container_width=True):
        with st.spinner("Calculating..."):
            # --- INPUT PARSING AND VALIDATION ---
            diameter_list = parse_text_input(diameter_str)
            shots_list = [int(s) for s in parse_text_input(shots_str)]
            
            power_list = None
            rate_list = None
            energy_list = None

            if use_avg_power:
                power_list = parse_text_input(avg_power_str)
                rate_list = parse_text_input(rep_rate_str)
                if not all([power_list, rate_list, diameter_list, shots_list]):
                    st.warning("Please enter values in all fields.")
                    return
                if not (len(power_list) == len(rate_list) == len(diameter_list) == len(shots_list)):
                    st.warning("Please ensure all inputs have the same number of data points.")
                    return
                # Calculate energy from power and rate for the core function
                energy_list = [p / r for p, r in zip(power_list, rate_list)]
            else:
                energy_list = parse_text_input(pulse_energy_str)
                if not all([energy_list, diameter_list, shots_list]):
                    st.warning("Please enter values in all fields.")
                    return
                if not (len(energy_list) == len(diameter_list) == len(shots_list)):
                    st.warning("Please ensure all inputs have the same number of data points.")
                    return

            # --- CALL CORE CALCULATION FUNCTION ---
            try:
                results_df = calculate_fluence_df(
                    energy_list=energy_list,
                    diameter_list=diameter_list,
                    shots_list=shots_list,
                    power_list=power_list,
                    rate_list=rate_list
                )
                st.session_state.results_df = results_df
            except Exception as e:
                st.error(f"An error occurred during calculation: {e}")

    # --- RESULTS DISPLAY ---
    if 'results_df' in st.session_state and st.session_state.app_mode == "Fluence (Energy Density)":
        st.markdown("---")
        st.markdown(f'<p class="results-header">Calculation Results</p>', unsafe_allow_html=True)

        df_to_display = st.session_state.results_df

        # Define column order and formatters
        ideal_order = [
            'Avg. Power (mW)', 'Rep. Rate (kHz)', 'Pulse Energy (µJ)',
            'Diameter (µm)', 'Number of Shots', 'Peak Fluence (J/cm²)',
            'Cumulative Dose (J/cm²)'
        ]
        cols_to_show = [col for col in ideal_order if col in df_to_display.columns]

        formatters = {
            'Pulse Energy (µJ)': '{:.3f}',
            'Peak Fluence (J/cm²)': '{:.3f}',
            'Cumulative Dose (J/cm²)': '{:.3f}',
            'Area (cm²)': '{:.4e}' # This column is calculated but not shown by default
        }

        st.dataframe(
            df_to_display[cols_to_show].style.format(formatters),
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Results as CSV",
            convert_df_to_csv(df_to_display[cols_to_show]),
            "fluence_calculator_results.csv",
            "text/csv",
            use_container_width=True
        )