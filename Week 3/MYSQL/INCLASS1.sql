USE bank;

SELECT * FROM account;

SELECT frequency, date
FROM account;

SELECT DISTINCT frequency
from account;

SELECT AVG(amount) AS avg_amount
FROM loan;

SELECT account_id, amount
FROM loan
ORDER BY amount DESC;

SELECT account_id, SUM(amount)
FROM loan
GROUP BY account_id;

SELECT COUNT(client_id) AS number_of_client_district, district_id 
FROM client
GROUP BY district_id
ORDER BY number_of_client_district DESC;

SELECT account_id, status, AVG(amount) AS avg_amount
FROM loan
GROUP BY account_id, status;

SELECT SUM(card_id), type
FROM card
GROUP BY type
ORDER BY type ASC;

SELECT SUM(client_id), district_id
FROM client
WHERE district_id = 1;

SELECT amount, loan_id
FROM loan
WHERE amount > 100000
	AND (status in ("A", "B"));
    
    

SELECT AVG(amount) as avg_amount, account_id
FROM loan
WHERE amount BETWEEN 50000 AND 250000
	AND status = "A"
GROUP BY account_id
HAVING avg_amount > 100000;

SELECT loan_id, amount,
CASE
	WHEN amount > 100000 THEN "HIGH"
    WHEN amount >= 50000 and amount <= 100000 THEN "MEDIMUM"
    ELSE "LOW"
END AS tier
FROM loan;

SELECT DISTINCT frequency
FROM account
WHERE frequency LIKE "";