import pandas as pd
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from datetime import datetime

def generate_association_rules(frequent_itemsets, min_confidence=0.5):
    if frequent_itemsets.empty:
        print("No frequent itemsets found.")
        return pd.DataFrame()
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    return rules

def preprocess_transactions(dates):
    transaction_list = [[date.strftime('%A'), date.strftime('%B')] for date in dates]
    unique_items = set(item for transaction in transaction_list for item in transaction)
    binary_matrix = []
    for transaction in transaction_list:
        binary_matrix.append([1 if item in transaction else 0 for item in unique_items])
        
    one_hot_df = pd.DataFrame(binary_matrix, columns=list(unique_items)).astype(bool)
    return one_hot_df

def find_frequent_itemsets_apriori(transactions, min_support=0.1):
    transaction_list = list(transactions)
    unique_items = set(item for transaction in transaction_list for item in transaction)
    binary_matrix = []
    for transaction in transaction_list:
        binary_matrix.append([1 if item in transaction else 0 for item in unique_items])
        
    one_hot_df = pd.DataFrame(binary_matrix, columns=list(unique_items)).astype(bool)
    frequent_itemsets = apriori(one_hot_df, min_support=min_support, use_colnames=True)
    return frequent_itemsets

# def find_periodic_patterns_apriori(dates, min_support=0.1, min_confidence=0.5):
#     dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f') for date in dates]
#     transactions = [[date.strftime('%A'), date.strftime('%B')] for date in dates]
#     frequent_itemsets = find_frequent_itemsets_apriori(transactions, min_support)
#     rules = generate_association_rules(frequent_itemsets, min_confidence)
#     patterns = rules[['antecedents', 'consequents', 'support', 'confidence']].to_dict('records')
#     return patterns

def find_periodic_patterns_apriori(dates):
    dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f') for date in dates]
    transactions = [[date.strftime('%A'), date.strftime('%B')] for date in dates]
    frequent_itemsets = find_frequent_itemsets_apriori(transactions)
    patterns = [{'pattern': ', '.join(itemset), 'frequency': support} for itemset, support in zip(frequent_itemsets['itemsets'], frequent_itemsets['support'])]
    print("Apriori Patterns: ", patterns)
    return patterns

def find_frequent_itemsets_apriori_improved(dates, min_support=0.1):
    one_hot_df = preprocess_transactions(dates)
    frequent_itemsets = apriori(one_hot_df, min_support=min_support, use_colnames=True)
    patterns = [{'pattern': ', '.join(itemset), 'frequency': support} for itemset, support in zip(frequent_itemsets['itemsets'], frequent_itemsets['support'])]
    return patterns

def find_frequent_itemsets_fpgrowth(transactions, min_support=0.1):
    transaction_list = list(transactions)
    unique_items = set(item for transaction in transaction_list for item in transaction)
    
    binary_matrix = []
    for transaction in transaction_list:
        binary_matrix.append([1 if item in transaction else 0 for item in unique_items])
        
    one_hot_df = pd.DataFrame(binary_matrix, columns=list(unique_items)).astype(bool)
    frequent_itemsets = fpgrowth(one_hot_df, min_support=min_support, use_colnames=True)
    return frequent_itemsets

# def find_periodic_patterns_fpgrowth(dates, min_support=0.1, min_confidence=0.5):
#     dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f') for date in dates]
#     transactions = [[date.strftime('%A'), date.strftime('%B')] for date in dates]
#     frequent_itemsets = find_frequent_itemsets_fpgrowth(transactions, min_support)
#     rules = generate_association_rules(frequent_itemsets, min_confidence)
#     patterns = rules[['antecedents', 'consequents', 'support', 'confidence']].to_dict('records')
#     return patterns

def find_periodic_patterns_fpgrowth(dates):
    dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f') for date in dates]
    transactions = [[date.strftime('%A'), date.strftime('%B')] for date in dates]
    frequent_itemsets = find_frequent_itemsets_fpgrowth(transactions)
    patterns = [{'pattern': ', '.join(itemset), 'frequency': support} for itemset, support in zip(frequent_itemsets['itemsets'], frequent_itemsets['support'])]
    print("FP-Growth Patterns: ", patterns)
    return patterns

def find_frequent_itemsets_fpgrowth_improved(dates, min_support=0.1):
    one_hot_df = preprocess_transactions(dates)
    frequent_itemsets = fpgrowth(one_hot_df, min_support=min_support, use_colnames=True)
    patterns = [{'pattern': ', '.join(itemset), 'frequency': support} for itemset, support in zip(frequent_itemsets['itemsets'], frequent_itemsets['support'])]
    return patterns

# def create_risk_model(df):
#     from sklearn.model_selection import train_test_split
#     from sklearn.ensemble import RandomForestClassifier
#     from sklearn.metrics import classification_report

#     df['high_risk'] = df['diagnosis'].apply(lambda x: 1 if x in ['Heart Disease', 'COPD'] else 0)
#     X = df[['age', 'bmi']]
#     y = df['high_risk']

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#     clf = RandomForestClassifier(n_estimators=100, random_state=42)
#     clf.fit(X_train, y_train)

#     y_pred = clf.predict(X_test)
#     print(classification_report(y_test, y_pred))

#     return clf

# def predict_risk(clf, age, bmi):
#     data = pd.DataFrame({'age': [age], 'bmi': [bmi]})
#     return clf.predict(data)

def find_periodic_patterns(dates):
    # Implement your periodic pattern mining logic here.
    # For example, this function should return a list of patterns and their frequencies.
    patterns = [
        {'pattern': 'Visit every Monday', 'frequency': 5},
        {'pattern': 'Monthly check-up', 'frequency': 3}
    ]
    return patterns

def find_patterns():
    # Your logic to find patterns
    # For example:
    patterns = [
        {'pattern': 'Pattern A', 'count': 10},
        {'pattern': 'Pattern B', 'count': 7},
        # Add more patterns as needed
    ]
    return patterns
