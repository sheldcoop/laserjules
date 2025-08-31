MATERIALS = {
    "Acrylic (PMMA)": {
        "thermal_conductivity": 0.2,  # W/m.K
        "specific_heat": 1466,  # J/kg.K
        "melting_point": 160,  # °C
        "density": 1180,  # kg/m³
        "reflectivity": 0.04,  # unitless
        "absorption_coefficient": 100,  # m⁻¹
    },
    "Stainless Steel (304)": {
        # Placeholder values
        "thermal_conductivity": 16.2,
        "specific_heat": 500,
        "melting_point": 1400,
        "density": 8000,
        "reflectivity": 0.6,
        "absorption_coefficient": 1e7,
    },
    "Aluminum": {
        # Placeholder values
        "thermal_conductivity": 237,
        "specific_heat": 900,
        "melting_point": 660,
        "density": 2700,
        "reflectivity": 0.9,
        "absorption_coefficient": 1e7,
    },
    "Copper": {
        # Placeholder values
        "thermal_conductivity": 401,
        "specific_heat": 385,
        "melting_point": 1084,
        "density": 8960,
        "reflectivity": 0.95,
        "absorption_coefficient": 1e7,
    },
    "Silicon": {
        # Placeholder values
        "thermal_conductivity": 149,
        "specific_heat": 700,
        "melting_point": 1414,
        "density": 2330,
        "reflectivity": 0.3,
        "absorption_coefficient": 1e5,
    },
}

def get_material_properties(material_name: str) -> dict:
    """
    Retrieves the properties of a given material.

    Args:
        material_name (str): The name of the material.

    Returns:
        dict: A dictionary containing the properties of the material.

    Raises:
        ValueError: If the material is not found in the database.
    """
    if material_name not in MATERIALS:
        raise ValueError(f"Material '{material_name}' not found in the database.")

    return MATERIALS[material_name]
