import pickle
import pandas as pd

# ------------------------
# Load Models
# ------------------------

def load_model():

    model = pickle.load(
        open(
            "models/best_model.pkl",
            "rb"
        )
    )

    return model


def load_scaler():

    scaler = pickle.load(
        open(
            "models/scaler.pkl",
            "rb"
        )
    )

    return scaler


def load_kmeans():

    kmeans = pickle.load(
        open(
            "models/kmeans.pkl",
            "rb"
        )
    )

    return kmeans


def load_features():

    features = pickle.load(
        open(
            "models/feature_columns.pkl",
            "rb"
        )
    )

    return features


# ------------------------
# Retention Strategy
# ------------------------

def retention_strategy(probability):

    if probability > 0.80:

        return """
        HIGH RISK CUSTOMER

        Recommendations:
        - Offer annual contract discount
        - Free tech support
        - Dedicated customer support
        - Loyalty rewards
        """

    elif probability > 0.60:

        return """
        MEDIUM RISK CUSTOMER

        Recommendations:
        - Personalized offers
        - Upgrade plans
        - Promotional discounts
        """

    else:

        return """
        LOW RISK CUSTOMER

        Recommendations:
        - Continue engagement
        - Loyalty programs
        """


# ------------------------
# LTV Calculator
# ------------------------

def calculate_ltv(monthly_charges, tenure):

    return monthly_charges * tenure