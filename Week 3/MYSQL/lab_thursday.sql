use sakila;

#VIEW
create view customer_rental_info as
select customer_id,first_name, email, count(rental_id) as rental_counts
from customer 
inner join rental
using (customer_id)
group by customer_id;


#Temporary table

CREATE TEMPORARY TABLE total_paid AS
select customer_id,first_name, last_name, sum(amount) as total_amount
from customer 
inner join rental
using (customer_id)
inner join payment
using (customer_id)
group by customer_id;


#Common Table Expressions (CTE)

with cte as (
select total_paid.first_name, email, total_amount, rental counts
from total_paid
inner join customer_rental_info
using (customer_id))

select first_name, email, total_amount, rental_counts, total_amount/rental_counts as average_amount_spent
from cte;


cte2 as (
select customer_id,first_name, email, count(rental_id) as rental_counts
from customer 
inner join rental
using (customer_id)
group by customer_id)

select *
FROM cte c 
inner JOIN cte2 c2 ON c.customer_id = c2.customer_id;