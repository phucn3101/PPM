import pandas as pd
from src.data_processing import generate_synthetic_data
from src.pattern_mining import find_frequent_itemsets_apriori, find_frequent_itemsets_fpgrowth, generate_association_rules, create_risk_model, predict_risk
from src.visualization import plot_support, plot_confidence

print("Starting the script...")

# Generate synthetic data
print("Generating synthetic data...")
df = generate_synthetic_data(num_patients=30, num_records=100)
df.to_csv('data/synthetic_data.csv', index=False)
print("Synthetic data generated and saved.")

# Load and process data
print("Loading and processing data...")
df = pd.read_csv('data/synthetic_data.csv')
df['visit_date'] = pd.to_datetime(df['visit_date'])
df['month'] = df['visit_date'].dt.to_period('M')
monthly_transactions = df.groupby('month')['patient_id'].apply(list)
print("Data loaded and processed.")

# Run Apriori Algorithm
print("Running Apriori Algorithm...")
frequent_itemsets_apriori = find_frequent_itemsets_apriori(monthly_transactions, min_support=0.1)
rules_apriori = generate_association_rules(frequent_itemsets_apriori, min_confidence=0.5)
print("Apriori Algorithm completed.")

# Run FP-Growth Algorithm
print("Running FP-Growth Algorithm...")
frequent_itemsets_fpgrowth = find_frequent_itemsets_fpgrowth(monthly_transactions, min_support=0.1)
rules_fpgrowth = generate_association_rules(frequent_itemsets_fpgrowth, min_confidence=0.5)
print("FP-Growth Algorithm completed.")

# Print results for comparison
print("Apriori Frequent Itemsets:")
print(frequent_itemsets_apriori)
print("FP-Growth Frequent Itemsets:")
print(frequent_itemsets_fpgrowth)

print("Apriori Association Rules:")
print(rules_apriori)
print("FP-Growth Association Rules:")
print(rules_fpgrowth)

# Visualize the results for Apriori
print("Visualizing results for Apriori...")
plot_support(frequent_itemsets_apriori)
plot_confidence(rules_apriori)

# Visualize the results for FP-Growth
print("Visualizing results for FP-Growth...")
plot_support(frequent_itemsets_fpgrowth)
plot_confidence(rules_fpgrowth)

# Create and evaluate risk model
print("Creating risk model...")
clf = create_risk_model(df)
print("Risk model created and evaluated.")

# Predict risk for a new patient
age = 45
bmi = 28
risk_prediction = predict_risk(clf, age, bmi)
print(f"Predicted risk for age {age} and BMI {bmi}: {'High' if risk_prediction[0] == 1 else 'Low'}")

print("Script completed.")
