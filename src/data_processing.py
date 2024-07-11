# import pandas as pd
# from faker import Faker
# import random
# import sqlite3

# def generate_synthetic_data(num_patients=30, num_records=500):
#     fake = Faker()
#     patients = []
#     records = []

#     remaining_records = num_records

#     for i in range(num_patients):
#         patient_id = fake.uuid4()
#         age = random.randint(18, 90)
#         gender = random.choice(['Male', 'Female'])
#         address = fake.address()
#         phone_number = fake.phone_number()
#         email = fake.email()
#         bmi = round(random.uniform(15.0, 40.0), 1)

#         if age < 30:
#             diagnosis = random.choice(['Healthy', 'Cold', 'Flu', 'Allergies'])
#         elif age < 50:
#             diagnosis = random.choice(['Healthy', 'Hypertension', 'Diabetes', 'Asthma'])
#         else:
#             diagnosis = random.choice(['Heart Disease', 'COPD', 'Diabetes', 'Hypertension', 'Cancer'])

#         patients.append({
#             'patient_id': patient_id,
#             'age': age,
#             'gender': gender,
#             'address': address,
#             'phone_number': phone_number,
#             'email': email,
#             'bmi': bmi,
#             'diagnosis': diagnosis
#         })

#         if i < num_patients - 1:
#             num_patient_records = random.randint(1, remaining_records - (num_patients - i - 1))
#         else:
#             num_patient_records = remaining_records

#         remaining_records -= num_patient_records

#         for _ in range(num_patient_records):
#             visit_date = fake.date_between(start_date='-3y', end_date='today')
#             records.append({
#                 'patient_id': patient_id,
#                 'visit_date': visit_date,
#                 'diagnosis': diagnosis
#             })

#     patients_df = pd.DataFrame(patients)
#     records_df = pd.DataFrame(records)

#     return patients_df, records_df

# def store_data_to_db(patients_df, records_df, db_path):
#     conn = sqlite3.connect(db_path)
#     patients_df.to_sql('patients', conn, if_exists='replace', index=False)
#     records_df.to_sql('records', conn, if_exists='replace', index=False)
#     conn.close()

# def load_data_from_db(db_path):
#     conn = sqlite3.connect(db_path)
#     patients_df = pd.read_sql_query("SELECT * FROM patients", conn)
#     records_df = pd.read_sql_query("SELECT * FROM records", conn)
#     conn.close()

#     return patients_df, records_df

import pandas as pd
import random
import numpy as np
import uuid
from datetime import datetime, timedelta
import sqlite3

def generate_vietnamese_name():
    first_names = ["Anh", "Bình", "Chi", "Dũng", "Hà", "Hải", "Hân", "Hiền", "Hoàng", "Hùng", "Khánh", "Lan", "Linh", "Minh", "Nga", "Ngọc", "Phong", "Phương", "Quân", "Quỳnh", "Sơn", "Thảo", "Thiên", "Thu", "Trang", "Trung", "Tuấn", "Vân", "Vy", "Yến"]
    last_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Huỳnh", "Hoàng", "Phan", "Vũ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý"]
    middle_names = ["Thị", "Văn", "Hữu", "Thanh", "Kim", "Minh", "Nhật", "Phúc", "Gia", "Khánh", "Hồng", "Xuân", "Đình", "Ngọc", "Tường"]

    first_name = random.choice(first_names)
    middle_name = random.choice(middle_names)
    last_name = random.choice(last_names)

    return f"{last_name} {middle_name} {first_name}"

def generate_synthetic_data(num_patients, num_records):
    # Define patient attributes
    patient_ids = [str(uuid.uuid4()) for _ in range(num_patients)]
    names = [generate_vietnamese_name() for _ in range(num_patients)]
    ages = np.random.randint(18, 90, size=num_patients)
    genders = ['Male', 'Female']
    diagnoses = ['Cold', 'Flu', 'Allergy', 'Heart Disease', 'COPD']

    # Define severity and age factors
    diagnosis_severity = {
        'Cold': 0.1,
        'Flu': 0.2,
        'Allergy': 0.3,
        'Heart Disease': 0.8,
        'COPD': 0.9
    }

    age_factor = lambda age: 0.1 if age < 30 else 0.2 if age < 50 else 0.5

    # Generate patients DataFrame
    patients = []
    for patient_id, name, age in zip(patient_ids, names * (num_patients // len(names) + 1), ages):
        gender = random.choice(genders)
        diagnosis = random.choices(diagnoses, k=1)[0]
        patients.append((patient_id, name, age, gender, diagnosis))

    patients_df = pd.DataFrame(patients, columns=['patient_id', 'name', 'age', 'gender', 'diagnosis'])

    # Generate records DataFrame
    records = []
    start_date = datetime.now() - timedelta(days=365)  # One year back

    for patient_id, age, diagnosis in zip(patient_ids, ages, patients_df['diagnosis']):
        num_visits = int((num_records * (diagnosis_severity[diagnosis] + age_factor(age))) / num_patients)
        for _ in range(num_visits):
            visit_date = start_date + timedelta(days=random.randint(0, 365))
            records.append((patient_id, visit_date))

    records_df = pd.DataFrame(records, columns=['patient_id', 'visit_date'])

    return patients_df, records_df

def store_data_to_db(patients_df, records_df, db_path):
    conn = sqlite3.connect(db_path)
    patients_df.to_sql('patients', conn, if_exists='replace', index=False)
    records_df.to_sql('records', conn, if_exists='replace', index=False)
    conn.close()
