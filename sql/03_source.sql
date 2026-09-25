-- Which application source has the higher labeled fraud rate?
SELECT source, COUNT(*) applications, SUM(fraud_bool) frauds,
 ROUND(100.0*AVG(fraud_bool),3) fraud_rate_pct FROM applications GROUP BY source ORDER BY fraud_rate_pct DESC;
