GRANT ALL
ON OrderHeader
TO root@localhost;

GRANT ALL
ON order_line
TO root@localhost;

GRANT ALL
ON item
TO root@localhost;

GRANT ALL
ON itemPrice
TO root@localhost;

SHOW GRANTS FOR root@localhost;
SHOW VARIABLES LIKE "secure_file_priv";

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/OrderHeader.csv' 
INTO TABLE OrderHeader
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/order_line.csv' 
INTO TABLE order_line
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/item_price.csv' 
INTO TABLE itemPrice
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/item.csv' 
INTO TABLE item
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

show tables;

select *
from OrderHeader;

select *
from order_line;

select *
from order_line as ol
inner join OrderHeader as oh
on oh.po_no = ol.OrderHeader_po_no;