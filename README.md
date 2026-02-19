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

## 📊 Model Training

The system uses a hybrid ML + rule-based approach. To train or retrain the model:

```bash
# Open Jupyter Notebook
jupyter notebook

# Navigate to: Notebooks/model_training.ipynb
# Run all cells to:
# - Train 6 baseline models for comparison
# - Apply hyperparameter tuning to Random Forest
# - Find optimal prediction threshold
# - Compare baseline vs improved performance
# - Save improved model automatically
```

**Note:** SMOTE (class balancing) is already applied in `data_preprocessing.ipynb`

**After training, the notebook will save:**
- `Models/stroke_model_improved.pkl` - Optimized model
- `Models/model_performance_improved.csv` - Performance metrics
- `Models/model_comparison.csv` - Baseline vs Improved comparison

**To deploy the improved model:**
```bash
copy Models\stroke_model_improved.pkl Models\stroke_model.pkl
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
│   ├── stroke_model.pkl               # Active trained model
│   ├── scaler.pkl                     # Feature scaler
│   ├── model_comparison.csv           # Baseline vs Improved comparison
│   ├── model_performance_improved.csv # Current model metrics
│   ├── lime_explanation.html          # LIME explainability report
│   ├── shap_summary_plot.png          # SHAP feature importance
│   └── shap_beeswarm_plot.png         # SHAP detailed analysis
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

### Input Features (in order of importance)
1. **Age** (42.6% importance) - Strongest predictor
2. **Average Glucose Level** (18.7% importance) - Diabetes indicator
3. **BMI** (14.9% importance) - Obesity factor
4. **Work Type** (7.5% importance)
5. **Smoking Status** (5.3% importance)
6. **Residence Type** (3.0% importance)
7. **Gender** (2.6% importance)
8. **Marital Status** (2.4% importance)
9. **Hypertension** (1.6% importance) - Correlated with age
10. **Heart Disease** (1.4% importance) - Correlated with age

**Note:** Hypertension and heart disease show low ML importance because they're highly correlated with age. However, they remain medically critical and are weighted heavily in the manual risk score.

### Risk Calculation
The system uses a **hybrid approach**:
1. ML model prediction (Random Forest)
2. Manual risk score based on medical guidelines
3. If manual score > ML score, averages them
4. Prevents underestimation of high-risk patients

### Risk Scoring Weights (Manual Risk Score)
Based on medical guidelines, used as safety check when ML underestimates:
- **Age 75+**: +0.35
- **Age 65-74**: +0.25
- **Age 55-64**: +0.15
- **Heart Disease**: +0.30 (highest medical risk)
- **Hypertension**: +0.25
- **Diabetes (glucose ≥126)**: +0.15
- **Current Smoker**: +0.20
- **Obesity (BMI ≥35)**: +0.15
- **Overweight (BMI ≥30)**: +0.10
- **Multiple risk factors (3+)**: +0.10 compound bonus
- **Multiple risk factors (2)**: +0.05 compound bonus

## 🎨 UI Features

- **Real-time Validation**: Green/red borders as you type
- **Color-coded Results**: 
  - Green: Low risk (0-30%)
  - Yellow: Moderate risk (30-60%)
  - Red: High risk (60-100%)
- **Personalized Recommendations**: Based on specific risk factors
- **Print-friendly**: Results can be printed

## 📈 Model Performance

### Current Improved Model
- **Accuracy**: 85.4%
- **Precision**: 16.3%
- **Recall**: 48.0% (200% improvement over baseline!)
- **F1 Score**: 24.4% (76.6% improvement)
- **AUC-ROC**: 0.79 (good discrimination)

### Baseline Model (for comparison)
- **Accuracy**: 90.2%
- **Precision**: 12.1%
- **Recall**: 16.0%
- **F1 Score**: 13.8%

**Key Improvement:** The improved model catches 48% of stroke cases vs only 16% for baseline - critical for medical screening where missing cases is dangerous.

**Why lower accuracy?** The improved model is more conservative (predicts more strokes) to avoid missing real cases. This is medically appropriate - false positives are safer than false negatives in stroke screening.

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
# Retrain the model:
# Open Notebooks/model_training.ipynb in Jupyter
# Run all cells to train improved model
# Follow instructions at end to deploy
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
2. Run all cells to train with current data
3. Review baseline vs improved comparison in the notebook output
4. If performance improves, follow deployment instructions in notebook
5. Document changes in `Models/model_comparison.csv`

To modify preprocessing:
1. Edit `Notebooks/data_preprocessing.ipynb` (applies SMOTE)
2. Edit `Notebooks/feature_engineering.ipynb` (creates new features)
3. Retrain model using `model_training.ipynb`

## ⚠️ Important Notice

This is an educational screening tool for preliminary risk assessment. It is **NOT a medical diagnosis system** and should not replace professional medical advice. Always consult qualified healthcare professionals for medical diagnosis and treatment.

## 📄 License

MIT License - See LICENSE file for details

## 👥 Authors

Based on research by Krishna Mridha, Jungpil Shin, Sandesh Ghimire, Anmol Aran, Md. Mezbahuddin, and M. F. Mridha

---

## 📖 Detailed Guides

### Model Training Guide

The `Notebooks/model_training.ipynb` notebook:
1. Loads preprocessed data (already SMOTE-balanced from preprocessing)
2. Trains 6 baseline models (RF, XGBoost, LogReg, SVM, KNN, NaiveBayes)
3. Performs GridSearch hyperparameter tuning on best model (Random Forest)
4. Finds optimal prediction threshold using precision-recall curve
5. Compares baseline vs improved performance
6. Saves improved model and comprehensive metrics

**What it optimizes:**
- Number of trees (n_estimators): 100 or 200
- Tree depth (max_depth): 15, 20, or unlimited
- Split criteria (min_samples_split): 2 or 5
- Leaf size (min_samples_leaf): 1 or 2
- Class weights: balanced or unbalanced

**Evaluation metrics:**
- F1 Score (primary metric for imbalanced data)
- Precision (fewer false alarms)
- Recall (fewer missed stroke cases - most critical!)
- AUC-ROC (overall discrimination ability)
- Confusion matrix (detailed error analysis)

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