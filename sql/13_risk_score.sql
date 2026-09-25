-- How does credit-risk score rank fraud prevalence?
WITH b AS (SELECT fraud_bool, NTILE(10) OVER (ORDER BY credit_risk_score DESC) decile FROM applications)
 SELECT decile, COUNT(*) applications, SUM(fraud_bool) frauds,
 ROUND(100.0*AVG(fraud_bool),3) fraud_rate_pct FROM b GROUP BY 1 ORDER BY 1;
