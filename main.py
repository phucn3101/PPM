import time
import pandas as pd
from src.data_processing import generate_synthetic_data
from src.pattern_mining import find_frequent_itemsets, generate_association_rules
from src.visualization import plot_support, plot_confidence

def main():
    start_time = time.time()

    print("Starting the script...")

    # Generate synthetic data
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    df.to_csv('data/synthetic_data.csv', index=False)
    print("Synthetic data generated and saved.")

    # Load and process data
    print("Loading and processing data...")
    df = pd.read_csv('data/synthetic_data.csv')
    print(f"Data shape: {df.shape}")
    print(f"Data sample:\n{df.head()}")

    df['visit_date'] = pd.to_datetime(df['visit_date'])
    df['month'] = df['visit_date'].dt.to_period('M')
    monthly_transactions = df.groupby('month')['patient_id'].apply(list)
    print(f"Monthly transactions:\n{monthly_transactions.head()}")
    print("Data loaded and processed.")

    # Find frequent itemsets
    print("Finding frequent itemsets...")
    frequent_itemsets_start = time.time()
    frequent_itemsets = find_frequent_itemsets(monthly_transactions, min_support=0.2)  # Adjust min_support
    print(f"Frequent itemsets found in {time.time() - frequent_itemsets_start:.2f} seconds")
    print(frequent_itemsets)

    # Print frequent itemsets before generating rules
    print("Frequent itemsets:")
    print(frequent_itemsets)

    # Generate association rules
    print("Generating association rules...")
    rules_start = time.time()
    rules = generate_association_rules(frequent_itemsets, min_threshold=0.8)  # Adjust min_threshold
    print(f"Association rules generated in {time.time() - rules_start:.2f} seconds")
    print(rules)

    # Visualize the results
    print("Visualizing the results...")
    plot_support(frequent_itemsets, min_support=0.2, max_items=20)  # Adjust as needed
    plot_confidence(rules, min_confidence=0.6, max_rules=20)  # Adjust as needed
    print("Results visualized.")

    print(f"Total execution time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
