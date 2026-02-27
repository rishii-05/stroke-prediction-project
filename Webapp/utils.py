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
    logging.info("\nModel and scaler loaded successfully.")

except Exception as e:
    logging.error(f"\nError loading model or scaler: {e}")
    model, scaler = None, None


# ---------------- PREPROCESS INPUT ----------------
def preprocess_input(data):
    """
    Preprocess input data with correct feature order and scaling
    Feature order MUST match training exactly
    """
    try:
        if scaler is None:
            raise ValueError("\nScaler not loaded!")

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
        logging.error(f"\nError in preprocessing: {e}")
        raise


# ---------------- PREDICTION ----------------
def predict_stroke(input_data):
    """
    Predict stroke risk using probability-based threshold with manual risk adjustment
    Returns: dict with prediction, probability, reasons, and recommendations
    """
    try:
        if model is None:
            raise ValueError("\nModel not loaded!")

        # Preprocess input
        processed_data = preprocess_input(input_data)

        # Get probability for stroke class (class = 1)
        proba = model.predict_proba(processed_data)[0][1]
        
        # Calculate manual risk score as a safety check
        manual_risk_score = calculate_manual_risk_score(input_data)
        
        # Adjust probability if manual risk score suggests higher risk
        # This helps when the model underestimates risk
        if manual_risk_score > proba:
            logging.info(f"\nManual risk score ({manual_risk_score:.3f}) higher than model ({proba:.3f})")
            proba = (proba + manual_risk_score) / 2  # Average them
            logging.info(f"\nAdjusted probability to: {proba:.3f}")
        
        probability_percent = round(proba * 100, 2)

        # Medical-safe threshold
        prediction = 1 if proba >= 0.3 else 0

        # Generate risk factors explanation
        reasons = generate_risk_factors(input_data, proba)
        
        # Generate personalized recommendations
        recommendations = generate_recommendations(input_data, proba)

        logging.info(f"\nStroke probability: {proba:.3f}")
        logging.info(f"\nFinal prediction (0=Low, 1=High): {prediction}")

        return {
            'prediction': prediction,
            'probability': probability_percent,
            'reasons': reasons,
            'recommendations': recommendations
        }

    except Exception as e:
        logging.error(f"\nPrediction error: {e}")
        return {
            'prediction': -1,
            'probability': 0,
            'reasons': ['Error in prediction'],
            'recommendations': ['Please try again or contact support']
        }


def calculate_manual_risk_score(input_data):
    """
    Calculate a manual risk score based on known risk factors
    This serves as a safety check when the ML model underestimates risk
    Returns a score between 0 and 1
    """
    gender, age, hypertension, heart_disease, ever_married, work_type, \
    residence_type, avg_glucose_level, bmi, smoking_status = input_data
    
    risk_score = 0.0
    
    # Age is the strongest predictor
    if age >= 75:
        risk_score += 0.35
    elif age >= 65:
        risk_score += 0.25
    elif age >= 55:
        risk_score += 0.15
    elif age >= 45:
        risk_score += 0.08
    elif age >= 35:
        risk_score += 0.03
    else:
        risk_score += 0.01
    
    # Hypertension - major risk factor
    if hypertension == 1:
        risk_score += 0.25
    
    # Heart disease - very serious
    if heart_disease == 1:
        risk_score += 0.30
    
    # Glucose level - diabetes is serious
    if avg_glucose_level >= 200:
        risk_score += 0.20
    elif avg_glucose_level >= 126:  # Diabetes threshold
        risk_score += 0.15
    elif avg_glucose_level >= 100:  # Pre-diabetes
        risk_score += 0.08
    
    # BMI
    if bmi >= 35:
        risk_score += 0.15
    elif bmi >= 30:
        risk_score += 0.10
    elif bmi >= 25:
        risk_score += 0.05
    
    # Smoking - very significant
    if smoking_status == 3:  # Currently smokes
        risk_score += 0.20
    elif smoking_status == 1:  # Formerly smoked
        risk_score += 0.08
    
    # Gender (males have slightly higher risk)
    if gender == 1:
        risk_score += 0.05
    
    # Multiple risk factors compound - add bonus if 3+ major factors present
    major_factors = sum([
        hypertension == 1,
        heart_disease == 1,
        avg_glucose_level >= 126,
        bmi >= 30,
        smoking_status == 3,
        age >= 55
    ])
    
    if major_factors >= 3:
        risk_score += 0.10  # Compound risk bonus
    elif major_factors >= 2:
        risk_score += 0.05
    
    # Cap at 0.95 (never 100% certain)
    risk_score = min(risk_score, 0.95)
    
    return risk_score


