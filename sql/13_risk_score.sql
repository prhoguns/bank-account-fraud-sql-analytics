-- How does credit-risk score rank fraud prevalence?
-- Many applications share a score; the hash splits ties the same way every run without looking at the label.
WITH b AS (SELECT fraud_bool, NTILE(10) OVER (ORDER BY credit_risk_score DESC, hash(name_email_similarity, days_since_request, velocity_6h)) decile FROM applications)
 SELECT decile, COUNT(*) applications, SUM(fraud_bool) frauds,
 ROUND(100.0*AVG(fraud_bool),3) fraud_rate_pct FROM b GROUP BY 1 ORDER BY 1;
