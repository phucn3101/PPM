from flask import Flask, jsonify, request, render_template
import webbrowser
import threading
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

from src.data_processing import generate_synthetic_data, store_data_to_db

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/generate-data', methods=['POST'])
def generate_data():
    data = request.get_json()
    num_patients = int(data.get('num_patients', 30))
    num_records = int(data.get('num_records', 100))

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

@app.route('/patient/<int:patient_id>/visits', methods=['GET'])
def get_patient_visits(patient_id):
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    cursor.execute("SELECT visit_date FROM records WHERE patient_id = ?", (patient_id,))
    visits = cursor.fetchall()
    conn.close()

    dates = [visit[0] for visit in visits]
    sns.set(style="darkgrid")
    plt.figure(figsize=(10, 6))
    plt.hist(dates, bins=12, color='blue', alpha=0.7)
    plt.title('Patient Visits Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Visits')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return f'<img src="data:image/png;base64,{plot_url}" />'

if __name__ == '__main__':
    app.run(debug=True)
