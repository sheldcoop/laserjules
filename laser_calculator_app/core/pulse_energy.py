import pandas as pd

def calculate_pulse_energy(
    power_list: list[float],
    rate_list: list[float]
) -> pd.DataFrame:
    """
    Calculates pulse energy from average power and repetition rate.

    Args:
        power_list: A list of average power values in mW.
        rate_list: A list of repetition rate values in kHz.

    Returns:
        A pandas DataFrame containing the original inputs and the calculated
        pulse energy in µJ.

    Raises:
        ValueError: If the input lists are empty or have mismatched lengths.
    """
    if not power_list or not rate_list:
        raise ValueError("Input lists cannot be empty.")

    if len(power_list) != len(rate_list):
        raise ValueError("Input lists must have the same number of data points.")

    # Check for zero in repetition rate to avoid division by zero
    if any(r == 0 for r in rate_list):
        raise ValueError("Repetition rate cannot be zero.")

    df = pd.DataFrame({
        'Avg. Power (mW)': power_list,
        'Rep. Rate (kHz)': rate_list
    })

    df['Pulse Energy (µJ)'] = df['Avg. Power (mW)'] / df['Rep. Rate (kHz)']

    return df
