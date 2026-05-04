import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score


DATA_PATH = "data/raw/UCI_Credit_Card.csv"
MODEL_PATH = "models/model_v1.joblib"
FEATURES_PATH = "models/features.json"
METRICS_PATH = "reports/metrics_v1.json"

TARGET_COL = "default.payment.next.month"

# загрузка датасета
def load_data(path):
    df = pd.read_csv(path)
    return df

# предобработка данных
def preprocessing(df):
    if "ID" in df.columns:
        df = df.drop(columns=["ID"])
    return df

# обучение модели, расчет метрик, сохранение признаков
def train_model(df):
    df = preprocessing(df)

    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    X_train, X_valid, y_train, y_valid = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_valid)
    y_proba = model.predict_proba(X_valid)[:, 1]

    metrics = {
        "f1": round(f1_score(y_valid, y_pred), 4),
        "precision": round(precision_score(y_valid, y_pred), 4),
        "recall": round(recall_score(y_valid, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_valid, y_proba), 4)
    }

    feature_names = list(X.columns)

    return model, metrics, feature_names

# сохраняем модель, список признаков, метрики
def save_model(model, metrics, feature_names):

    joblib.dump(model, MODEL_PATH)

    with open(FEATURES_PATH, "w", encoding="utf-8") as f:
        json.dump(feature_names, f, indent=2)

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)


def main():
    df = load_data(DATA_PATH)

    model, metrics, feature_names = train_model(df)

    save_model(model, metrics, feature_names)

    print("Model saved to:", MODEL_PATH)
    print("Features saved to:", FEATURES_PATH)
    print("Metrics saved to:", METRICS_PATH)
    print(metrics)


if __name__ == "__main__":
    main()