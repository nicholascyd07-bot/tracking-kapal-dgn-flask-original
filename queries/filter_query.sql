SELECT * 
FROM nr_playground_table1 
WHERE (%s IS NULL OR time >= %s)
  AND (%s IS NULL OR time <= %s)
  AND (%s IS NULL OR depth >= %s)
  AND (%s IS NULL OR depth <= %s)
  AND (%s IS NULL OR magtype = %s)
  AND (%s IS NULL OR type = %s)
ORDER BY time DESC;