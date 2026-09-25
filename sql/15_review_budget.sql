-- How much fraud can a fixed review budget capture?
WITH ranked AS (SELECT fraud_bool,
 ROW_NUMBER() OVER (ORDER BY credit_risk_score DESC, name_email_similarity ASC) rank_no,
 COUNT(*) OVER () total_count, SUM(fraud_bool) OVER () total_frauds FROM applications)
 SELECT budget review_pct, COUNT(*) FILTER (WHERE rank_no<=total_count*budget/100.0) reviews,
 SUM(fraud_bool) FILTER (WHERE rank_no<=total_count*budget/100.0) frauds_found,
 ROUND(100.0*SUM(fraud_bool) FILTER (WHERE rank_no<=total_count*budget/100.0)/MAX(total_frauds),2) fraud_recall_pct
 FROM ranked CROSS JOIN (VALUES (1),(2),(5),(10),(20),(50),(100)) b(budget)
 GROUP BY budget ORDER BY budget;
