GRANT ALL
ON planning 
TO root@localhost;

SHOW GRANTS FOR root@localhost;
SHOW VARIABLES LIKE "secure_file_priv";

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/forcast_data.csv' 
INTO TABLE planning 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

show tables;

select count(*)
from planning;