from flask import Flask, jsonify, request, render_template
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd
from src.data_processing import generate_synthetic_data, store_data_to_db

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

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

    plt.hist(visit_dates, bins=30, color='blue', alpha=0.7, width=20)
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


# @app.route('/patient/<string:patient_id>/visits', methods=['GET'])
# def get_patient_visits(patient_id):
#     conn = sqlite3.connect('data/patients.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT visit_date FROM records WHERE patient_id = ?", (patient_id,))
#     visits = cursor.fetchall()
#     conn.close()

#     if not visits:
#         return "No visits found for this patient.", 404

#     visit_dates = [visit[0] for visit in visits]
#     visit_dates = pd.to_datetime(visit_dates)

#     sns.set(style="darkgrid")
#     plt.figure(figsize=(20, 10))
#     plt.hist(visit_dates, bins=len(visit_dates.unique()), color='blue', alpha=0.7)
#     plt.title('Patient Visits Over Time')
#     plt.xlabel('Date')
#     plt.ylabel('Number of Visits')
#     plt.xticks(rotation=45)

#     img = io.BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     plot_url = base64.b64encode(img.getvalue()).decode()

#     chart_url = f'data:image/png;base64,{plot_url}'
#     return render_template('patient_visits.html', chart_url=chart_url)


# @app.route('/patient/<string:patient_id>/visits', methods=['GET'])
# def get_patient_visits(patient_id):
#     conn = sqlite3.connect('data/patients.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT visit_date FROM records WHERE patient_id = ?", (patient_id,))
#     visits = cursor.fetchall()
#     conn.close()

#     if not visits:
#         return "No visits found for this patient.", 404

#     dates = [visit[0] for visit in visits]
#     visit_dates = pd.to_datetime(dates)
    
#     sns.set(style="darkgrid")
#     plt.figure(figsize=(20, 10))  # Adjusted size for better readability

#     # Define fixed date range (adjust according to your data range)
#     min_date = pd.to_datetime('2020-01-01')
#     max_date = pd.to_datetime('2022-12-31')

#     plt.hist(visit_dates, bins=30, color='blue', alpha=0.7, width=0.8)
#     plt.title('Patient Visits Over Time')
#     plt.xlabel('Date')
#     plt.ylabel('Number of Visits')

#     plt.xlim(min_date, max_date)  # Set fixed date range
#     plt.ylim(0, 10)  # Set fixed visit range (adjust if necessary)

#     img = io.BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     plot_url = base64.b64encode(img.getvalue()).decode()

#     chart_url = f'data:image/png;base64,{plot_url}'
#     return render_template('patient_visits.html', chart_url=chart_url)


if __name__ == '__main__':
    app.run(debug=True)
