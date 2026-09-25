-- How do labeled rates and review-rule hit rates vary by employment segment?
SELECT employment_status, COUNT(*) applications, SUM(fraud_bool) frauds,
 ROUND(100.0*AVG(fraud_bool),3) fraud_rate_pct,
 ROUND(100.0*AVG((foreign_request=1 OR name_email_similarity<0.2)::INT),2) rule_hit_pct
 FROM applications GROUP BY 1 ORDER BY applications DESC;
