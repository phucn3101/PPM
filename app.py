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
from pattern_mining import find_periodic_patterns

# load_dotenv()
# HF_API_TOKEN = os.getenv('HF_API_TOKEN')

load_dotenv()
HUGGING_FACE_MODEL = os.getenv("HUGGING_FACE_MODEL")
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_MODEL")

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained(HUGGING_FACE_MODEL, use_auth_token=HUGGING_FACE_TOKEN)
model = AutoModelForSequenceClassification.from_pretrained(HUGGING_FACE_MODEL, use_auth_token=HUGGING_FACE_TOKEN)
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
    num_patients = int(data.get('num_patients', 30))
    num_records = int(data.get('num_records', 500))

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

# @app.route('/patient/<string:patient_id>/visits', methods=['GET'])
@app.route('/patient/<string:patient_id>/visits', methods=['GET'])
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
HUGGING_FACE_API_KEY = "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"

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

@app.route('/patient/<patient_id>/patterns')
def patient_patterns(patient_id):
    # Fetch patient visits from the database
    visits = session.query(Visit).filter_by(patient_id=patient_id).all()

    # Prepare the data in the format required by find_periodic_patterns
    visit_dates = [visit.date for visit in visits]

    # Process the visits to find periodic patterns
    patterns = find_periodic_patterns(visit_dates)

    # Render the template with the patterns
    return render_template('patterns.html', patient_id=patient_id, patterns=patterns)

if __name__ == '__main__':
    app.run(debug=True)
