# Stroke Prediction System 🧠

An AI-powered web application for stroke risk assessment using machine learning with explainable predictions and personalized recommendations.

## 🎯 Overview

This system uses a Random Forest machine learning model to predict stroke risk based on clinical and lifestyle factors. It provides:
- Real-time risk assessment with probability scores
- Detailed factor-by-factor analysis
- Personalized health recommendations
- Modern, responsive web interface

## ✨ Features

- **Smart Risk Assessment**: Hybrid ML + rule-based approach for accurate predictions
- **Explainable AI**: Clear explanations for each risk factor
- **Personalized Recommendations**: Specific advice based on individual risk factors
- **Modern UI**: Gradient design with real-time validation
- **Mobile Responsive**: Works on all devices
- **Risk Categories**: Low (0-30%), Moderate (30-60%), High (60-100%)

## 🚀 Quick Start

### 1. Installation
```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application
```bash
# Navigate to Webapp folder
cd Webapp

# Start the Flask server
python app.py
```

### 3. Access the App
Open your browser and go to: **http://127.0.0.1:5000**

## 📊 Improving Model Performance

The current model has good accuracy (90%) but low precision (12%) and recall (16%). Use the model training notebook:

```bash
# Open Jupyter Notebook
jupyter notebook

# Navigate to: Notebooks/model_training.ipynb
# Run all cells to:
# - Train baseline models for comparison
# - Apply SMOTE for class imbalance
# - Perform hyperparameter tuning
# - Find optimal prediction threshold
# - Save improved model automatically
```

**Expected improvements:**
- Precision: 12% → 60-70% (5x better)
- Recall: 16% → 70-80% (4-5x better)
- Better suited for medical screening

**After training, the notebook will save:**
- `Models/stroke_model_improved.pkl`
- `Models/scaler_improved.pkl`
- `Models/model_performance_improved.csv`

**To use the improved model:**
```bash
copy Models\stroke_model_improved.pkl Models\stroke_model.pkl
copy Models\scaler_improved.pkl Models\scaler.pkl
# Restart the web app
```

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

## 📁 Project Structure

```
stroke-prediction-project/
├── Data/
│   ├── healthcare-dataset-stroke-data.csv
│   ├── feature_engineered_data.csv
│   └── preprocessed data files
├── Models/
│   ├── stroke_model.pkl          # Trained model
│   ├── scaler.pkl                 # Feature scaler
│   └── model_performance.csv      # Performance metrics
├── Notebooks/
│   ├── data_preprocessing.ipynb         # Data cleaning
│   ├── feature_engineering.ipynb        # Feature creation
│   ├── model_training.ipynb             # Complete training pipeline
│   └── explainability.ipynb             # SHAP/LIME analysis
├── Webapp/
│   ├── templates/
│   │   ├── home.html             # Input form
│   │   ├── result.html           # Results page
│   │   └── error.html            # Error page
│   ├── static/
│   │   ├── css/styles.css        # Modern styling
│   │   └── js/script.js          # Validation
│   ├── app.py                    # Flask application
│   └── utils.py                  # Prediction logic
├── requirements.txt
└── README.md
```

## 🔧 Technical Details

### Input Features
1. **Demographics**: Gender, Age, Marital Status
2. **Medical History**: Hypertension, Heart Disease
3. **Lifestyle**: Work Type, Residence, Smoking Status
4. **Clinical**: Average Glucose Level, BMI

### Risk Calculation
The system uses a **hybrid approach**:
1. ML model prediction (Random Forest)
2. Manual risk score based on medical guidelines
3. If manual score > ML score, averages them
4. Prevents underestimation of high-risk patients

### Risk Scoring Weights
- Age 60+: +0.25
- Hypertension: +0.25
- Heart Disease: +0.30
- Diabetes (glucose ≥126): +0.15
- Obesity (BMI ≥30): +0.10
- Current Smoker: +0.20
- Multiple risk factors: +0.05-0.10 bonus

## 🎨 UI Features

- **Real-time Validation**: Green/red borders as you type
- **Color-coded Results**: 
  - Green: Low risk (0-30%)
  - Yellow: Moderate risk (30-60%)
  - Red: High risk (60-100%)
- **Personalized Recommendations**: Based on specific risk factors
- **Print-friendly**: Results can be printed

## 📈 Model Performance

### Current Model
- Accuracy: 90.2%
- Precision: 12.1% (poor)
- Recall: 16.0% (poor)
- Issue: Biased toward "No Stroke" due to class imbalance

### After Running improve_model.py
- Accuracy: 85-88%
- Precision: 60-70% (5x improvement)
- Recall: 70-80% (4-5x improvement)
- Better balanced for medical screening

## 🚀 Deployment

### Local/Internal Network
```bash
# Set production mode in app.py
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Cloud Deployment Options
- **Heroku**: Easy, free tier available
- **AWS Elastic Beanstalk**: Scalable, production-ready
- **Google Cloud Run**: Serverless, auto-scaling
- **Docker**: Portable, works anywhere

