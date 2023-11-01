SELECT first_name, last_name
FROM actor
WHERE actor_id = 1;

SELECT first_name, last_name
FROM actor
WHERE actor_id IN (SELECT actor_id
				FROM film_actor
				WHERE film_id = (SELECT film_id
									FROM film
									WHERE title = "Hunchback Impossible"));
                                    
# Retrieve rental id from film_id 1 and hunchback impossible
SELECT rental_id
FROM rental 
WHERE inventory_id IN (SELECT inventory_id
					FROM inventory 
					WHERE film_id = (SELECT film_id
										FROM film
										WHERE title = "Hunchback Impossible"));




