import pandas as pd
from faker import Faker
import random
import sqlite3

def generate_synthetic_data(num_patients=30, num_records=500):
    fake = Faker()
    patients = []
    records = []

    remaining_records = num_records

    for i in range(num_patients):
        patient_id = fake.uuid4()
        age = random.randint(1, 100)
        gender = random.choice(['Male', 'Female'])
        address = fake.address()
        phone_number = fake.phone_number()
        email = fake.email()
        bmi = round(random.uniform(15.0, 40.0), 1)

        if age < 30:
            diagnosis = random.choice(['Healthy', 'Cold', 'Flu', 'Allergies'])
        elif age < 50:
            diagnosis = random.choice(['Healthy', 'Hypertension', 'Diabetes', 'Asthma'])
        else:
            diagnosis = random.choice(['Heart Disease', 'COPD', 'Diabetes', 'Hypertension', 'Cancer'])

        patients.append({
            'patient_id': patient_id,
            'age': age,
            'gender': gender,
            'address': address,
            'phone_number': phone_number,
            'email': email,
            'bmi': bmi,
            'diagnosis': diagnosis
        })

        if i < num_patients - 1:
            num_patient_records = random.randint(1, remaining_records - (num_patients - i - 1))
        else:
            num_patient_records = remaining_records

        remaining_records -= num_patient_records

        for _ in range(num_patient_records):
            visit_date = fake.date_between(start_date='-3y', end_date='today')
            records.append({
                'patient_id': patient_id,
                'visit_date': visit_date,
                'diagnosis': diagnosis
            })

    patients_df = pd.DataFrame(patients)
    records_df = pd.DataFrame(records)

    return patients_df, records_df

def store_data_to_db(patients_df, records_df, db_path):
    conn = sqlite3.connect(db_path)
    patients_df.to_sql('patients', conn, if_exists='replace', index=False)
    records_df.to_sql('records', conn, if_exists='replace', index=False)
    conn.close()

def load_data_from_db(db_path):
    conn = sqlite3.connect(db_path)
    patients_df = pd.read_sql_query("SELECT * FROM patients", conn)
    records_df = pd.read_sql_query("SELECT * FROM records", conn)
    conn.close()

    return patients_df, records_df
