SELECT title, inventory_id, inventory.store_id
FROM film
INNER JOIN inventory
ON film.film_id = inventory.film_id
INNER JOIN store
ON inventory.store_id = store.store_id;

SELECT title, name
FROM film
INNER JOIN film_category
ON film.film_id = film_category.film_id
INNER JOIN category
ON category.category_id = film_category.film_id;

#Retrieve each category and the number of films present
SELECT COUNT(film_id), name
FROM film_category
INNER JOIN category
ON category.category_id = film_category.category_id
GROUP BY name;

