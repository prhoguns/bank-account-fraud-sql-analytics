-- How do transparent review rules compare on precision and recall?
WITH flags AS (SELECT fraud_bool, foreign_request=1 foreign_rule,
 name_email_similarity<0.2 weak_match_rule, device_distinct_emails_8w>=2 reused_device_rule,
 foreign_request=1 OR (name_email_similarity<0.2 AND device_distinct_emails_8w>=2) combined_rule FROM applications),
 unpivoted AS (SELECT fraud_bool, 'foreign request' rule_name, foreign_rule flag FROM flags UNION ALL
 SELECT fraud_bool, 'weak name/email match', weak_match_rule FROM flags UNION ALL
 SELECT fraud_bool, 'reused device', reused_device_rule FROM flags UNION ALL
 SELECT fraud_bool, 'combined', combined_rule FROM flags)
 SELECT rule_name, COUNT(*) FILTER (WHERE flag) reviews,
 SUM(fraud_bool) FILTER (WHERE flag) frauds_found,
 ROUND(100.0*SUM(fraud_bool) FILTER (WHERE flag)/NULLIF(COUNT(*) FILTER (WHERE flag),0),2) precision_pct,
 ROUND(100.0*SUM(fraud_bool) FILTER (WHERE flag)/SUM(fraud_bool),2) recall_pct
 FROM unpivoted GROUP BY 1 ORDER BY recall_pct DESC;
