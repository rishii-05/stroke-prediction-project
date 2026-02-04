import joblib
import numpy as np
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define model and scaler paths
MODEL_PATH = "C:/Users/chigu/Desktop/stroke_prediction_project/Models/stroke_model.pkl"
SCALER_PATH = "C:/Users/chigu/Desktop/stroke_prediction_project/Models/scaler.pkl"

try:
    # Load trained model and scaler
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    logging.info("Model and scaler loaded successfully.")

    # Debugging: Ensure scaler parameters match training
    print("Scaler Mean:", scaler.mean_)
    print("Scaler Variance:", scaler.var_)

except Exception as e:
    logging.error(f"Error loading model or scaler: {e}")
    model, scaler = None, None

def preprocess_input(data):
    """Preprocess input data with correct feature order and scaling."""
    try:
        if scaler is None:
            raise ValueError("❌ Scaler not loaded! Check scaler.pkl file.")

        # Ensure correct feature order (MUST match training dataset order)
        feature_names = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 
                         'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status']

        # Convert input to DataFrame with correct column names
        data_df = pd.DataFrame([data], columns=feature_names)

        # Apply StandardScaler
        scaled_data = scaler.transform(data_df)

        return scaled_data

    except Exception as e:
        logging.error(f"❌ Error in preprocessing: {e}")
        raise

def predict_stroke(input_data):
    """Predict stroke risk using the trained model."""
    try:
        if model is None:
            raise ValueError("❌ Model not loaded! Check model.pkl file.")

        # Preprocess input
        processed_data = preprocess_input(input_data)

        # Predict (should now work correctly)
        prediction = model.predict(processed_data)[0]

        return int(prediction)  # Ensure output is 0 or 1

    except Exception as e:
        logging.error(f"❌ Prediction error: {e}")
        return -1  # Return -1 in case of an error
