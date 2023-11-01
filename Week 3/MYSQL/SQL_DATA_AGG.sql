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

SELECT rental_date,
CASE
	WHEN DATE_FORMAT(rental_date, "%W") = "Sunday" or "Saturday" THEN "Weekend"
    ELSE "Workday"
    END as DAY_TYPE;
    

SELECT ROUND(AVG(length),2) as avg_d, rating
from film
GROUP BY rating;

SELECT FLOOR(AVG(length) / 60), "hours", ROUND(AVG(length) % 60), "minutes" AS average_duration
FROM film;


SELECT COUNT(film_id) AS total_rated
FROM film
GROUP BY rating
ORDER BY total_rated DESC;

SELECT rating, ROUND(AVG(length),2) AS mean_duration
FROM film
GROUP BY rating
ORDER BY mean_duration DESC;

SELECT rating, ROUND(AVG(length), 2) AS mean_duration
FROM film
GROUP BY rating
HAVING mean_duration > 120;

