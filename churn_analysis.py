import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('telco_churn.csv')

# Fix column names
df.columns = [col.strip() for col in df.columns]

# Create database
conn = sqlite3.connect(':memory:')
df.to_sql('churn', conn, index=False, if_exists='replace')

# Run SQL queries
queries = {
    'Q1_Churn_Distribution': "SELECT Churn, COUNT(*) as count FROM churn GROUP BY Churn;",
    'Q2_Contract_Impact': "SELECT Contract, COUNT(*) as total, SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned FROM churn GROUP BY Contract;",
    'Q3_Tenure_Analysis': "SELECT CASE WHEN tenure < 12 THEN '0-12mo' WHEN tenure < 24 THEN '12-24mo' ELSE '24+mo' END as tenure_group, COUNT(*) as customers FROM churn GROUP BY tenure_group;",
}

print("="*60)
print("CHURN ANALYSIS - SQL RESULTS")
print("="*60)

for name, query in queries.items():
    result = pd.read_sql_query(query, conn)
    print(f"\n{name}:")
    print(result.to_string())

# Visualizations
plt.figure(figsize=(16, 12))

# Plot 1: Churn distribution
plt.subplot(3, 3, 1)
churn_counts = df['Churn'].value_counts()
plt.pie(churn_counts, labels=['No Churn', 'Churn'], autopct='%1.1f%%', colors=['green', 'red'])
plt.title('Churn Distribution')

# Plot 2: Churn by contract
plt.subplot(3, 3, 2)
contract_churn = df.groupby('Contract')['Churn'].apply(lambda x: (x=='Yes').sum())
plt.bar(contract_churn.index, contract_churn.values, color=['blue', 'orange', 'green'])
plt.title('Churn by Contract Type')
plt.ylabel('Churn Count')

# Plot 3: Tenure vs Churn
plt.subplot(3, 3, 3)
plt.scatter(df['tenure'], df['Churn'].map({'No': 0, 'Yes': 1}), alpha=0.5)
plt.xlabel('Tenure (months)')
plt.ylabel('Churn (0=No, 1=Yes)')
plt.title('Tenure vs Churn')

# Plot 4: Monthly charges
plt.subplot(3, 3, 4)
df.boxplot(column='MonthlyCharges', by='Churn', ax=plt.gca())
plt.title('Monthly Charges by Churn')
plt.suptitle('')

# Plot 5: Internet service
plt.subplot(3, 3, 5)
internet_churn = df[df['Churn']=='Yes']['InternetServiceType'].value_counts()
plt.bar(internet_churn.index, internet_churn.values, color=['red', 'orange', 'yellow'])
plt.title('Churn by Internet Service')
plt.xticks(rotation=45)

# Plot 6: Total charges
plt.subplot(3, 3, 6)
plt.hist(df[df['Churn']=='No']['TotalCharges'].astype(float, errors='ignore'), alpha=0.6, label='No Churn', bins=30)
plt.hist(df[df['Churn']=='Yes']['TotalCharges'].astype(float, errors='ignore'), alpha=0.6, label='Churn', bins=30)
plt.xlabel('Total Charges')
plt.ylabel('Count')
plt.title('Total Charges Distribution')
plt.legend()

# Plot 7: Contract length
plt.subplot(3, 3, 7)
contract_data = df['Contract'].value_counts()
plt.bar(contract_data.index, contract_data.values, color=['purple', 'brown', 'pink'])
plt.title('Contract Distribution')

# Plot 8: Customer service calls
plt.subplot(3, 3, 8)
if 'numAdminTickets' in df.columns:
    df.boxplot(column='numAdminTickets', by='Churn', ax=plt.gca())
    plt.title('Support Tickets by Churn')
    plt.suptitle('')

# Plot 9: Churn rate summary
plt.subplot(3, 3, 9)
churn_rate = (df['Churn']=='Yes').sum() / len(df) * 100
no_churn_rate = 100 - churn_rate
plt.bar(['No Churn', 'Churn'], [no_churn_rate, churn_rate], color=['green', 'red'])
plt.ylabel('Percentage (%)')
plt.title('Overall Churn Rate')

plt.tight_layout()
plt.savefig('churn_analysis.png', dpi=300, bbox_inches='tight')
print("\n✅ Analysis visualizations saved!")

conn.close()
