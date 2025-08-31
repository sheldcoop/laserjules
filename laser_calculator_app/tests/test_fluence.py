import pytest
import pandas as pd
import numpy as np
from laser_calculator_app.core.fluence import calculate_fluence

def test_calculate_fluence_with_pulse_energy():
    """
    Tests the fluence calculation with direct pulse energy input.
    """
    energy_list = [1.6, 1.8]
    diameter_list = [10.0, 12.0]
    shots_list = [40, 50]

    result_df = calculate_fluence(
        energy_list=energy_list,
        diameter_list=diameter_list,
        shots_list=shots_list
    )

    assert isinstance(result_df, pd.DataFrame)
    assert 'Peak Fluence (J/cm²)' in result_df.columns
    assert 'Cumulative Dose (J/cm²)' in result_df.columns

    # Expected values calculated manually
    # For 1.6 µJ, 10 µm diameter:
    # Energy = 1.6e-6 J
    # Radius = 5e-4 cm
    # Area = pi * (5e-4)^2 = 7.854e-7 cm^2
    # Peak Fluence = 2 * 1.6e-6 / 7.854e-7 = 4.074 J/cm^2
    # Cumulative Dose = 4.074 * 40 = 162.96 J/cm^2
    assert np.isclose(result_df['Peak Fluence (J/cm²)'][0], 4.074, atol=1e-3)
    assert np.isclose(result_df['Cumulative Dose (J/cm²)'][0], 162.97, atol=1e-2)

def test_calculate_fluence_with_avg_power():
    """
    Tests the fluence calculation using average power and repetition rate.
    """
    power_list = [80.0, 90.0]
    rate_list = [50.0, 60.0]
    diameter_list = [10.0, 12.0]
    shots_list = [40, 50]

    result_df = calculate_fluence(
        power_list=power_list,
        rate_list=rate_list,
        diameter_list=diameter_list,
        shots_list=shots_list
    )

    assert 'Pulse Energy (µJ)' in result_df.columns
    # Expected energy = 80mW / 50kHz = 1.6 µJ
    assert np.isclose(result_df['Pulse Energy (µJ)'][0], 1.6)
    assert np.isclose(result_df['Peak Fluence (J/cm²)'][0], 4.074, atol=1e-3)

def test_mismatched_input_lengths_raise_error():
    """
    Tests that a ValueError is raised for mismatched input list lengths.
    """
    with pytest.raises(ValueError, match="Input lists must have the same number of data points."):
        calculate_fluence(
            energy_list=[1.6],
            diameter_list=[10.0, 12.0],
            shots_list=[40, 50]
        )

def test_missing_energy_or_power_raises_error():
    """
    Tests that a ValueError is raised if no energy or power data is provided.
    """
    with pytest.raises(ValueError, match="Either pulse energy or average power and repetition rate must be provided."):
        calculate_fluence(
            diameter_list=[10.0],
            shots_list=[40]
        )

def test_zero_diameter_handles_gracefully():
    """
    Tests that a diameter of 0 does not cause a division-by-zero error.
    """
    result_df = calculate_fluence(
        energy_list=[1.6],
        diameter_list=[0.0],
        shots_list=[40]
    )
    assert result_df['Peak Fluence (J/cm²)'][0] == 0.0
    assert result_df['Cumulative Dose (J/cm²)'][0] == 0.0
