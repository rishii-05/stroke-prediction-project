# Stroke Prediction Web App 🧠💡
A Flask-based web application that predicts stroke risk based on user input.

## 📌 Features
- User inputs age, hypertension, heart disease, glucose level, BMI and other.
- Interactive web app using Flask.
- A trained ML model that predicts stroke risk based on user input.

## 🛠️ Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python webapp/app.py`
4. Access the app in the open browser: `http://127.0.0.1:5000/`

## 📊 Model
- Trained using `scikit-learn`
- Scaled inputs using `StandardScaler`
- Model stored as `Models/stroke_model.pkl`

## 📁 File Structure
stroke-prediction-app/
│── Data/
│   ├── healthcare-dataset-stroke-data.csv
│── Models/
│   ├── stroke_model.pkl
│   ├── scaler.pkl
│── Notebooks/
│   ├── data_preprocessing.ipynb
│   ├── feature_engineering.ipynb
│   ├── model_training.ipynb
│   ├── explainability.ipynb
│── Webapp/
│   ├── templates/
│   │   ├── home.html
│   │   ├── result.html
│   │   ├── error.html
│   ├── static/
│   │   ├── css/
│   │   │   ├── styles.css
│   │   ├── js/
│   │   │   ├── script.js
│   │── app.py
│   │── utils.py
│── requirements.txt
│── README.md
│── .gitignore

## 📜 License
MIT License