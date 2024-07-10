from flask import Flask, jsonify, request
import webbrowser
import threading
import sqlite3
from src.data_processing import generate_synthetic_data, store_data_to_db

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

# def open_browser():
#     webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # threading.Timer(1, open_browser).start()
    app.run(debug=True)

@app.route('/generate-data', methods=['POST'])
def generate_data():
    data = request.get_json()
    num_patients = data.get('num_patients', 30)
    num_records = data.get('num_records', 100)

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
    return jsonify(patients)

@app.route('/records', methods=['GET'])
def get_records():
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records")
    records = cursor.fetchall()
    conn.close()
    return jsonify(records)
