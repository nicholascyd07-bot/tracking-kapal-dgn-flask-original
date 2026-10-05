SELECT *
FROM nr_playground_table1
WHERE (%s::timestamp IS NULL OR time >= %s::timestamp)
  AND (%s::timestamp IS NULL OR time <= %s::timestamp)
  AND (%s::numeric IS NULL OR depth >= %s::numeric)
  AND (%s::numeric IS NULL OR depth <= %s::numeric)
  AND (%s = 0 OR magtype = ANY(%s))
  AND (%s IS NULL OR type = %s)
ORDER BY time DESC;