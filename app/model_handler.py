import json
import joblib
import pandas as pd

MODEL_PATH = "models/model_v1.joblib"
FEATURES_PATH = "models/features.json"

# загрузка модели
def load_model():
    model = joblib.load(MODEL_PATH)
    return model

# загрузка признаков
def load_features():
    with open(FEATURES_PATH, "r", encoding="utf-8") as f:
        features = json.load(f)
    return features

model = load_model()
feature_names = load_features()


def predict_default(input_data):
    # проверяем корректность признаков
    missing_features = []
    for feature in feature_names:
        if feature not in input_data:
            missing_features.append(feature)

    if missing_features:
        raise ValueError(f"Missing features: {missing_features}")

    data = pd.DataFrame([input_data], columns=feature_names)
    prediction = int(model.predict(data)[0])
    probability = float(model.predict_proba(data)[0][1])

    return {
        "prediction": prediction,
        "probability": round(probability, 4),
    }