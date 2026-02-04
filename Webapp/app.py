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
        # Categorical feature mapping (same as training phase)
        category_map = {
            "gender": {"Male": 1, "Female": 0, "1": 1, "0": 0},  # Allow both text & numbers
            "ever_married": {"Yes": 1, "No": 0, "1": 1, "0": 0},
            "work_type": {"Govt Job": 0, "Private": 1, "Self-employed": 2, "Children": 3, "0": 0, "1": 1, "2": 2, "3": 3},
            "Residence_type": {"Rural": 0, "Urban": 1, "0": 0, "1": 1},
            "smoking_status": {"Unknown": 0, "Formerly Smoked": 1, "Never Smoked": 2, "Smokes": 3, "0": 0, "1": 1, "2": 2, "3": 3},
        }

        # Extract numerical inputs
        input_data = [
            float(request.form["age"]),
            float(request.form["hypertension"]),
            float(request.form["heart_disease"]),
            float(request.form["avg_glucose_level"]),
            float(request.form["bmi"]),
        ]

        # Extract categorical inputs properly
        for field in category_map.keys():
            value = request.form.get(field, None)

            if value is None:
                logging.error(f"⚠️ Missing input for {field}")
                return render_template("error.html", error=f"Missing input: {field}")

            # Convert value to string before lookup to handle both "1"/"0" and "Male"/"Female"
            value_str = str(value)

            if value_str not in category_map[field]:
                logging.error(f"⚠️ Invalid input for {field}: {value}")
                return render_template("error.html", error=f"Invalid input: {field}")

            input_data.append(category_map[field][value_str])  # Correct encoding

        logging.info(f"✅ Final User Input (All Features): {input_data}")

        # Get prediction
        prediction = predict_stroke(input_data)

        return render_template('result.html', prediction=prediction)

    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        return render_template('error.html', error="Something went wrong! Please try again.")

if __name__ == '__main__':
    app.run(debug=True)
