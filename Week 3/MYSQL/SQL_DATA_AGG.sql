USE sakila;

SELECT length, title as max_length
from film
ORDER BY length DESC
LIMIT 1;

SELECT length, title as min_length
from film
ORDER BY length ASC
LIMIT 1;

SELECT ROUND(AVG(length))
FROM film
Order BY length
LIMIT 1