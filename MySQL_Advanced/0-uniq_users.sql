-- Task: Create a tabke named 'users' to store user information.
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
-- The table is designed to store user data with constraints on the 'id' and 'email' fields.