def generate_risk_factors(input_data, probability):
    """
    Generate human-readable risk factors based on input data
    input_data order: gender, age, hypertension, heart_disease, ever_married, 
                      work_type, Residence_type, avg_glucose_level, bmi, smoking_status
    """
    reasons = []
    
    # Unpack input data
    gender, age, hypertension, heart_disease, ever_married, work_type, \
    residence_type, avg_glucose_level, bmi, smoking_status = input_data
    
    # Overall risk assessment - more nuanced
    if probability >= 0.6:
        reasons.append(f"🚨 HIGH RISK: {probability*100:.1f}% probability - Immediate medical consultation recommended")
    elif probability >= 0.3:
        reasons.append(f"⚠️ MODERATE RISK: {probability*100:.1f}% probability - Regular monitoring and lifestyle changes needed")
    else:
        # Check if there are risk factors even with low probability
        has_risk_factors = (hypertension == 1 or heart_disease == 1 or 
                           avg_glucose_level >= 100 or bmi >= 25 or smoking_status in [1, 3])
        if has_risk_factors:
            reasons.append(f"⚡ LOW-MODERATE RISK: {probability*100:.1f}% probability - Address risk factors to prevent future complications")
        else:
            reasons.append(f"✓ LOW RISK: {probability*100:.1f}% probability - Continue healthy lifestyle")
    
    # Age analysis (most important factor)
    if age >= 60:
        reasons.append(f"⚠️ Age {int(age)} years - Higher risk group (60+ years)")
    elif age >= 45:
        reasons.append(f"⚡ Age {int(age)} years - Moderate risk group (45-59 years)")
    else:
        reasons.append(f"✓ Age {int(age)} years - Lower risk group (under 45)")
    
    # Hypertension
    if hypertension == 1:
        reasons.append("⚠️ Hypertension present - Significant risk factor")
    else:
        reasons.append("✓ No hypertension detected")
    
    # Heart disease
    if heart_disease == 1:
        reasons.append("⚠️ Heart disease present - Major risk factor")
    else:
        reasons.append("✓ No heart disease detected")
    
    # Glucose level
    if avg_glucose_level >= 200:
        reasons.append(f"🚨 Very high glucose level ({avg_glucose_level:.1f} mg/dL) - Uncontrolled diabetes")
    elif avg_glucose_level >= 126:
        reasons.append(f"⚠️ High glucose level ({avg_glucose_level:.1f} mg/dL) - Diabetes indicator")
    elif avg_glucose_level >= 100:
        reasons.append(f"⚡ Elevated glucose level ({avg_glucose_level:.1f} mg/dL) - Pre-diabetes range")
    else:
        reasons.append(f"✓ Normal glucose level ({avg_glucose_level:.1f} mg/dL)")
    
    # BMI
    if bmi >= 35:
        reasons.append(f"🚨 BMI {bmi:.1f} - Severe obesity (high risk)")
    elif bmi >= 30:
        reasons.append(f"⚠️ BMI {bmi:.1f} - Obesity (increased risk)")
    elif bmi >= 25:
        reasons.append(f"⚡ BMI {bmi:.1f} - Overweight (moderate risk)")
    else:
        reasons.append(f"✓ BMI {bmi:.1f} - Normal weight range")
    
    # Smoking status
    if smoking_status == 3:
        reasons.append("⚠️ Current smoker - Significant risk factor")
    elif smoking_status == 1:
        reasons.append("⚡ Former smoker - Reduced but present risk")
    elif smoking_status == 2:
        reasons.append("✓ Never smoked - Lower risk")
    else:
        reasons.append("⚡ Smoking status unknown")
    
    return reasons


