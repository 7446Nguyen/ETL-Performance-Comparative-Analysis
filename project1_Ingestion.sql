-- Give permissions to create and modify tables
GRANT ALL
ON planning 
TO root@localhost;

-- Identify secure location that MySQL will accept data files from
SHOW GRANTS FOR root@localhost;
SHOW VARIABLES LIKE "secure_file_priv";

-- Load raw .csv file into planning table in project1 database.
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/forcast_data.csv' 
INTO TABLE planning 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Verify that data has been loaded
show tables;

select count(*)
from planning;
