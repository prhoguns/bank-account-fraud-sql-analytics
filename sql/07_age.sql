-- How does fraud rate vary by age band?
SELECT customer_age age_band, COUNT(*) applications, SUM(fraud_bool) frauds,
 ROUND(100.0*AVG(fraud_bool),3) fraud_rate_pct FROM applications GROUP BY 1 ORDER BY 1;
