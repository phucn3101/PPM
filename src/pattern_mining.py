import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def find_frequent_itemsets(transactions, min_support=0.1):
    # Create a list of unique items
    unique_items = list(set(item for transaction in transactions for item in transaction))

    # Create a binary matrix
    binary_matrix = []
    for transaction in transactions:
        binary_matrix.append([1 if item in transaction else 0 for item in unique_items])
    
    # Convert binary matrix to DataFrame
    one_hot_df = pd.DataFrame(binary_matrix, columns=unique_items)
    
    # Convert to boolean DataFrame
    one_hot_df = one_hot_df.astype(bool)
    
    # Use apriori to find frequent itemsets
    frequent_itemsets = apriori(one_hot_df, min_support=min_support, use_colnames=True)
    return frequent_itemsets

def generate_association_rules(frequent_itemsets, min_threshold=0.7):
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_threshold)
    return rules
