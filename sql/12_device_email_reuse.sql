-- Does reuse of a device across emails raise fraud rates?
SELECT device_distinct_emails_8w email_count_8w, COUNT(*) applications,
 SUM(fraud_bool) frauds, ROUND(100.0*AVG(fraud_bool),3) fraud_rate_pct
 FROM applications GROUP BY 1 ORDER BY 1;
