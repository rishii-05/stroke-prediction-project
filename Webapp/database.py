"""
Database management for user authentication and prediction history
Uses SQLite for simplicity - can be upgraded to PostgreSQL/MySQL for production
"""
import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'stroke_app.db')

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            theme_preference TEXT DEFAULT 'light'
        )
    ''')
    
    # Prediction history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            age INTEGER,
            gender TEXT,
            hypertension INTEGER,
            heart_disease INTEGER,
            avg_glucose_level REAL,
            bmi REAL,
            smoking_status TEXT,
            prediction_result INTEGER,
            probability REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password, full_name):
    """Create new user account"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, full_name))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, user_id
    except sqlite3.IntegrityError:
        return False, "Username or email already exists"
    except Exception as e:
        return False, str(e)

def verify_user(username, password):
    """Verify user credentials"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    
    cursor.execute('''
        SELECT id, username, email, full_name, theme_preference
        FROM users
        WHERE username = ? AND password_hash = ?
    ''', (username, password_hash))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return True, dict(user)
    return False, None

def get_user_by_id(user_id):
    """Get user information by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, email, full_name, created_at, theme_preference
        FROM users
        WHERE id = ?
    ''', (user_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    return dict(user) if user else None

def update_theme_preference(user_id, theme):
    """Update user's theme preference"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users
        SET theme_preference = ?
        WHERE id = ?
    ''', (theme, user_id))
    
    conn.commit()
    conn.close()

def save_prediction(user_id, input_data, prediction_result, probability):
    """Save prediction to history"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # input_data order: gender, age, hypertension, heart_disease, ever_married, 
        #                   work_type, Residence_type, avg_glucose_level, bmi, smoking_status
        gender_map = {0: 'Female', 1: 'Male'}
        smoking_map = {0: 'Unknown', 1: 'Formerly Smoked', 2: 'Never Smoked', 3: 'Currently Smokes'}
        
        cursor.execute('''
            INSERT INTO predictions (
                user_id, age, gender, hypertension, heart_disease,
                avg_glucose_level, bmi, smoking_status, prediction_result, probability
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            int(input_data[1]),  # age
            gender_map.get(input_data[0], 'Unknown'),  # gender
            int(input_data[2]),  # hypertension
            int(input_data[3]),  # heart_disease
            float(input_data[7]),  # avg_glucose_level
            float(input_data[8]),  # bmi
            smoking_map.get(input_data[9], 'Unknown'),  # smoking_status
            prediction_result,
            probability
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving prediction: {e}")
        return False

def get_user_predictions(user_id, limit=10):
    """Get user's prediction history"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, prediction_date, age, gender, hypertension, heart_disease,
               avg_glucose_level, bmi, smoking_status, prediction_result, probability
        FROM predictions
        WHERE user_id = ?
        ORDER BY prediction_date DESC
        LIMIT ?
    ''', (user_id, limit))
    
    predictions = cursor.fetchall()
    conn.close()
    
    return [dict(pred) for pred in predictions]

def get_user_stats(user_id):
    """Get user statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            COUNT(*) as total_predictions,
            AVG(probability) as avg_risk,
            MAX(probability) as max_risk,
            MIN(prediction_date) as first_prediction
        FROM predictions
        WHERE user_id = ?
    ''', (user_id,))
    
    stats = cursor.fetchone()
    conn.close()
    
    return dict(stats) if stats else None

# Initialize database on import
init_db()
