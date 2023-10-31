CREATE DATABASE library;

use library;


CREATE TABLE books (
ISBN INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
book_name VARCHAR(40));

CREATE TABLE users (
user_id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(40),
last_name VARCHAR(40));


INSERT INTO users (user_id, first_name, last_name)
VALUES (1, "Aleks", "Boski"),
		(2, "Jaime", "Rollon");
        
ALTER TABLE books
ADD COLUMN user_id INT;

INSERT INTO books (ISBN, book_name, user_id)
VALUES (1234, "Of Mice and Men", 1),
		(5678, "Meditations", 2);
        
SELECT * FROM users;

ALTER TABLE books
ADD FOREIGN KEY (user_id) REFERENCES users(user_id);