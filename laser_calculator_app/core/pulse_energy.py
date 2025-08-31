def calculate_pulse_energy(average_power: float, repetition_rate: float) -> float:
    """
    Calculates the laser pulse energy.

    Args:
        average_power (float): The average power of the laser in Watts (W).
        repetition_rate (float): The repetition rate of the laser in Hertz (Hz).

    Returns:
        float: The pulse energy in Joules (J).

    Raises:
        ValueError: If repetition rate is zero, to prevent division by zero.
    """
    if repetition_rate == 0:
        raise ValueError("Repetition rate cannot be zero.")

    pulse_energy = average_power / repetition_rate
    return pulse_energy
