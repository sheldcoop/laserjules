import streamlit as st
import pandas as pd
import re

# --- CONSTANTS ---
UJ_TO_J = 1e-6
UM_TO_CM = 1e-4
KHZ_TO_HZ = 1e3

# --- HELPER FUNCTIONS ---
def parse_text_input(text_data: str) -> list[float]:
    """Parses a string of numbers separated by commas, spaces, or newlines."""
    if not text_data:
        return []
    items = re.split(r'[,\s\n]+', text_data.strip())
    return [float(item) for item in items if item]

@st.cache_data
def convert_df_to_csv(df: pd.DataFrame) -> bytes:
    """Converts a DataFrame to a UTF-8 encoded CSV file for downloading."""
    return df.to_csv(index=False).encode('utf-8')