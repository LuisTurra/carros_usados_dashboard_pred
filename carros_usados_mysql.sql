SELECT * FROM used_car_listings;

DESCRIBE used_car_listings;

ALTER TABLE used_car_listings 
ADD COLUMN city VARCHAR(100),
ADD COLUMN state VARCHAR(100),
ADD COLUMN country VARCHAR(100);

UPDATE used_car_listings
SET 
    city = TRIM(SUBSTRING_INDEX(location, ',', 1)),
    state = NULLIF(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(location, ',', 2), ',', -1)), ''),
    country = CASE 
                 WHEN location LIKE '%,%,%' 
                     THEN TRIM(SUBSTRING_INDEX(location, ',', -1))
                 WHEN location LIKE '%,%' 
                     THEN TRIM(SUBSTRING_INDEX(location, ',', -1))
                 ELSE NULL
              END;
              
SELECT * FROM used_car_listings;

SELECT DISTINCT make
FROM used_car_listings;
SELECT DISTINCT model
FROM used_car_listings;
SELECT DISTINCT year
FROM used_car_listings;
SELECT DISTINCT trim
FROM used_car_listings;
SELECT DISTINCT body_type
FROM used_car_listings;
SELECT DISTINCT fuel_type
FROM used_car_listings;
SELECT DISTINCT transmission
FROM used_car_listings;
SELECT DISTINCT mileage
FROM used_car_listings;
SELECT DISTINCT `condition`
FROM used_car_listings;
SELECT DISTINCT city
FROM used_car_listings;
SELECT DISTINCT state
FROM used_car_listings;
SELECT DISTINCT country
FROM used_car_listings;
SELECT DISTINCT seller_type
FROM used_car_listings;

SELECT * FROM used_car_listings;
