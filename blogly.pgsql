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
INSERT INTO users (first_name, last_name, image_url)
    VALUES ('Nia', 'Jax', 'https://th.bing.com/th/id/OIP.UFGeRVYH-RQUeZuyGdZxZgHaGL?pid=ImgDet&rs=1'), ('Jey', 'Uso', 'https://th.bing.com/th/id/R.f5f712fd75c3e092e828951da4181afe?rik=cYQgnsT%2f95ws7Q&pid=ImgRaw&r=0');

INSERT INTO posts (title, content, created_at, user_id)
    VALUES ('This is it.', 'the body content', '2022-04-15 18:29:20.029542', 1), ('#2 This is it.', 'the body content', '2022-04-13 18:29:20.029542', 1), ('#3 This is it.', 'the body content', '2022-04-14 18:29:20.029542', 2)
