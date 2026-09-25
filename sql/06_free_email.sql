-- Is a free email domain associated with a higher fraud rate?
SELECT email_is_free, COUNT(*) applications, SUM(fraud_bool) frauds,
 ROUND(100.0*AVG(fraud_bool),3) fraud_rate_pct FROM applications GROUP BY 1 ORDER BY 1;
