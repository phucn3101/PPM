import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

def plot_support(frequent_itemsets, min_support=0.1, max_items=20):
    # Filter itemsets by minimum support
    filtered_itemsets = frequent_itemsets[frequent_itemsets['support'] >= min_support]
    
    # Sort itemsets by support
    sorted_itemsets = filtered_itemsets.sort_values(by='support', ascending=False)
    
    # Limit the number of itemsets
    limited_itemsets = sorted_itemsets.head(max_items)
    
    # Plot the support of the frequent itemsets
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(limited_itemsets)), limited_itemsets['support'], tick_label=[str(i) for i in limited_itemsets['itemsets']])
    plt.xticks(rotation=90)
    plt.xlabel('Itemsets')
    plt.ylabel('Support')
    plt.title('Support of Frequent Itemsets')
    plt.savefig('output/support_plot.png')
    plt.show()
    plt.close()

def plot_confidence(rules, min_confidence=0.5, max_rules=20):
    # Filter rules by minimum confidence
    filtered_rules = rules[rules['confidence'] >= min_confidence]
    
    # Sort rules by confidence
    sorted_rules = filtered_rules.sort_values(by='confidence', ascending=False)
    
    # Limit the number of rules
    limited_rules = sorted_rules.head(max_rules)
    
    # Plot the confidence of the association rules
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(limited_rules)), limited_rules['confidence'], tick_label=[f"{rule[0]} -> {rule[1]}" for rule in limited_rules[['antecedents', 'consequents']].values])
    plt.xticks(rotation=90)
    plt.xlabel('Rules')
    plt.ylabel('Confidence')
    plt.title('Confidence of Association Rules')
    plt.savefig('output/confidence_plot.png')
    plt.show()
    plt.close()

# def plot_patient_visits(patient_id):
#     conn = sqlite3.connect('data/patients.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT visit_date FROM records WHERE patient_id = ?", (patient_id,))
#     visits = cursor.fetchall()
#     conn.close()
    
#     if not visits:
#         return None

#     visit_dates = [pd.to_datetime(visit[0]) for visit in visits]

#     plt.figure(figsize=(15, 6))  # Adjust the figure size to make it longer
#     plt.hist(visit_dates, bins=len(visit_dates), width=0.3)  # Adjust the width to make the bars thinner
#     plt.xlabel('Visit Date')
#     plt.ylabel('Number of Visits')
#     plt.title(f'Visit Pattern for Patient {patient_id}')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
    
#     img_path = f'static/plots/{patient_id}_visits.png'
#     plt.savefig(img_path)
#     plt.close()
    
#     return img_path