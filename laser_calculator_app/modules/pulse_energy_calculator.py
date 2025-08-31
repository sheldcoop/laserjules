import streamlit as st
from laser_calculator_app.core.pulse_energy import calculate_pulse_energy

def render():
    """Renders the Pulse Energy Calculator UI."""
    st.header("Pulse Energy Calculator")

    st.markdown("""
    Calculate the pulse energy of a laser given its average power and repetition rate.
    """)

    # --- INPUTS ---
    col1, col2 = st.columns(2)
    with col1:
        avg_power = st.number_input("Average Power (W)", min_value=0.0, value=10.0, step=1.0)
    with col2:
        rep_rate = st.number_input("Repetition Rate (Hz)", min_value=1, value=1000, step=100)

    # --- CALCULATION ---
    if st.button("Calculate Pulse Energy"):
        try:
            pulse_energy = calculate_pulse_energy(avg_power, rep_rate)
            st.success(f"**Pulse Energy:** {pulse_energy:.6f} J")
            st.info(f"Which is equivalent to {pulse_energy * 1e3:.3f} mJ or {pulse_energy * 1e6:.3f} µJ.")
        except ValueError as e:
            st.error(e)
