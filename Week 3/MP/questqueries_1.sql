CREATE DATABASE medical;

USE medical;

SELECT bmi_category, gender, COUNT(gender) as count
FROM medical
GROUP BY bmi_category, gender;

SELECT bmi_category as BMI, round (avg(quality_of_sleep),2) as Quality
FROM medical
WHERE bmi_category= "Normal" or bmi_category= "Overweight" or bmi_category= "Obese"
GROUP BY bmi_category
order by Quality desc;




SELECT age_group, AVG(activity_level) as avg_activity_level
FROM (
    SELECT activity_level, 
        CASE
            WHEN age >= 25 AND age <= 35 THEN '25-35'
            WHEN age > 35 AND age <= 45 THEN '35-45'
            WHEN age > 45 THEN '45+'
            ELSE 'Unknown'
        END AS age_group
    FROM medical
) AS age_group_data
GROUP BY age_group;