def generate_recommendations(input_data, probability):
    """
    Generate personalized recommendations based on specific risk factors
    input_data order: gender, age, hypertension, heart_disease, ever_married, 
                      work_type, Residence_type, avg_glucose_level, bmi, smoking_status
    """
    recommendations = []
    
    # Unpack input data
    gender, age, hypertension, heart_disease, ever_married, work_type, \
    residence_type, avg_glucose_level, bmi, smoking_status = input_data
    
    # Count major risk factors
    has_major_risks = (hypertension == 1 or heart_disease == 1 or 
                       avg_glucose_level >= 126 or bmi >= 30 or smoking_status == 3)
    
    # High risk or multiple risk factors - urgent actions first
    if probability >= 0.5 or has_major_risks:
        recommendations.append("Schedule an appointment with a healthcare provider for comprehensive evaluation")
    
    # Hypertension recommendations
    if hypertension == 1:
        recommendations.append("Monitor blood pressure daily and maintain a log")
        recommendations.append("Reduce sodium intake to less than 2,300mg per day")
        recommendations.append("Take prescribed blood pressure medications as directed")
        recommendations.append("Aim for blood pressure below 120/80 mmHg")
    
    # Heart disease recommendations
    if heart_disease == 1:
        recommendations.append("Follow your cardiologist's treatment plan strictly")
        recommendations.append("Keep emergency contact numbers readily available")
        recommendations.append("Avoid strenuous activities without medical clearance")
        recommendations.append("Take cardiac medications exactly as prescribed")
    
    # Glucose recommendations
    if avg_glucose_level >= 126:
        recommendations.append("Consult an endocrinologist for diabetes management immediately")
        recommendations.append("Monitor blood sugar levels at least twice daily")
        recommendations.append("Follow a diabetic-friendly diet plan (low glycemic index foods)")
        recommendations.append("Get HbA1c test every 3 months to track diabetes control")
    elif avg_glucose_level >= 100:
        recommendations.append("Get HbA1c test to check for pre-diabetes")
        recommendations.append("Reduce sugar and refined carbohydrate intake")
        recommendations.append("Increase fiber intake with whole grains and vegetables")
    
    # BMI recommendations
    if bmi >= 30:
        recommendations.append("Work with a nutritionist to develop a structured weight loss plan")
        recommendations.append("Start with low-impact exercises like walking 30 minutes daily")
        recommendations.append("Aim to lose 5-10% of body weight to significantly reduce stroke risk")
        recommendations.append("Track daily calorie intake and maintain a food diary")
    elif bmi >= 25:
        recommendations.append("Maintain a balanced diet with portion control")
        recommendations.append("Incorporate 150 minutes of moderate exercise weekly")
        recommendations.append("Focus on whole foods and limit processed foods")
    
    # Smoking recommendations
    if smoking_status == 3:  # Currently smokes
        recommendations.append("URGENT: Quit smoking immediately - single most important change you can make")
        recommendations.append("Consider nicotine replacement therapy or prescription medications")
        recommendations.append("Join a smoking cessation program for support")
        recommendations.append("Avoid triggers and secondhand smoke exposure")
    elif smoking_status == 1:  # Formerly smoked
        recommendations.append("Congratulations on quitting smoking - continue to stay tobacco-free")
        recommendations.append("Avoid environments with secondhand smoke")
    
    # Age-specific recommendations
    if age >= 60:
        recommendations.append("Schedule health screenings every 6 months due to age-related risk")
        recommendations.append("Consider joining senior wellness programs")
    elif age >= 45:
        recommendations.append("Annual comprehensive health check-ups recommended")
    elif age < 45 and has_major_risks:
        recommendations.append("Young age is protective, but address risk factors now to prevent future complications")
    
    # General lifestyle for those with risk factors
    if has_major_risks or probability >= 0.3:
        recommendations.append("Adopt a Mediterranean-style diet rich in fruits, vegetables, and whole grains")
        recommendations.append("Limit alcohol consumption (max 1-2 drinks per day)")
        recommendations.append("Manage stress through meditation, yoga, or counseling")
        recommendations.append("Ensure 7-8 hours of quality sleep nightly")
        recommendations.append("Learn stroke warning signs: F.A.S.T. (Face drooping, Arm weakness, Speech difficulty, Time to call emergency)")
    
    # Low risk maintenance - only if truly low risk
    if probability < 0.3 and not has_major_risks:
        recommendations.append("Continue maintaining your healthy lifestyle")
        recommendations.append("Regular exercise and balanced diet are key to prevention")
        recommendations.append("Schedule routine health check-ups annually")
        recommendations.append("Stay informed about stroke prevention")
    
    # If no recommendations yet (shouldn't happen), add default
    if len(recommendations) == 0:
        recommendations.append("Maintain a healthy lifestyle with regular exercise and balanced diet")
        recommendations.append("Schedule regular health check-ups")
    
    return recommendations
