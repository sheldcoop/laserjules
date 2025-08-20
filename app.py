import streamlit as st
import numpy as np
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Laser Process Calculator")

# --- CUSTOM CSS (Simplified and Refined) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        body { font-family: 'Inter', sans-serif; }
        [data-testid="stSidebar"] { padding: 20px; }
        h1 { padding-top: 20px; padding-bottom: 10px; }

        /* Style all buttons in the sidebar for a consistent look */
        [data-testid="stSidebar"] .stButton button {
            text-align: left !important;
            font-weight: 500;
            padding: 10px 15px;
            border-radius: 8px;
        }

        /* Data Table & Results Styling */
        .stDataFrame thead th { background-color: #e9ecef; color: #212529; font-weight: 600; }
        .results-header { font-size: 22px; font-weight: 600; color: #16a34a; }
        hr { margin: 2rem 0; border-color: #e0e0e0; }
    </style>
""", unsafe_allow_html=True)

# --- Initialize session state ---
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Pulse Energy"

# --- SIDEBAR WITH THE ROBUST BUTTON-BASED NAVIGATION ---
with st.sidebar:
    st.header("Calculator Mode")

    # Determine which button is primary (red) and which is secondary (gray)
    pulse_btn_type = "primary" if st.session_state.app_mode == "Pulse Energy" else "secondary"
    fluence_btn_type = "primary" if st.session_state.app_mode == "Fluence" else "secondary"

    if st.button("Pulse Energy", use_container_width=True, type=pulse_btn_type):
        st.session_state.app_mode = "Pulse Energy"
        st.session_state.results_df = None # Clear results on mode switch
        st.rerun()

    if st.button("Fluence (Energy Density)", use_container_width=True, type=fluence_btn_type):
        st.session_state.app_mode = "Fluence"
        st.session_state.results_df = None # Clear results on mode switch
        st.rerun()

# --- MAIN PANEL ---
st.title("Advanced Laser Process Calculator")

if 'results_df' not in st.session_state:
    st.session_state.results_df = None

if st.session_state.app_mode == "Pulse Energy":
    st.header("Calculate Pulse Energy")
    st.markdown("---")
    with st.expander("Show Formula"):
        st.latex(r'''\text{Pulse Energy (µJ)} = \frac{\text{Average Power (mW)}}{\text{Repetition Rate (kHz)}}''')
    
    avg_power_str = st.text_input("Average Power (mW)", placeholder="e.g., 80, 90, 140")
    rep_rate_str = st.text_input("Repetition Rate (kHz)", placeholder="e.g., 50, 50, 50")
    
    if st.button("Calculate Pulse Energy", type="primary"):
        # ... (calculation logic remains the same) ...
        if not avg_power_str or not rep_rate_str:
            st.warning("Please enter values in all fields.")
        else:
            try:
                power_list = [float(p.strip()) for p in avg_power_str.split(',')]
                rate_list = [float(r.strip()) for r in rep_rate_str.split(',')]
                if len(power_list) == len(rate_list):
                    df = pd.DataFrame({'Avg. Power (mW)': power_list, 'Rep. Rate (kHz)': rate_list})
                    df['Pulse Energy (µJ)'] = df['Avg. Power (mW)'] / df['Rep. Rate (kHz)']
                    st.session_state.results_df = df
                else:
                    st.warning("Please enter the same number of data points for all inputs.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

elif st.session_state.app_mode == "Fluence":
    st.header("Calculate Fluence & Cumulative Dose")
    st.markdown("---")
    with st.expander("Show Formulas"):
        st.latex(r'''\text{Peak Fluence (J/cm²)} = 2 \times \frac{\text{Pulse Energy (J)}}{\text{Area (cm²)}}''')
    
    pulse_energy_str = st.text_input("Pulse Energy (µJ)", placeholder="e.g., 1.6, 1.8, 2.8")
    diameter_str = st.text_input("Beam Spot Diameter (µm)", placeholder="e.g., 9, 10, 14")
    shots_str = st.text_input("Number of Shots", placeholder="e.g., 22, 22, 22")
    
    if st.button("Calculate Fluence", type="primary"):
        # ... (calculation logic remains the same) ...
        if not pulse_energy_str or not diameter_str or not shots_str:
            st.warning("Please enter values in all fields.")
        else:
            try:
                energy_list = [float(e.strip()) for e in pulse_energy_str.split(',')]
                diameter_list = [float(d.strip()) for d in diameter_str.split(',')]
                shots_list = [int(s.strip()) for s in shots_str.split(',')]
                if not (len(energy_list) == len(diameter_list) == len(shots_list)):
                    st.warning("Please enter the same number of data points for all inputs.")
                else:
                    df = pd.DataFrame({'Pulse Energy (µJ)': energy_list, 'Diameter (µm)': diameter_list, 'Number of Shots': shots_list})
                    df['Energy (J)'] = df['Pulse Energy (µJ)'] * 1e-6
                    df['Area (cm²)'] = np.pi * (((df['Diameter (µm)'] / 2) * 1e-4) ** 2)
                    df['Peak Fluence (J/cm²)'] = 2 * (df['Energy (J)'] / df['Area (cm²)'])
                    df['Cumulative Dose (J/cm²)'] = df['Peak Fluence (J/cm²)'] * df['Number of Shots']
                    st.session_state.results_df = df[['Pulse Energy (µJ)', 'Diameter (µm)', 'Number of Shots', 'Peak Fluence (J/cm²)', 'Cumulative Dose (J/cm²)']]
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- UNIVERSAL RESULTS DISPLAY ---
if st.session_state.results_df is not None:
    st.markdown("---")
    st.markdown(f'<p class="results-header">Calculation Results</p>', unsafe_allow_html=True)
    st.dataframe(
        st.session_state.results_df.style.format(precision=3), 
        use_container_width=True,
        hide_index=True
    )