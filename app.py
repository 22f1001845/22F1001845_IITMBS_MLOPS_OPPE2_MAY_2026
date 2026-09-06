from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from datetime import datetime, timezone

# Load trained model
model = joblib.load("heart_disease_model.joblib")

app = FastAPI(
    title="Heart Disease Prediction API",
    description="Production-ready heart disease prediction API",
    version="1.0.0"
)


class PatientData(BaseModel):
    age: int
    gender: str
    cp: int
    trestbps: float
    chol: float
    fbs: int
    restecg: int
    thalach: float
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int


@app.get("/")
def home():
    return {
        "message": "Heart Disease Prediction API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.post("/predict")
def predict(patient: PatientData):

    input_data = pd.DataFrame([patient.model_dump()])

    prediction = int(model.predict(input_data)[0])
    probability = float(model.predict_proba(input_data)[0][1])

    return {
        "prediction": prediction,
        "prediction_label": (
            "Heart Disease" if prediction == 1
            else "No Heart Disease"
        ),
        "probability": round(probability, 4),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
