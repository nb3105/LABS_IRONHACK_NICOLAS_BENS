USE sakila;

SHOW Tables;

SELECT * FROM actor;

SELECT * FROM film;

SELECT * FROM customer;

SELECT title
FROM film;

SELECT name as language
FROM language;

SELECT DISTINCT release_year
FROM film;

SELECT COUNT(store_id);

SELECT COUNT(staff_id)
FROM staff;

SELECT COUNT(inventory_id), COUNT(return_date)
FROM rental;

SELECT DISTINCT COUNT(actor_id)
FROM film_actor;

SELECT length, title
FROM film
ORDER BY length DESC
LIMIT 10;

SELECT *
FROM actor
WHERE first_name = "SCARLETT";







