import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = next(BASE_DIR.glob("data/*.csv"), None)
if DATA_FILE is None:
    raise FileNotFoundError("Could not find dataset CSV in the data/ folder.")

st.title("Customer Segmentation")

df = pd.read_csv(DATA_FILE)

# Segment Statistics

st.subheader("Customer Segments")

segment_counts = (
    df['Segment']
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "Segment",
    "Customers"
]

fig = px.bar(
    segment_counts,
    x="Segment",
    y="Customers",
    title="Customers per Segment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Scatter Plot

st.subheader(
    "Tenure vs Monthly Charges"
)

fig2 = px.scatter(
    df,
    x="tenure",
    y="MonthlyCharges",
    color="Segment",
    hover_data=[
        "TotalCharges"
    ],
    title="Customer Segmentation"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# Segment Churn

st.subheader(
    "Segment Wise Churn"
)

segment_churn = pd.crosstab(
    df['Segment'],
    df['Churn']
)

fig3 = px.bar(
    segment_churn,
    barmode='group',
    title="Segment-wise Churn"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# Segment Summary

st.subheader(
    "Segment Summary"
)

summary = df.groupby(
    'Segment'
).agg({
    'tenure':'mean',
    'MonthlyCharges':'mean',
    'TotalCharges':'mean'
}).round(2)

st.dataframe(summary)