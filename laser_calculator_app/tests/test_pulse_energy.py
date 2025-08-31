import pytest
import pandas as pd
import numpy as np
from laser_calculator_app.core.pulse_energy import calculate_pulse_energy

def test_calculate_pulse_energy_basic():
    """
    Tests the basic pulse energy calculation.
    """
    power_list = [80.0, 100.0]
    rate_list = [50.0, 100.0]

    result_df = calculate_pulse_energy(power_list, rate_list)

    assert isinstance(result_df, pd.DataFrame)
    assert 'Pulse Energy (µJ)' in result_df.columns
    assert np.isclose(result_df['Pulse Energy (µJ)'][0], 1.6)
    assert np.isclose(result_df['Pulse Energy (µJ)'][1], 1.0)

def test_mismatched_lengths_raise_error():
    """
    Tests that a ValueError is raised for mismatched input list lengths.
    """
    with pytest.raises(ValueError, match="Input lists must have the same number of data points."):
        calculate_pulse_energy([80.0], [50.0, 100.0])

def test_empty_lists_raise_error():
    """
    Tests that a ValueError is raised for empty input lists.
    """
    with pytest.raises(ValueError, match="Input lists cannot be empty."):
        calculate_pulse_energy([], [])

def test_zero_repetition_rate_raises_error():
    """
    Tests that a ValueError is raised if repetition rate is zero.
    """
    with pytest.raises(ValueError, match="Repetition rate cannot be zero."):
        calculate_pulse_energy([80.0], [0.0])
