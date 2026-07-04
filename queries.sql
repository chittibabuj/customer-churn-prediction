 Q1: Churn distribution
SELECT 
  Churn,
  COUNT(*) as customer_count,
  ROUND(COUNT() * 100.0 / (SELECT COUNT() FROM churn), 2) as percentage
FROM churn
GROUP BY Churn;

-- Q2: Churn by contract type
SELECT 
  Contract,
  COUNT(*) as total,
  SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned,
  ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM churn
GROUP BY Contract;

-- Q3: Churn by tenure
SELECT 
  CASE 
    WHEN tenure < 12 THEN '0-12 months'
    WHEN tenure < 24 THEN '12-24 months'
    WHEN tenure < 36 THEN '24-36 months'
    ELSE '36+ months'
  END as tenure_group,
  COUNT(*) as customers,
  SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned_count,
  ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM churn
GROUP BY tenure_group;

-- Q4: Monthly charges analysis
SELECT 
  Churn,
  ROUND(AVG(MonthlyCharges), 2) as avg_monthly_charges,
  ROUND(MAX(MonthlyCharges), 2) as max_charges,
  ROUND(MIN(MonthlyCharges), 2) as min_charges
FROM churn
GROUP BY Churn;

-- Q5: Internet service type impact
SELECT 
  InternetServiceType,
  COUNT(*) as total_customers,
  SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned,
  ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate
FROM churn
GROUP BY InternetServiceType;

-- Q6: High-risk customers
SELECT 
  CustomerID,
  tenure,
  MonthlyCharges,
  Contract,
  InternetServiceType,
  Churn
FROM churn
WHERE MonthlyCharges > 80 AND tenure < 12 AND Churn = 'Yes'
ORDER BY MonthlyCharges DESC;

-- Q7: Customer lifetime value
SELECT 
  Churn,
  ROUND(AVG(tenure * MonthlyCharges), 2) as avg_lifetime_value,
  COUNT(*) as customer_count
FROM churn
GROUP BY Churn;

-- Q8: Multiple services impact
SELECT 
  CASE 
    WHEN (PhoneService = 'Yes')::int + (InternetService = 'Yes')::int + (OnlineSecurity = 'Yes')::int >= 2 THEN 'Multiple Services'
    ELSE 'Single/No Service'
  END as service_category,
  COUNT(*) as customers,
  SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as churned
FROM churn
GROUP BY service_category;
