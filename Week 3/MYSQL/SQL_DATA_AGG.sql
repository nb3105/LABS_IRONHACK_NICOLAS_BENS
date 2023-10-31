USE sakila;

SELECT length, title as max_length
from film
ORDER BY length DESC
LIMIT 1;

SELECT length, title as min_length
from film
ORDER BY length ASC
LIMIT 1;

SELECT ROUND(AVG(length)) as avg_d
FROM film
Order BY length
LIMIT 1;

SELECT rental_date, return_date
FROM rental
ORDER BY DATEDIFF(rental_date, return_date) DESC;

SELECT
    rental_id, rental_date
FROM rental
LIMIT 20;

SELECT ROUND(AVG(length),2) as avg_d, rating
from film
GROUP BY rating
