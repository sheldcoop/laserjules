import pandas as pd
import numpy as np

# --- CONSTANTS ---
# It's good practice to define constants where they are used
# or in a dedicated config/constants file.
# For now, we define them here for clarity.
UJ_TO_J = 1e-6
UM_TO_CM = 1e-4

def calculate_fluence_df(
    energy_list: list[float],
    diameter_list: list[float],
    shots_list: list[int],
    power_list: list[float] | None = None,
    rate_list: list[float] | None = None
) -> pd.DataFrame:
    """
    Calculates peak fluence and cumulative dose and returns a DataFrame.

    Args:
        energy_list: A list of pulse energies in microjoules (µJ).
        diameter_list: A list of beam spot diameters in micrometers (µm).
        shots_list: A list of the number of shots.
        power_list: An optional list of average powers in milliwatts (mW).
        rate_list: An optional list of repetition rates in kilohertz (kHz).

    Returns:
        A pandas DataFrame containing all inputs and calculated results.
    """
    if power_list and rate_list:
        df = pd.DataFrame({
            'Avg. Power (mW)': power_list,
            'Rep. Rate (kHz)': rate_list,
            'Pulse Energy (µJ)': energy_list,
            'Diameter (µm)': diameter_list,
            'Number of Shots': shots_list
        })
    else:
        df = pd.DataFrame({
            'Pulse Energy (µJ)': energy_list,
            'Diameter (µm)': diameter_list,
            'Number of Shots': shots_list
        })

    # Perform calculations
    df['Energy (J)'] = df['Pulse Energy (µJ)'] * UJ_TO_J
    df['Area (cm²)'] = np.pi * (((df['Diameter (µm)'] / 2) * UM_TO_CM) ** 2)

    # Peak Fluence for a Gaussian beam is 2 * Energy / Area
    df['Peak Fluence (J/cm²)'] = 2 * (df['Energy (J)'] / df['Area (cm²)'])
    df['Cumulative Dose (J/cm²)'] = df['Peak Fluence (J/cm²)'] * df['Number of Shots']

    return df
