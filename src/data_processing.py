import pandas as pd
import numpy as np
import random

def generate_synthetic_data(num_patients=30, num_records=100):
    # Generate patient IDs
    patient_ids = [f'P{str(i).zfill(4)}' for i in range(num_patients)]

    # Generate visit dates
    date_range = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    visit_dates = np.random.choice(date_range, num_records)

    # Generate additional patient details
    ages = np.random.randint(18, 90, num_patients)
    genders = np.random.choice(['Male', 'Female'], num_patients)
    bmi = np.random.uniform(18, 40, num_patients)

    # Define diagnosis categories based on age
    def get_diagnosis(age):
        if age < 30:
            return np.random.choice(['Asthma', 'Diabetes'])
        elif age < 50:
            return np.random.choice(['Hypertension', 'Diabetes', 'Asthma'])
        elif age < 65:
            return np.random.choice(['Hypertension', 'Diabetes', 'COPD', 'Heart Disease'])
        else:
            return np.random.choice(['Hypertension', 'COPD', 'Heart Disease'])

    records = []

    for i in range(num_records):
        patient_id = random.choice(patient_ids)
        visit_date = random.choice(visit_dates)
        age = ages[patient_ids.index(patient_id)]
        gender = genders[patient_ids.index(patient_id)]
        bmi_value = bmi[patient_ids.index(patient_id)]
        diagnosis = get_diagnosis(age)
        records.append([patient_id, visit_date, age, gender, bmi_value, diagnosis])

    df = pd.DataFrame(records, columns=['patient_id', 'visit_date', 'age', 'gender', 'bmi', 'diagnosis'])
    return df
