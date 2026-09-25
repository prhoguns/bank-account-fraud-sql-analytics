-- How does fraud rate vary by device operating system?
SELECT device_os, COUNT(*) applications, SUM(fraud_bool) frauds,
 ROUND(100.0*AVG(fraud_bool),3) fraud_rate_pct FROM applications GROUP BY device_os ORDER BY fraud_rate_pct DESC;
