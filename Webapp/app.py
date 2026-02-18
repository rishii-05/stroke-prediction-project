from flask import Flask, render_template, request
import logging
import datetime
from utils import predict_stroke  # Ensure this function is correctly implemented in utils.py

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Safe categorical encoding (accepts numbers OR text)
        def encode(value, mapping):
            value = str(value)
            if value.isdigit():
                return int(value)
            return mapping[value]

        category_map = {
            "gender": {"Male": 1, "Female": 0},
            "ever_married": {"Yes": 1, "No": 0},
            "work_type": {"Govt Job": 0, "Private": 1, "Self-employed": 2, "Children": 3},
            "Residence_type": {"Rural": 0, "Urban": 1},
            "smoking_status": {"Unknown": 0, "Formerly Smoked": 1, "Never Smoked": 2, "Smokes": 3},
        }

        # Handle BMI - use mean if not provided
        bmi_value = request.form.get("bmi", "").strip()
        if bmi_value == "" or bmi_value is None:
            # Use the mean BMI from training data (28.893237)
            bmi_value = 28.89
            logging.info(f"⚠️ BMI not provided, using mean value: {bmi_value}")
        else:
            bmi_value = float(bmi_value)

        # EXACT TRAINING FEATURE ORDER
        input_data = [
            encode(request.form["gender"], category_map["gender"]),                 # gender
            float(request.form["age"]),                                             # age
            float(request.form["hypertension"]),                                    # hypertension
            float(request.form["heart_disease"]),                                   # heart_disease
            encode(request.form["ever_married"], category_map["ever_married"]),     # ever_married
            encode(request.form["work_type"], category_map["work_type"]),           # work_type
            encode(request.form["Residence_type"], category_map["Residence_type"]), # Residence_type
            float(request.form["avg_glucose_level"]),                               # avg_glucose_level
            bmi_value,                                                              # bmi (with default handling)
            encode(request.form["smoking_status"], category_map["smoking_status"])  # smoking_status
        ]

        logging.info(f"✅ Final User Input (Correct & Safe): {input_data}")

        result = predict_stroke(input_data)

        return render_template("result.html", 
                             prediction=result['prediction'],
                             probability=result['probability'],
                             reasons=result['reasons'],
                             recommendations=result['recommendations'])

    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        return render_template("error.html", error=str(e))

if __name__ == '__main__':
    app.run(debug=True)