import sys
import os
import pandas as pd
import numpy as np
import pytest

# Add the app directory to the system path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'laser_calculator_app')))

from core.calculations import calculate_fluence_df

# --- Test Cases ---

def test_basic_fluence_calculation():
    """
    Tests the fluence calculation with a single, simple set of inputs.
    """
    energy_list = [10.0]  # µJ
    diameter_list = [20.0]  # µm
    shots_list = [1]

    results_df = calculate_fluence_df(energy_list, diameter_list, shots_list)

    assert isinstance(results_df, pd.DataFrame)
    assert not results_df.empty
    assert 'Peak Fluence (J/cm²)' in results_df.columns

    # Expected values
    # Energy = 10 µJ = 1e-5 J
    # Radius = 10 µm = 1e-3 cm
    # Area = pi * (1e-3)^2 = 3.14159e-6 cm²
    # Peak Fluence = 2 * Energy / Area = 2 * 1e-5 / 3.14159e-6 = 6.366 J/cm²
    expected_fluence = 6.366

    # Check if the calculated value is close to the expected value
    assert np.isclose(results_df['Peak Fluence (J/cm²)'].iloc[0], expected_fluence, rtol=1e-3)

def test_fluence_with_power_and_rate():
    """
    Tests the fluence calculation when providing average power and rep rate.
    """
    power_list = [1000.0] # mW
    rate_list = [100.0] # kHz
    diameter_list = [20.0] # µm
    shots_list = [5]

    # Energy per pulse = 1000 mW / 100 kHz = 10 µJ
    energy_list = [p / r for p, r in zip(power_list, rate_list)]

    results_df = calculate_fluence_df(energy_list, diameter_list, shots_list, power_list, rate_list)

    assert 'Avg. Power (mW)' in results_df.columns
    assert np.isclose(results_df['Pulse Energy (µJ)'].iloc[0], 10.0)

    # Fluence should be the same as the basic test
    expected_fluence = 6.366
    assert np.isclose(results_df['Peak Fluence (J/cm²)'].iloc[0], expected_fluence, rtol=1e-3)

    # Check cumulative dose
    expected_dose = expected_fluence * 5
    assert np.isclose(results_df['Cumulative Dose (J/cm²)'].iloc[0], expected_dose, rtol=1e-3)

def test_multiple_data_points():
    """
    Tests the function's ability to handle multiple data points in one batch.
    """
    energy_list = [10.0, 20.0]
    diameter_list = [20.0, 25.0]
    shots_list = [1, 2]

    results_df = calculate_fluence_df(energy_list, diameter_list, shots_list)

    assert len(results_df) == 2

    # Check first row (same as basic test)
    expected_fluence_1 = 6.366
    assert np.isclose(results_df['Peak Fluence (J/cm²)'].iloc[0], expected_fluence_1, rtol=1e-3)

    # Check second row
    # Energy = 20 µJ = 2e-5 J
    # Radius = 12.5 µm = 1.25e-3 cm
    # Area = pi * (1.25e-3)^2 = 4.9087e-6 cm²
    # Peak Fluence = 2 * 2e-5 / 4.9087e-6 = 8.149 J/cm²
    expected_fluence_2 = 8.149
    assert np.isclose(results_df['Peak Fluence (J/cm²)'].iloc[1], expected_fluence_2, rtol=1e-3)

    # Check cumulative dose for the second row
    expected_dose_2 = expected_fluence_2 * 2
    assert np.isclose(results_df['Cumulative Dose (J/cm²)'].iloc[1], expected_dose_2, rtol=1e-3)
