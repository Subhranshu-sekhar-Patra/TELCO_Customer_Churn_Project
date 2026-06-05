import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = next(BASE_DIR.glob("data/*.csv"), None)
if DATA_FILE is None:
    raise FileNotFoundError("Could not find dataset CSV in the data/ folder.")

st.title(
    "Business KPI Dashboard"
)

df = pd.read_csv(DATA_FILE)

# ===========================
# KPI CALCULATIONS
# ===========================

total_customers = len(df)

churn_rate = (
    (df['Churn'] == 'Yes').mean()
    * 100
)

retention_rate = (
    100 - churn_rate
)

avg_ltv = (
    df['MonthlyCharges']
    * df['tenure']
).mean()

revenue_lost = df[
    df['Churn'] == 'Yes'
]['MonthlyCharges'].sum()

high_risk = len(
    df[
        df['Risk_Probability']
        > 0.7
    ]
)

# ===========================
# KPI CARDS
# ===========================

col1,col2,col3 = st.columns(3)

col1.metric(
    "Total Customers",
    total_customers
)

col2.metric(
    "Churn Rate",
    f"{churn_rate:.2f}%"
)

col3.metric(
    "Retention Rate",
    f"{retention_rate:.2f}%"
)

col4,col5,col6 = st.columns(3)

col4.metric(
    "Average LTV",
    f"${avg_ltv:.2f}"
)

col5.metric(
    "Revenue Lost",
    f"${revenue_lost:.2f}"
)

col6.metric(
    "High Risk Customers",
    high_risk
)

# ===========================
# PIE CHART
# ===========================

st.subheader(
    "Customer Status"
)

status_df = pd.DataFrame({
    "Status":[
        "Retained",
        "Churned"
    ],
    "Count":[
        total_customers -
        df['Churn'].eq('Yes').sum(),

        df['Churn'].eq('Yes').sum()
    ]
})

fig1 = px.pie(
    status_df,
    values='Count',
    names='Status',
    title='Retention vs Churn'
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ===========================
# TENURE HISTOGRAM
# ===========================

st.subheader(
    "Tenure Distribution"
)

fig2 = px.histogram(
    df,
    x='tenure',
    nbins=30,
    title='Tenure Distribution'
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ===========================
# CHURN BY CONTRACT
# ===========================

st.subheader(
    "Contract Type Analysis"
)

contract = pd.crosstab(
    df['Contract'],
    df['Churn']
)

fig3 = px.bar(
    contract,
    barmode='group',
    title='Contract vs Churn'
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ===========================
# MONTHLY CHARGES
# ===========================

st.subheader(
    "Monthly Charges Analysis"
)

fig4 = px.box(
    df,
    x='Churn',
    y='MonthlyCharges',
    title='Monthly Charges vs Churn'
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ===========================
# HIGH RISK CUSTOMERS
# ===========================

st.subheader(
    "High Risk Customers"
)

risk_df = df[
    df['Risk_Probability']
    > 0.7
]

st.dataframe(
    risk_df.head(20)
)