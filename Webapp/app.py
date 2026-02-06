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

'''@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Log request details
        user_ip = request.remote_addr
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Request from {user_ip} at {timestamp}")

        # Extract and validate user input
        required_fields = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi']
        
        for field in required_fields:
            if field not in request.form:
                logging.error(f"Missing form field: {field}")
                return render_template('error.html', error=f"Missing input: {field}")

        try:
            input_data = [float(request.form[field]) for field in required_fields]
        except ValueError as ve:
            logging.error(f"Invalid input: {ve}")
            return render_template('error.html', error="Invalid input! Please enter numerical values.")

        # Log input data
        logging.info(f"User Input: {input_data}")

        # Predict stroke risk
        prediction = predict_stroke(input_data)

        # Log the prediction result
        logging.info(f"Prediction Result: {prediction}")

        return render_template('result.html', prediction=prediction)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return render_template('error.html', error="Something went wrong! Please try again.")'''

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

        # ✅ EXACT TRAINING FEATURE ORDER
        input_data = [
            encode(request.form["gender"], category_map["gender"]),                 # gender
            float(request.form["age"]),                                             # age
            float(request.form["hypertension"]),                                    # hypertension
            float(request.form["heart_disease"]),                                   # heart_disease
            encode(request.form["ever_married"], category_map["ever_married"]),     # ever_married
            encode(request.form["work_type"], category_map["work_type"]),           # work_type
            encode(request.form["Residence_type"], category_map["Residence_type"]), # Residence_type
            float(request.form["avg_glucose_level"]),                               # avg_glucose_level
            float(request.form["bmi"]),                                             # bmi
            encode(request.form["smoking_status"], category_map["smoking_status"])  # smoking_status
        ]

        logging.info(f"✅ Final User Input (Correct & Safe): {input_data}")

        prediction = predict_stroke(input_data)

        return render_template("result.html", prediction=prediction)

    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        return render_template("error.html", error=str(e))




if __name__ == '__main__':
    app.run(debug=True)
