use db;
DROP TABLE IF EXISTS questions;
CREATE TABLE questions (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(255) NOT NULL,
    session_id INT UNSIGNED NOT NULL,
    position INT(4) UNSIGNED NOT NULL,
    author VARCHAR(100) NOT NULL,
    created_at DATETIME
);
