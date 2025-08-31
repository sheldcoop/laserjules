import streamlit as st
import pandas as pd
from laser_calculator_app.core.material_analyzer import get_material_properties, MATERIALS

def render():
    """Renders the Material Analyzer UI."""
    st.header("Material Analyzer")

    st.markdown("""
    Explore the properties of different materials relevant to laser processing.
    """)

    # --- MATERIAL SELECTION ---
    material_name = st.selectbox("Select a Material", list(MATERIALS.keys()))

    # --- DISPLAY PROPERTIES ---
    if material_name:
        try:
            properties = get_material_properties(material_name)

            # Format the properties for display
            df = pd.DataFrame.from_dict(properties, orient='index', columns=['Value'])
            df.index.name = "Property"
            df = df.reset_index()

            # Add units to the table
            units = {
                "thermal_conductivity": "W/m.K",
                "specific_heat": "J/kg.K",
                "melting_point": "°C",
                "density": "kg/m³",
                "reflectivity": "",
                "absorption_coefficient": "m⁻¹",
            }
            df['Unit'] = df['Property'].map(units)

            st.table(df)

        except ValueError as e:
            st.error(e)
