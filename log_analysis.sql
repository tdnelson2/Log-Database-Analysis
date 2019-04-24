\c news;

-- Question 1
CREATE VIEW popular_articles AS
  SELECT
    articles.author AS author_id,
    articles.title AS title,
    top_paths.total AS total
  FROM
    articles,
    (
      SELECT path, count(path) as total
      FROM log
      WHERE
        status = '200 OK'
      AND
        path LIKE '/article/%'
      GROUP BY path
      ORDER BY total DESC
    )
      AS top_paths
    WHERE
      CONCAT('/article/', articles.slug) = top_paths.path
      ORDER BY top_paths.total DESC;

-- Question 2
CREATE VIEW popular_authors AS
  SELECT
    authors.id,
    authors.name,
    SUM(popular_articles.total) AS total
  FROM
    popular_articles,
    authors
  WHERE
    popular_articles.author_id = authors.id
  GROUP BY
    authors.id;

-- Question 3
CREATE VIEW errors_by_days AS
    SELECT
      success_days.day,
      CAST(fail_days.count AS DECIMAL) / success_days.count AS error_rate,
      fail_days.count AS errors,
      success_days.count AS successes
    FROM
      (
        SELECT
          DATE_TRUNC('day', time) as day,
          COUNT(*)
        FROM log WHERE status = '200 OK'
        GROUP BY day
      )
      AS success_days
    LEFT JOIN
      (
        SELECT
          DATE_TRUNC('day', time) as day,
          COUNT(*)
        FROM log WHERE status != '200 OK'
        GROUP BY day
      )
      AS fail_days
    ON
      success_days.day = fail_days.day
    ORDER BY
      error_rate DESC;
