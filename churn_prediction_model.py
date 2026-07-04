import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('telco_churn.csv')

# Clean column names
df.columns = [col.strip() for col in df.columns]

# Prepare features
categorical_cols = df.select_dtypes(include='object').columns.tolist()
categorical_cols.remove('Churn')  # Remove target

# Encode categorical variables
le_dict = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    le_dict[col] = le

# Encode target
df['Churn'] = (df['Churn'] == 'Yes').astype(int)

# Select features
X = df.drop('Churn', axis=1)
y = df['Churn']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Evaluation
print("="*60)
print("CHURN PREDICTION MODEL - RESULTS")
print("="*60)

print(f"\nModel Accuracy: {model.score(X_test, y_test):.4f}")
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['No Churn', 'Churn']))

# Feature importance
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': np.abs(model.coef_[0])
}).sort_values('Coefficient', ascending=False).head(10)

print("\nTop 10 Most Important Features:")
print(feature_importance.to_string())

# Visualizations
plt.figure(figsize=(14, 10))

# Plot 1: Confusion Matrix
plt.subplot(2, 2, 1)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')

# Plot 2: Feature Importance
plt.subplot(2, 2, 2)
plt.barh(feature_importance['Feature'], feature_importance['Coefficient'], color='steelblue')
plt.xlabel('Coefficient Magnitude')
plt.title('Top 10 Feature Importance')

# Plot 3: ROC Curve
from sklearn.metrics import roc_curve
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
plt.subplot(2, 2, 3)
plt.plot(fpr, tpr, linewidth=2, label=f'AUC = {roc_auc_score(y_test, y_pred_proba):.3f}')
plt.plot([0, 1], [0, 1], 'k--', linewidth=1)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()

# Plot 4: Prediction distribution
plt.subplot(2, 2, 4)
plt.hist(y_pred_proba[y_test==0], alpha=0.6, label='No Churn', bins=30)
plt.hist(y_pred_proba[y_test==1], alpha=0.6, label='Churn', bins=30)
plt.xlabel('Predicted Probability')
plt.ylabel('Count')
plt.title('Prediction Distribution')
plt.legend()

plt.tight_layout()
plt.savefig('churn_prediction_results.png', dpi=300, bbox_inches='tight')
print("\n✅ Model visualizations saved!")
