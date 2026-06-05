import streamlit as st
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = next(BASE_DIR.glob("data/*.csv"), None)
if DATA_FILE is None:
    raise FileNotFoundError("Could not find dataset CSV in the data/ folder.")

df = pd.read_csv(DATA_FILE)

prob = 0.0

if prob > 0.7:

    st.error(
        "High Risk Customer"
    )

    st.write(
        """
        Recommended Action:
        - Loyalty Discount
        - Free Tech Support
        - Annual Contract Offer
        """
    )