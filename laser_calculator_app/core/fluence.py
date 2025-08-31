import math

def calculate_fluence(pulse_energy: float, beam_diameter: float) -> float:
    """
    Calculates the laser fluence for a circular beam.

    Args:
        pulse_energy (float): The pulse energy in Joules (J).
        beam_diameter (float): The diameter of the laser beam in meters (m).

    Returns:
        float: The fluence in Joules per square meter (J/m^2).

    Raises:
        ValueError: If beam diameter is zero or negative.
    """
    if beam_diameter <= 0:
        raise ValueError("Beam diameter must be a positive value.")

    beam_radius = beam_diameter / 2
    area = math.pi * (beam_radius ** 2)

    fluence = pulse_energy / area
    return fluence
