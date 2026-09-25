-- How do volume and labeled fraud rate change by month?
SELECT month, COUNT(*) applications, SUM(fraud_bool) frauds,
 ROUND(100.0*AVG(fraud_bool),3) fraud_rate_pct
 FROM applications GROUP BY month ORDER BY month;
