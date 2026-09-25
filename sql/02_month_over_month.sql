-- Which months have the largest fraud-rate change?
WITH m AS (SELECT month, 100.0*AVG(fraud_bool) rate FROM applications GROUP BY month)
 SELECT month, ROUND(rate,3) fraud_rate_pct,
 ROUND(rate-LAG(rate) OVER (ORDER BY month),3) change_pp
 FROM m ORDER BY month;
