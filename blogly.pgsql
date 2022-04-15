-- DROP DATABASE IF EXISTS blogly_db;
-- CREATE DATABASE blogly_db;
SELECT
    'CREATE DATABASE blogly_db'
WHERE
    NOT EXISTS (
        SELECT
        FROM
            pg_database
        WHERE
            datname = 'blogly_db') \gexec

\c blogly_db
