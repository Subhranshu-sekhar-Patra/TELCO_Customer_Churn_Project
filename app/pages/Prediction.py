import pickle
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
model = pickle.load(
    open(
        BASE_DIR / "models" / "best_model.pkl",
        "rb"
    )
)

scaler = pickle.load(
    open(
        BASE_DIR / "models" / "scaler.pkl",
        "rb"
    )
)

def predict_probability(input_data):
    scaled_data = scaler.transform(input_data)
    return model.predict_proba(scaled_data)[0][1]
