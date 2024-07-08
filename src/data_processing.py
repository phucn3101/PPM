import pandas as pd
import numpy as np

def generate_synthetic_data():
    np.random.seed(42)
    num_patients = 10  # Reduce the number of patients temporarily
    num_records = 50  # Reduce the number of records temporarily

    patient_ids = np.random.randint(1, num_patients + 1, size=num_records)
    visit_dates = pd.date_range(start='2022-01-01', periods=num_records, freq='D').tolist()
    visit_dates = np.random.choice(visit_dates, size=num_records)

    data = {'patient_id': patient_ids, 'visit_date': visit_dates}
    df = pd.DataFrame(data)
    return df
