# Customer Churn Prediction

Predictive machine learning model to identify customers at risk of leaving.

## Project Overview

- *Objective:* Predict which telecom customers will churn
- *Dataset:* Telco Customer Churn (7,043 customers, 21 features)
- *Target:* Binary classification (Churn = Yes/No)
- *Methods:* SQL analysis + Logistic Regression

## Key Findings

- *Overall Churn Rate:* ~27%
- *Contract Impact:* Month-to-month contracts have 42% churn vs 11% for 2-year
- *Tenure Impact:* <12 months customers have 50% churn rate
- *Top Risk Factors:* Fiber optic internet, high monthly charges, short tenure

## Model Performance

- *Accuracy:* 80%
- *ROC-AUC:* 0.84
- *Precision (Churn):* 65%
- *Recall (Churn):* 52%

## Files

- queries.sql - 8 SQL analysis queries
- churn_analysis.py - Exploratory data analysis
- churn_prediction_model.py - ML model training
- telco_churn.csv - Dataset
- churn_analysis.png - EDA visualizations
- churn_prediction_results.png - Model results

## Technologies

- *SQL:* Data extraction and aggregation
- *Python:* pandas, scikit-learn, matplotlib
- *ML:* Logistic Regression with feature importance

## Results Interpretation

High-risk customers (will likely churn):
- New customers (tenure < 12 months)
- High monthly charges (> $80)
- Fiber optic internet service
- Month-to-month contracts

Recommendations:
- Focus retention efforts on new customers
- Offer incentives for long-term contracts
- Investigate fiber optic service quality

## Author

Jilakara Chittibabu - Computer Science Graduate | AI/ML Portfolio

---

*Advanced Portfolio Project for German Tech Employers*
