import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from app.utils import load_model, load_scaler, load_features

st.set_page_config(page_title="Customer Churn Analytics", layout="wide")

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
MODELS_DIR = ROOT / "models"


def find_dataset():
    csv_files = sorted(DATA_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No dataset CSV file found in data/ folder.")
    return csv_files[0]


@st.cache_data
def load_data():
    dataset_file = find_dataset()
    df = pd.read_csv(dataset_file)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0.0)
    df["LTV"] = df["MonthlyCharges"] * df["tenure"]
    df["Avg_Revenue"] = df["TotalCharges"] / df["tenure"].replace({0: 1})
    df["Segment"] = df["tenure"].apply(lambda x: 0 if x <= 12 else 1 if x <= 24 else 2)
    return df


def build_feature_vector(inputs, feature_names):
    row = {name: 0.0 for name in feature_names}
    row["SeniorCitizen"] = 1.0 if inputs["SeniorCitizen"] else 0.0
    row["tenure"] = float(inputs["tenure"])
    row["MonthlyCharges"] = float(inputs["MonthlyCharges"])
    row["TotalCharges"] = float(inputs["TotalCharges"])
    row["LTV"] = float(inputs["MonthlyCharges"] * inputs["tenure"])
    row["Avg_Revenue"] = float(inputs["TotalCharges"] / max(inputs["tenure"], 1))
    row["Segment"] = float(0 if inputs["tenure"] <= 12 else 1 if inputs["tenure"] <= 24 else 2)

    for name in feature_names:
        if "_" not in name:
            continue
        field, value = name.split("_", 1)
        if field not in inputs:
            continue
        if str(inputs[field]) == value:
            row[name] = 1.0

    return np.array([row[name] for name in feature_names], dtype=float)


def format_percentage(value):
    return f"{value * 100:.2f}%"


def render_home(df):
    st.title("Telecom Customer Churn Analytics Dashboard")
    st.write("Predict churn, analyze customers, and generate retention strategies.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total customers", len(df))
    col2.metric("Churn rate", format_percentage(df["Churn"].eq("Yes").mean()))
    col3.metric("Average tenure", f"{df['tenure'].mean():.1f} months")

    st.subheader("Churn distribution")
    churn_count = df["Churn"].value_counts().reset_index()
    churn_count.columns = ["Churn", "Count"]
    fig = px.pie(churn_count, names="Churn", values="Count", title="Churn vs Retained")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Dataset preview")
    st.dataframe(df.head(10), use_container_width=True)


def render_kpi(df):
    st.title("Business KPI Dashboard")
    churn_rate = df["Churn"].eq("Yes").mean() * 100
    retention_rate = 100 - churn_rate
    avg_ltv = df["LTV"].mean()
    revenue_lost = df.loc[df["Churn"] == "Yes", "MonthlyCharges"].sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total customers", len(df))
    c2.metric("Churn rate", f"{churn_rate:.2f}%")
    c3.metric("Retention rate", f"{retention_rate:.2f}%")

    c4, c5, c6 = st.columns(3)
    c4.metric("Average LTV", f"${avg_ltv:.2f}")
    c5.metric("Revenue lost", f"${revenue_lost:.2f}")
    c6.metric("High risk customers", int((df["tenure"] <= 6).sum()))

    st.subheader("Tenure distribution")
    fig2 = px.histogram(df, x="tenure", nbins=25, title="Tenure distribution")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Monthly charges by churn")
    fig3 = px.box(df, x="Churn", y="MonthlyCharges", title="Monthly charges vs churn")
    st.plotly_chart(fig3, use_container_width=True)


def render_eda(df):
    st.title("Exploratory Data Analysis")
    st.write("Use this page to explore churn drivers and customer behavior.")

    st.subheader("Internet service churn")
    fig1 = px.histogram(df, x="InternetService", color="Churn", barmode="group")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Contract type churn")
    fig2 = px.histogram(df, x="Contract", color="Churn", barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Charges vs tenure")
    fig3 = px.scatter(df, x="tenure", y="MonthlyCharges", color="Churn", hover_data=["InternetService"])
    st.plotly_chart(fig3, use_container_width=True)


def render_prediction():
    st.title("Churn Prediction")
    st.write("Enter customer details to estimate churn probability.")

    model = None
    scaler = None
    features = None
    try:
        model = load_model()
        scaler = load_scaler()
        features = load_features()
    except Exception as exc:
        st.error(f"Could not load model files: {exc}")
        return

    with st.form("prediction_form"):
        left, right = st.columns(2)
        with left:
            gender = st.selectbox("Gender", ["Male", "Female"])
            senior = st.checkbox("Senior citizen")
            partner = st.selectbox("Partner", ["Yes", "No"])
            dependents = st.selectbox("Dependents", ["Yes", "No"])
            tenure = st.slider("Tenure (months)", 0, 72, 12)
            phone_service = st.selectbox("Phone service", ["Yes", "No"])
            multiple_lines = st.selectbox("Multiple lines", ["No phone service", "No", "Yes"])
            internet_service = st.selectbox("Internet service", ["DSL", "Fiber optic", "No"])
        with right:
            online_security = st.selectbox("Online security", ["No internet service", "No", "Yes"])
            online_backup = st.selectbox("Online backup", ["No internet service", "No", "Yes"])
            device_protection = st.selectbox("Device protection", ["No internet service", "No", "Yes"])
            tech_support = st.selectbox("Tech support", ["No internet service", "No", "Yes"])
            streaming_tv = st.selectbox("Streaming TV", ["No internet service", "No", "Yes"])
            streaming_movies = st.selectbox("Streaming movies", ["No internet service", "No", "Yes"])
            contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
            paperless = st.selectbox("Paperless billing", ["Yes", "No"])
            payment_method = st.selectbox(
                "Payment method",
                ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
            )
            monthly_charges = st.number_input("Monthly charges", min_value=0.0, value=50.0, step=1.0)
            total_charges = st.number_input("Total charges", min_value=0.0, value=float(tenure * monthly_charges), step=1.0)

        submitted = st.form_submit_button("Predict churn")

    if submitted:
        inputs = {
            "gender": gender,
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless,
            "PaymentMethod": payment_method,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
        }
        vector = build_feature_vector(inputs, features)
        scaled = scaler.transform(vector.reshape(1, -1))
        probability = model.predict_proba(scaled)[0][1]
        st.metric("Churn probability", format_percentage(probability))
        if probability > 0.80:
            st.error("High Risk Customer")
        elif probability > 0.60:
            st.warning("Medium Risk Customer")
        else:
            st.success("Low Risk Customer")

        if probability > 0.80:
            st.markdown(
                "**Retention recommendation:** offer annual contract discounts, free tech support, and loyalty rewards."
            )
        elif probability > 0.60:
            st.markdown(
                "**Retention recommendation:** use personalized offers, upgrade incentives, and special discounts."
            )
        else:
            st.markdown(
                "**Retention recommendation:** continue engagement with loyalty programs and regular check-ins."
            )


def main():
    df = load_data()
    page = st.sidebar.selectbox(
        "Choose page",
        ["Home", "KPI", "EDA", "Prediction"]
    )

    if page == "Home":
        render_home(df)
    elif page == "KPI":
        render_kpi(df)
    elif page == "EDA":
        render_eda(df)
    elif page == "Prediction":
        render_prediction()


if __name__ == "__main__":
    main()
