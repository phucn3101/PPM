from flask import Flask, jsonify, request, render_template
import requests
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd
from src.data_processing import generate_synthetic_data, store_data_to_db
from dotenv import load_dotenv
import os
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from src.pattern_mining import find_periodic_patterns, find_patterns, find_periodic_patterns_apriori, find_periodic_patterns_fpgrowth
# from flask_sqlalchemy import SQLAlchemy

# load_dotenv()
# HF_API_TOKEN = os.getenv('HF_API_TOKEN')

load_dotenv()
HUGGING_FACE_MODEL = os.getenv("HUGGING_FACE_MODEL")
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_MODEL")

app = Flask(__name__)

DATABASE = 'data/patients.db'

def get_db_connection():
    conn = sqlite3.connect('data/patients.db')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_patient_visits(patient_id):
    # conn = get_db_connection()
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    visits = cursor.execute('SELECT visit_date FROM records WHERE patient_id = ?', (patient_id,)).fetchall()
    conn.close()
    return visits

tokenizer = AutoTokenizer.from_pretrained(HUGGING_FACE_MODEL, token=HUGGING_FACE_TOKEN) # use_auth_token changed to token
model = AutoModelForSequenceClassification.from_pretrained(HUGGING_FACE_MODEL, token=HUGGING_FACE_TOKEN) # use_auth_token changed to token
classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

def analyze_text(text):
    try:
        # Get classification result
        result = classifier(text)
        # Extract label and score
        label = result[0]['label']
        score = result[0]['score']

        # Determine severity and hospitalization rate
        severity = "Unknown"
        hospitalization_rate = 0

        if label == "LABEL_1":
            severity = "Mild"
            hospitalization_rate = score * 10  # Example calculation
        elif label == "LABEL_2":
            severity = "Moderate"
            hospitalization_rate = score * 30
        elif label == "LABEL_3":
            severity = "Severe"
            hospitalization_rate = score * 50

        return {"severity": severity, "hospitalization_rate": hospitalization_rate}
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-data', methods=['POST'])
def generate_data():
    data = request.get_json()
    num_patients = int(data.get('num_patients', 500))
    num_records = int(data.get('num_records', 3000))

    patients_df, records_df = generate_synthetic_data(num_patients, num_records)
    store_data_to_db(patients_df, records_df, 'data/patients.db')

    return jsonify({'message': 'Synthetic data generated and stored in the database.'}), 201

@app.route('/patients', methods=['GET'])
def get_patients():
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return render_template('patients.html', patients=patients)

@app.route('/records', methods=['GET'])
def get_records():
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records")
    records = cursor.fetchall()
    conn.close()
    return jsonify(records)

@app.route('/patients/<string:patient_id>/visits', methods=['GET'])
def get_patient_visits(patient_id):
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    cursor.execute("SELECT visit_date FROM records WHERE patient_id = ?", (patient_id,))
    visits = cursor.fetchall()
    conn.close()

    if not visits:
        return "No visits found for this patient.", 404

    dates = [visit[0] for visit in visits]
    visit_dates = pd.to_datetime(dates)

    sns.set(style="darkgrid")
    plt.figure(figsize=(20, 10))

    # Dynamically set min and max date range
    min_date = visit_dates.min()
    max_date = visit_dates.max()

    plt.hist(visit_dates, bins=30, color='blue', alpha=0.7, width=5)
    plt.title('Patient Visits Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Visits')

    plt.xlim(min_date, max_date)  # Set dynamic date range
    plt.ylim(0, 10)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    chart_url = f'data:image/png;base64,{plot_url}'
    return render_template('patient_visits.html', chart_url=chart_url)

@app.route('/clear-data', methods=['POST'])
def clear_data():
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients")
    cursor.execute("DELETE FROM records")
    conn.commit()
    conn.close()
    return jsonify({'message': 'Data cleared from the database.'}), 200

HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
HUGGING_FACE_API_KEY = "<HF API key place holder>"

headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
}

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    result = classifier(text)[0]
    analysis = {
        'label': result['label'],
        'score': result['score']
    }
    return render_template('analysis_result.html', text=text, analysis=analysis)

@app.route('/patterns', methods=['GET'])
def patterns():
    # Assuming you have a function `find_patterns` that does the pattern mining
    patterns = find_patterns()
    return jsonify(patterns)

# @app.route('/patients/<patient_id>/patterns')
# def patient_patterns(patient_id):
#     visits = fetch_patient_visits(patient_id)
#     visit_dates = [visit['visit_date'] for visit in visits]
#     patterns = find_periodic_patterns(visit_dates)
#     return render_template('patterns.html', patient_id=patient_id, patterns=patterns)

# @app.route('/patients/<patient_id>/patterns')
# def patient_patterns(patient_id):
#     visits = fetch_patient_visits(patient_id)
#     visit_dates = [visit[0] for visit in visits]  # Access tuple elements using integer indices
#     patterns = find_periodic_patterns(visit_dates)
#     return render_template('patterns.html', patient_id=patient_id, patterns=patterns)

@app.route('/patients/<patient_id>/patterns')
def patient_patterns(patient_id):
    visits = fetch_patient_visits(patient_id)
    visit_dates = [visit[0] for visit in visits]

    apriori_patterns = find_periodic_patterns_apriori(visit_dates)
    fpgrowth_patterns = find_periodic_patterns_fpgrowth(visit_dates)

    return render_template('patterns.html', patient_id=patient_id, apriori_patterns=apriori_patterns, fpgrowth_patterns=fpgrowth_patterns)

# @app.route('/patient/<patient_id>/patterns/apriori')
# def patient_patterns_apriori(patient_id):
#     visits = fetch_patient_visits(patient_id)
#     visit_dates = [visit[0] for visit in visits]  # Accessing by index
#     patterns = find_periodic_patterns_apriori(visit_dates)
#     return render_template('patterns.html', patient_id=patient_id, patterns=patterns)

@app.route('/patients/<patient_id>/patterns/apriori')
def patient_patterns_apriori(patient_id):
    # Fetch patient visits from the database
    visits = fetch_patient_visits(patient_id)

    # Prepare the data in the format required by find_periodic_patterns
    visit_dates = [visit[0] for visit in visits]  # Accessing by index

    # Process the visits to find periodic patterns using Apriori
    apriori_patterns = find_periodic_patterns_apriori(visit_dates)

    # Render the template with the patterns
    return render_template('patterns_apriori.html', patient_id=patient_id, apriori_patterns=apriori_patterns)

@app.route('/patients/<patient_id>/patterns/fpgrowth')
def patient_patterns_fpgrowth(patient_id):
    visits = fetch_patient_visits(patient_id)
    visit_dates = [visit[0] for visit in visits]  # Accessing by index
    patterns = find_periodic_patterns_fpgrowth(visit_dates)
    return render_template('patterns.html', patient_id=patient_id, patterns=patterns)

if __name__ == '__main__':
    app.run(debug=True)
