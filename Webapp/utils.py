import os
import joblib
import numpy as np
import pandas as pd
import logging

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------- PATH SETUP ----------------
# utils.py is inside Webapp/
# Models folder is one level above
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "Models", "stroke_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "Models", "scaler.pkl")

# ---------------- LOAD MODEL & SCALER ----------------
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    logging.info("✅ Model and scaler loaded successfully.")

except Exception as e:
    logging.error(f"❌ Error loading model or scaler: {e}")
    model, scaler = None, None


# ---------------- PREPROCESS INPUT ----------------
def preprocess_input(data):
    """
    Preprocess input data with correct feature order and scaling
    Feature order MUST match training exactly
    """
    try:
        if scaler is None:
            raise ValueError("❌ Scaler not loaded!")

        feature_names = [
            'gender',
            'age',
            'hypertension',
            'heart_disease',
            'ever_married',
            'work_type',
            'Residence_type',
            'avg_glucose_level',
            'bmi',
            'smoking_status'
        ]

        # Convert input list to DataFrame
        data_df = pd.DataFrame([data], columns=feature_names)

        # Apply same scaler used during training
        scaled_data = scaler.transform(data_df)

        return scaled_data

    except Exception as e:
        logging.error(f"❌ Error in preprocessing: {e}")
        raise


# ---------------- PREDICTION ----------------
def predict_stroke(input_data):
    """
    Predict stroke risk using probability-based threshold
    """
    try:
        if model is None:
            raise ValueError("❌ Model not loaded!")

        # Preprocess input
        processed_data = preprocess_input(input_data)

        # Get probability for stroke class (class = 1)
        proba = model.predict_proba(processed_data)[0][1]

        # Medical-safe threshold
        prediction = 1 if proba >= 0.3 else 0

        logging.info(f"✅ Stroke probability: {proba:.3f}")
        logging.info(f"✅ Final prediction (0=Low, 1=High): {prediction}")

        return prediction

    except Exception as e:
        logging.error(f"❌ Prediction error: {e}")
        return -1
