-- How often do sentinel values appear in selected fields?
SELECT 'previous address months = -1' field, COUNT(*) FILTER (WHERE prev_address_months_count=-1) count_rows,
 ROUND(100.0*AVG((prev_address_months_count=-1)::INT),2) share_pct FROM applications
 UNION ALL SELECT 'bank months = -1', COUNT(*) FILTER (WHERE bank_months_count=-1),
 ROUND(100.0*AVG((bank_months_count=-1)::INT),2) FROM applications
 UNION ALL SELECT 'session length = -1', COUNT(*) FILTER (WHERE session_length_in_minutes=-1),
 ROUND(100.0*AVG((session_length_in_minutes=-1)::INT),2) FROM applications;
