import pytest
import math
from laser_calculator_app.core.fluence import calculate_fluence

def test_calculate_fluence_valid():
    """Tests the fluence calculation for a valid case."""
    pulse_energy = 0.01  # J
    beam_diameter = 0.001  # m
    expected_area = math.pi * (beam_diameter / 2) ** 2
    expected_fluence = pulse_energy / expected_area
    assert calculate_fluence(pulse_energy, beam_diameter) == pytest.approx(expected_fluence)

def test_calculate_fluence_zero_diameter():
    """Tests that a ValueError is raised for a zero beam diameter."""
    with pytest.raises(ValueError):
        calculate_fluence(0.01, 0)

def test_calculate_fluence_negative_diameter():
    """Tests that a ValueError is raised for a negative beam diameter."""
    with pytest.raises(ValueError):
        calculate_fluence(0.01, -1)
