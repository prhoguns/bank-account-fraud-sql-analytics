-- What is the fraud gradient for name-email similarity?
WITH b AS (SELECT fraud_bool, NTILE(5) OVER (ORDER BY name_email_similarity) quintile FROM applications)
 SELECT quintile, COUNT(*) applications, SUM(fraud_bool) frauds,
 ROUND(100.0*AVG(fraud_bool),3) fraud_rate_pct FROM b GROUP BY 1 ORDER BY 1;
