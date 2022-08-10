CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)

SELECT * FROM users WHERE id = id

DELETE * FROM users WHERE id = id

UPDATE users SET username = %s, email, = %s, password = %s WHERE id = %s