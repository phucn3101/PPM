import matplotlib.pyplot as plt

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
