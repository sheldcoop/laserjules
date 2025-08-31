import pandas as pd
import numpy as np

# Constants should be managed centrally, but for now, let's define them here.
# In a larger refactor, we might move them to a dedicated constants file.
UJ_TO_J = 1e-6
UM_TO_CM = 1e-4
KHZ_TO_HZ = 1e3

def calculate_fluence(
    diameter_list: list[float],
    shots_list: list[int],
    energy_list: list[float] = None,
    power_list: list[float] = None,
    rate_list: list[float] = None,
) -> pd.DataFrame:
    """
    Calculates peak fluence and cumulative dose based on laser parameters.

    Args:
        diameter_list: List of beam spot diameters (µm).
        shots_list: List of number of shots.
        energy_list: List of pulse energies (µJ). Used if power_list is None.
        power_list: List of average powers (mW).
        rate_list: List of repetition rates (kHz).

    Returns:
        A pandas DataFrame with the calculation results.

    Raises:
        ValueError: If input lists have mismatched lengths or are missing.
    """
    if power_list and rate_list:
        if not (len(power_list) == len(rate_list) == len(diameter_list) == len(shots_list)):
            raise ValueError("Input lists must have the same number of data points.")
        # Calculate energy from power and repetition rate
        energy_list = [(p / r) for p, r in zip(power_list, rate_list)]
        df = pd.DataFrame({
            'Avg. Power (mW)': power_list,
            'Rep. Rate (kHz)': rate_list,
            'Pulse Energy (µJ)': energy_list,
            'Diameter (µm)': diameter_list,
            'Number of Shots': shots_list
        })
    elif energy_list:
        if not (len(energy_list) == len(diameter_list) == len(shots_list)):
            raise ValueError("Input lists must have the same number of data points.")
        df = pd.DataFrame({
            'Pulse Energy (µJ)': energy_list,
            'Diameter (µm)': diameter_list,
            'Number of Shots': shots_list
        })
    else:
        raise ValueError("Either pulse energy or average power and repetition rate must be provided.")

    df['Energy (J)'] = df['Pulse Energy (µJ)'] * UJ_TO_J
    df['Area (cm²)'] = np.pi * (((df['Diameter (µm)'] / 2) * UM_TO_CM) ** 2)

    # Avoid division by zero for area
    # A diameter of 0 would lead to an area of 0.
    df['Peak Fluence (J/cm²)'] = 0.0
    non_zero_area_mask = df['Area (cm²)'] != 0
    df.loc[non_zero_area_mask, 'Peak Fluence (J/cm²)'] = 2 * (df.loc[non_zero_area_mask, 'Energy (J)'] / df.loc[non_zero_area_mask, 'Area (cm²)'])

    df['Cumulative Dose (J/cm²)'] = df['Peak Fluence (J/cm²)'] * df['Number of Shots']

    return df
