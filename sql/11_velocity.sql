-- How does six-hour application velocity relate to fraud?
WITH b AS (SELECT fraud_bool, NTILE(10) OVER (ORDER BY velocity_6h) decile FROM applications)
 SELECT decile, COUNT(*) applications, SUM(fraud_bool) frauds,
 ROUND(100.0*AVG(fraud_bool),3) fraud_rate_pct FROM b GROUP BY 1 ORDER BY 1;
