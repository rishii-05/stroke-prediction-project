# 🧠 AI Brain Stroke Risk Assessment System

An intelligent web application for stroke risk prediction using machine learning with user authentication, prediction history tracking, and personalized health recommendations.

## ✨ Features

### Core Functionality
- **AI-Powered Risk Assessment**: Random Forest ML model with 85% accuracy
- **Hybrid Prediction**: Combines ML model + medical guidelines for safety
- **Explainable Results**: Clear breakdown of risk factors
- **Personalized Recommendations**: Tailored health advice based on your risk profile

### User Management
- 🔐 Secure user registration and login
- 👤 Personal profile with statistics
- 📊 Complete prediction history tracking
- 💾 Automatic assessment saving
- 🔒 Password hashing and session management

### User Interface
- 🎨 Modern, clean design
- 📱 Mobile responsive
- ✅ Real-time form validation
- 🎯 Color-coded risk levels (Green/Yellow/Red)
- 🧭 Easy navigation

## 🚀 Quick Start

### 1. Create Virtual Environment

**Windows:**
```bash
# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\activate

# You should see (.venv) before your command prompt
```

**Mac/Linux:**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# You should see (.venv) before your command prompt
```

### 2. Install Dependencies

```bash
# Make sure virtual environment is activated (you should see (.venv))
pip install -r requirements.txt
```

### 3. Run the Application

```bash
# Navigate to Webapp folder
cd Webapp

