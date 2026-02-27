from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import logging
import datetime
from functools import wraps
from utils import predict_stroke
from database import (
    create_user, verify_user, get_user_by_id, 
    save_prediction, get_user_predictions, get_user_stats
)

import os

app = Flask(__name__)
# Use environment variable if available, otherwise use default for development
app.secret_key = os.environ.get('SECRET_KEY', 'sk_dev_local_testing_key_not_for_production')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    """Landing page - redirect based on login status"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        
        # Validation
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        if len(password) < 6:
            return render_template('register.html', error='Password must be at least 6 characters')
        
        # Create user
        success, result = create_user(username, email, password, full_name)
        
        if success:
            logging.info(f"✅ New user registered: {username}")
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error=result)
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, user = verify_user(username, password)
        
        if success:
            session['user_id'] = user['id']
            session['username'] = user['username']
            logging.info(f"✅ User logged in: {username}")
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    username = session.get('username', 'Unknown')
    session.clear()
    logging.info(f"✅ User logged out: {username}")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - assessment form"""
    user = get_user_by_id(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    user = get_user_by_id(session['user_id'])
    stats = get_user_stats(session['user_id'])
    return render_template('profile.html', user=user, stats=stats)

@app.route('/history')
@login_required
def history():
    """Prediction history page"""
    user = get_user_by_id(session['user_id'])
    predictions = get_user_predictions(session['user_id'], limit=20)
    return render_template('history.html', user=user, predictions=predictions)

@app.route('/predict', methods=['POST'])
@login_required
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
        
        # Save prediction to history
        save_prediction(
            session['user_id'],
            input_data,
            result['prediction'],
            result['probability']
        )
        
        user = get_user_by_id(session['user_id'])

        return render_template("result.html", 
                             prediction=result['prediction'],
                             probability=result['probability'],
                             reasons=result['reasons'],
                             recommendations=result['recommendations'],
                             user=user)

    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        return render_template("error.html", error=str(e))

if __name__ == '__main__':
    app.run(debug=True)