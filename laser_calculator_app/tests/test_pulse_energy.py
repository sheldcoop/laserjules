import pytest
from laser_calculator_app.core.pulse_energy import calculate_pulse_energy

def test_calculate_pulse_energy_valid():
    """Tests the pulse energy calculation for a valid case."""
    assert calculate_pulse_energy(10, 1000) == 0.01

def test_calculate_pulse_energy_zero_rep_rate():
    """Tests that a ValueError is raised for a zero repetition rate."""
    with pytest.raises(ValueError):
        calculate_pulse_energy(10, 0)
