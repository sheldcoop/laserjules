import streamlit as st
from laser_calculator_app.core.fluence import calculate_fluence

def render():
    """Renders the Fluence Calculator UI."""
    st.header("Fluence Calculator")

    st.markdown("""
    Calculate the laser fluence (energy density) for a circular beam.
    """)

    # --- INPUTS ---
    col1, col2 = st.columns(2)
    with col1:
        pulse_energy = st.number_input("Pulse Energy (J)", min_value=0.0, value=0.01, step=0.001, format="%.6f")
    with col2:
        beam_diameter_mm = st.number_input("Beam Diameter (mm)", min_value=0.0, value=1.0, step=0.1)

    # --- CALCULATION ---
    if st.button("Calculate Fluence"):
        try:
            # Convert beam diameter to meters for the core function
            beam_diameter_m = beam_diameter_mm / 1000

            fluence = calculate_fluence(pulse_energy, beam_diameter_m)

            # Convert fluence to J/cm^2 for display
            fluence_j_cm2 = fluence / 10000

            st.success(f"**Fluence:** {fluence_j_cm2:.4f} J/cm²")
            st.info(f"Which is equivalent to {fluence:.2f} J/m².")
            
        except ValueError as e:
            st.error(e)
