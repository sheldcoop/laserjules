# Laser Calculator

A web-based application providing a suite of calculators for laser processing applications. This tool is designed for scientists, engineers, and technicians working with lasers.

## Features

This application currently provides the following calculators:

*   **Pulse Energy Calculator:** Calculate the pulse energy from average power and repetition rate.
*   **Fluence Calculator:** Determine the peak fluence on a target material.
*   **Material Analyzer:** Explore the properties of different materials relevant to laser processing.

More calculators and features are planned for the future.

## Getting Started

To run this application locally, you will need Python 3.9+ installed.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd laser-calculator
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
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

The project is structured to be modular and maintainable:

```
laser_calculator/
├── laser_calculator_app/
│   ├── app.py                # Main Streamlit application
│   ├── core/                 # Core calculation logic
│   ├── modules/              # UI components for each calculator
│   └── tests/                # Unit tests for the core logic
└── README.md
```
