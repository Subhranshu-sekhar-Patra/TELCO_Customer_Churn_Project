import pickle

model = pickle.load(
    open(
        "models/best_model.pkl",
        "rb"
    )
)

scaler = pickle.load(
    open(
        "models/scaler.pkl",
        "rb"
    )
)

def predict_probability(input_data):
    scaled_data = scaler.transform(input_data)
    return model.predict_proba(scaled_data)[0][1]
