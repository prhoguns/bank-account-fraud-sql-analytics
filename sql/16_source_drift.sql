-- How does fraud rate drift over time by application source?
SELECT month, source, COUNT(*) applications, SUM(fraud_bool) frauds,
 ROUND(100.0*AVG(fraud_bool),3) fraud_rate_pct
 FROM applications GROUP BY 1,2 ORDER BY 1,2;
