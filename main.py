import pandas as pd
import sqlite3
from src.data_processing import generate_synthetic_data, store_data_to_db, load_data_from_db
from src.pattern_mining import find_frequent_itemsets_apriori, find_frequent_itemsets_fpgrowth, generate_association_rules, create_risk_model, predict_risk
from src.visualization import plot_support, plot_confidence

print("Starting the script...")

# Generate synthetic data
print("Generating synthetic data...")
patients_df, records_df = generate_synthetic_data(num_patients=30, num_records=100)
store_data_to_db(patients_df, records_df, 'data/patients.db')
print("Synthetic data generated and stored in the database.")

# Load data from database
print("Loading data from database...")
patients_df, records_df = load_data_from_db('data/patients.db')
print("Data loaded from database.")

# Process data
print("Processing data...")
records_df['visit_date'] = pd.to_datetime(records_df['visit_date'])
records_df['month'] = records_df['visit_date'].dt.to_period('M')
monthly_transactions = records_df.groupby('month')['patient_id'].apply(list)
print(f"Monthly Transactions: {monthly_transactions.head()}")
print("Data processed.")

# Run Apriori Algorithm
print("Running Apriori Algorithm...")
frequent_itemsets_apriori = find_frequent_itemsets_apriori(monthly_transactions, min_support=0.05)  # Lowering min_support
print(f"Frequent Itemsets Apriori: {frequent_itemsets_apriori}")
if not frequent_itemsets_apriori.empty:
    rules_apriori = generate_association_rules(frequent_itemsets_apriori, min_confidence=0.5)
    print("Apriori Algorithm completed.")
    print("Apriori Association Rules:")
    print(rules_apriori)
else:
    print("No frequent itemsets found using Apriori Algorithm.")

# Run FP-Growth Algorithm
print("Running FP-Growth Algorithm...")
frequent_itemsets_fpgrowth = find_frequent_itemsets_fpgrowth(monthly_transactions, min_support=0.05)  # Lowering min_support
print(f"Frequent Itemsets FP-Growth: {frequent_itemsets_fpgrowth}")
if not frequent_itemsets_fpgrowth.empty:
    rules_fpgrowth = generate_association_rules(frequent_itemsets_fpgrowth, min_confidence=0.5)
    print("FP-Growth Algorithm completed.")
    print("FP-Growth Association Rules:")
    print(rules_fpgrowth)
else:
    print("No frequent itemsets found using FP-Growth Algorithm.")

# Visualize the results for Apriori
if not frequent_itemsets_apriori.empty:
    print("Visualizing results for Apriori...")
    plot_support(frequent_itemsets_apriori)
    plot_confidence(rules_apriori)

# Visualize the results for FP-Growth
if not frequent_itemsets_fpgrowth.empty:
    print("Visualizing results for FP-Growth...")
    plot_support(frequent_itemsets_fpgrowth)
    plot_confidence(rules_fpgrowth)

# Create and evaluate risk model
print("Creating risk model...")
clf = create_risk_model(patients_df)
print("Risk model created and evaluated.")

# Predict risk for a new patient
age = 45
bmi = 28
risk_prediction = predict_risk(clf, age, bmi)
print(f"Predicted risk for age {age} and BMI {bmi}: {'High' if risk_prediction[0] == 1 else 'Low'}")

print("Script completed.")