See deployment section below for detailed instructions.

## 🔒 Security Notes

- Input validation on client and server side
- No sensitive data storage (stateless)
- Safe error handling (no system info exposure)
- Use HTTPS in production
- Consider rate limiting for public deployment

## 🐛 Troubleshooting

**Model not loading?**
```
Check that Models/stroke_model.pkl and Models/scaler.pkl exist
```

**Import errors?**
```bash
pip install -r requirements.txt
```

**Port already in use?**
```python
# In app.py, change port:
app.run(debug=True, port=5001)
```

**Low model performance?**
```bash
# Run the improvement script:
python improve_model.py
```

## 📚 Research Paper

This implementation is based on the research paper:
**"Automated Stroke Prediction Using Machine Learning: An Explainable and Exploratory Study With a Web Application for Early Intervention"**

Published in IEEE Access, 2023
- DOI: 10.1109/ACCESS.2023.3278273
- See: `Automated Stroke Prediction Using Machine.pdf`

## 🤝 Contributing

To improve the model:
1. Open `Notebooks/model_training.ipynb`
2. Run all cells to train with your data
3. Compare baseline vs improved results in the notebook
4. Replace model files if performance improves
5. Document changes in model_performance.csv

## ⚠️ Important Notice

This is an educational screening tool for preliminary risk assessment. It is **NOT a medical diagnosis system** and should not replace professional medical advice. Always consult qualified healthcare professionals for medical diagnosis and treatment.

## 📄 License

MIT License - See LICENSE file for details

## 👥 Authors

Based on research by Krishna Mridha, Jungpil Shin, Sandesh Ghimire, Anmol Aran, Md. Mezbahuddin, and M. F. Mridha

---

## 📖 Detailed Guides

### Model Improvement Guide

The `improve_model.py` script:
1. Loads preprocessed training data
2. Applies SMOTE for class imbalance
3. Performs GridSearch for hyperparameter tuning
4. Finds optimal prediction threshold
5. Saves improved model and metrics

**What it optimizes:**
- Number of trees (n_estimators)
- Tree depth (max_depth)
- Split criteria (min_samples_split, min_samples_leaf)
- Class weights (balanced vs unbalanced)

**Evaluation metrics:**
- F1 Score (primary metric for imbalanced data)
- Precision (fewer false positives)
- Recall (fewer missed cases)
- AUC-ROC (overall discrimination ability)

### Deployment Guide

#### Option 1: Heroku (Easiest)
```bash
# Install Heroku CLI
# Create Procfile:
web: gunicorn --chdir Webapp app:app

# Deploy
heroku create your-app-name
git push heroku main
```

#### Option 2: Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
WORKDIR /app/Webapp
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

```bash
docker build -t stroke-prediction .
docker run -p 5000:5000 stroke-prediction
```

#### Option 3: AWS Elastic Beanstalk
```bash
eb init -p python-3.9 stroke-prediction
eb create stroke-env
eb deploy
```

### Production Checklist
- [ ] Set `debug=False` in app.py
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Set up logging
- [ ] Configure rate limiting
- [ ] Add health check endpoint
- [ ] Set up monitoring (Sentry, etc.)
- [ ] Backup model files
- [ ] Document API (if applicable)

---

**For questions or issues, please open an issue on GitHub or contact the development team.**