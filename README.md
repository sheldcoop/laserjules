# Laser Processing Dashboard

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36.0-red.svg)](https://streamlit.io)
[![Pytest](https://img.shields.io/badge/Tests-passing-brightgreen.svg)](https://pytest.org)

A web-based dashboard providing a suite of professional calculators for laser processing applications. This tool is designed for scientists, engineers, and technicians working with lasers who need to perform quick and accurate calculations for various process parameters.

## Features

This application provides a collection of specialized calculators, including:

*   **Core Workflow Tools:**
    *   **Material Analyzer:** Analyze material properties relevant to laser processing.
    *   **Process Recommender:** Get recommendations for laser processes based on your material and desired outcome.
    *   **Microvia Process Simulator:** Visualize and simulate the process of drilling microvias.
*   **Advanced Analysis:**
    *   **Liu Plot Analyzer:** Generate and analyze Liu plots for determining laser damage thresholds.
    *   **Thermal Effects Calculator:** Model and calculate the thermal effects of laser interaction with materials.
*   **Fundamental Calculators:**
    *   **Pulse Energy Calculator:** Calculate the pulse energy from average power and repetition rate.
    *   **Fluence Calculator:** Determine the peak fluence and cumulative dose on a target material.
    *   **Mask Finder:** Utilities for finding and specifying masks.

## Getting Started

To run this application locally, you will need Python 3.9+ installed.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd laser_dashboard
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source ven v/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r laser_calculator_app/requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run laser_calculator_app/app.py
    ```
    The application should now be open in your web browser.

## Project Structure

The project is structured to separate concerns, making it modular and easy to maintain.

```
laser_dashboard/
├── laser_calculator_app/
│   ├── app.py                # Main Streamlit application, handles navigation
│   ├── core/                 # Core business logic (calculations)
│   │   ├── __init__.py
│   │   ├── fluence.py
│   │   └── pulse_energy.py
│   ├── modules/              # UI components for each calculator
│   │   ├── __init__.py
│   │   ├── fluence_calculator.py
│   │   └── ...
│   ├── tests/                # Unit tests for the core logic
│   │   ├── __init__.py
│   │   └── test_fluence.py
│   └── utils.py              # Utility functions
└── README.md
```

*   **`app.py`**: The main entry point for the Streamlit application.
*   **`core/`**: Contains all the core calculation logic. Each file corresponds to a specific calculator and contains functions that are independent of the Streamlit UI.
*   **`modules/`**: Contains the Streamlit UI code for each calculator. Each file in this directory is responsible for rendering the inputs, buttons, and results for a specific tool.
*   **`tests/`**: Contains unit tests for the functions in the `core/` directory. We use `pytest` for testing.
*   **`utils.py`**: Contains helper functions that are used across multiple modules.

## Contributing

Contributions are welcome! If you want to add a new calculator, please follow these steps:

1.  **Add the core logic:** Create a new Python file in the `laser_calculator_app/core/` directory. Add your calculation function(s) to this file. Remember to include error handling.
2.  **Write tests:** Create a corresponding test file in `laser_calculator_app/tests/` and write unit tests for your core logic.
3.  **Create the UI module:** Create a new file in `laser_calculator_app/modules/` that will contain the Streamlit UI for your calculator. Import your core logic function and call it to perform the calculation.
4.  **Add it to the app:** Open `laser_calculator_app/app.py` and add your new module to the `TOOL_CATEGORIES` dictionary.
5.  **Submit a pull request.**