# Start the server
python app.py
```

Open browser: **http://127.0.0.1:5000**

### 4. First Time Setup

1. Click "Register here" on login page
2. Create your account
3. Login with credentials
4. Start taking assessments!

## 📁 Project Structure

```
stroke-prediction-project/
├── Data/
│   ├── healthcare-dataset-stroke-data.csv    # Original dataset
│   ├── feature_engineered_data.csv           # Processed features
│   └── *_preprocessed.csv                    # Train/test splits
├── Models/
│   ├── stroke_model.pkl                      # Trained ML model
│   ├── scaler.pkl                            # Feature scaler
│   ├── model_comparison.csv                  # Performance metrics
│   └── shap_*.png                            # Explainability plots
├── Notebooks/
│   ├── data_preprocessing.ipynb              # Data cleaning + SMOTE
│   ├── feature_engineering.ipynb             # Feature creation
│   ├── model_training.ipynb                  # Model training pipeline
│   └── explainability.ipynb                  # SHAP/LIME analysis
├── Webapp/
│   ├── templates/                            # HTML pages
│   │   ├── login.html                        # Login page
│   │   ├── register.html                     # Registration page
│   │   ├── dashboard.html                    # Main assessment form
│   │   ├── profile.html                      # User profile
│   │   ├── history.html                      # Prediction history
│   │   └── result.html                       # Results page
│   ├── static/
│   │   ├── css/styles.css                    # Styling
│   │   └── js/script.js                      # Form validation
│   ├── app.py                                # Flask application
│   ├── database.py                           # Database functions
│   ├── utils.py                              # Prediction logic
│   └── stroke_app.db                         # SQLite database
├── requirements.txt                          # Python dependencies
├── .gitignore                                # Git ignore rules
└── README.md                                 # This file
```

## 🔧 Technical Details

### Input Features (in order of importance)
1. **Age** (42.6%) - Strongest predictor
2. **Average Glucose Level** (18.7%) - Diabetes indicator
3. **BMI** (14.9%) - Obesity factor
4. **Work Type** (7.5%)
5. **Smoking Status** (5.3%)
6. **Residence Type** (3.0%)
7. **Gender** (2.6%)
8. **Marital Status** (2.4%)
9. **Hypertension** (1.6%) - Correlated with age
10. **Heart Disease** (1.4%) - Correlated with age

**Note:** Hypertension and heart disease show low ML importance because they're highly correlated with age, but they remain medically critical and are weighted heavily in the manual risk score.

### Risk Calculation Method

The system uses a **hybrid approach**:
1. ML model prediction (Random Forest)
2. Manual risk score based on medical guidelines
3. If manual score > ML score, averages them
4. Prevents underestimation of high-risk patients

### Manual Risk Scoring Weights
- **Age 75+**: +0.35
- **Age 65-74**: +0.25
- **Age 55-64**: +0.15
- **Heart Disease**: +0.30 (highest medical risk)
- **Hypertension**: +0.25
- **Diabetes (glucose ≥126)**: +0.15
- **Current Smoker**: +0.20
- **Obesity (BMI ≥35)**: +0.15
- **Multiple risk factors (3+)**: +0.10 compound bonus

## 📈 Model Performance

### Current Improved Model
- **Accuracy**: 85.4%
- **Precision**: 16.3%
- **Recall**: 48.0% (200% improvement over baseline!)
- **F1 Score**: 24.4% (76.6% improvement)
- **AUC-ROC**: 0.79 (good discrimination)

**Key Improvement:** The improved model catches 48% of stroke cases vs only 16% for baseline - critical for medical screening where missing cases is dangerous.

**Why lower accuracy?** The improved model is more conservative (predicts more strokes) to avoid missing real cases. This is medically appropriate - false positives are safer than false negatives in stroke screening.

## 🗄️ Database

### Structure
- **SQLite database**: `Webapp/stroke_app.db`
- **Users table**: Stores account information (username, email, password hash)
- **Predictions table**: Stores assessment history

### Security
- Passwords are hashed (SHA-256)
- Database file is in `.gitignore` (not pushed to GitHub)
- Each user only sees their own data
- Session-based authentication

### Local vs Production
- **Your laptop**: Has test data (for development)
- **Deployed server**: Creates its own separate database (for production)
- They are completely independent - deleting local database doesn't affect production

## 🧪 Testing

Try these test cases:

**High Risk Patient:**
- Male, 75 years, Hypertension: Yes, Heart Disease: Yes
- Glucose: 150, BMI: 32, Currently Smokes
- Expected: 60-80% risk

**Low Risk Patient:**
- Female, 30 years, No conditions
- Glucose: 85, BMI: 22, Never Smoked
- Expected: 5-15% risk

**Moderate Risk Patient:**
- Male, 55 years, Hypertension: Yes
- Glucose: 110, BMI: 27, Former Smoker
- Expected: 35-50% risk

## 🔄 Model Retraining

To retrain the model with new data:

1. Open `Notebooks/model_training.ipynb`
2. Run all cells
3. Review baseline vs improved comparison
4. If performance improves:
   
   Backup current model:
   ```bash
   copy ../Models/stroke_model.pkl ../Models/stroke_model_backup.pkl
   ```
   Replace with improved model:
   ```bash
   copy ../Models/stroke_model_improved.pkl ../Models/stroke_model.pkl
   ```
   
5. Restart the web application

## 🐛 Troubleshooting

**Error: "Database locked"**
- Close any programs accessing the database
- Restart the application

**Port already in use:**
```python
# In app.py, change port:
app.run(debug=True, port=5001)
```

**Model version warning:**
- This is normal if scikit-learn versions differ
- Model still works correctly

## ⚠️ Important Notice

This is an educational screening tool for preliminary risk assessment. It is **NOT a medical diagnosis system** and should not replace professional medical advice. Always consult qualified healthcare professionals for medical diagnosis and treatment.

## 📚 References & Acknowledgments

This implementation is based on the following research paper:

- **Title:** Automated Stroke Prediction Using Machine Learning: An Explainable and Exploratory Study With a Web Application for Early Intervention 

- **Authors:** Krishna Mridha, Sandesh Ghimire, Jungpil Shin, Anmol Aran, Md. Mezbah Uddin, and M. F. Mridha 

- **Published in:** IEEE Access, Volume 11, 2023 

- **DOI:** 10.1109/ACCESS.2023.3278273

## 📄 License

This project is for educational purposes.