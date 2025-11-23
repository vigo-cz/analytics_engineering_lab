-- Example DuckDB queries and experiments
-- Create a sample table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    email VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO
    users (id, name, email)
VALUES
    (1, 'Alice', 'alice@example.com'),
    (2, 'Bob', 'bob@example.com'),
    (3, 'Charlie', 'charlie@example.com');

-- Query data
SELECT
    *
FROM
    users;

-- Aggregation example
SELECT
    DATE_TRUNC ('day', created_at) as day,
    COUNT(*) as user_count
FROM
    users
GROUP BY
    day
ORDER BY
    day;