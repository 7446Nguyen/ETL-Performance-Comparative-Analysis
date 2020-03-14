install.packages(c('skimr','lubridate'))
library(pacman)
p_load('tidyverse','lubridate')

oracle = O_07012019_12312019

#Data Cleaning
#Put PO numbers in correct format, remove timestamp
oracle = oracle %>%
  mutate(`Order Source Reference` = str_sub(oracle$`Order Source Reference`,1,6)) %>%
  mutate(`Request Date` = str_sub(oracle$`Request Date`,end = -6))# get rid of time stamp

oracle$`Request Date` = as.Date(oracle$`Request Date`, format = "%m/%d/%Y")

#Eliminate NA's - Reannan business reason why N/A's need to be removed
oracle2 = oracle %>%  filter(`Ordered Item` != '#N/A') %>% drop_na

skimr::skim(oracle2)

names(oracle2)[7]="eaches_qty"
names(oracle2)[2]="order_source_reference"
names(oracle2)[11]="site_num"
names(oracle2)[10]="request_date"
names(oracle2)[4]="ordered_item"
names(oracle2)[5]="item_desc"
names(oracle2)[6]="line_type"
names(oracle2)[8]="selling_price"
names(oracle2)[9]="extended_price"

#OrderHeader
OrderHeader = oracle2 %>%
  select(order_source_reference, site_num, request_date)
OrderHeader$ohID = seq.int(nrow(OrderHeader))
OrderHeader = OrderHeader %>% select(5,1:4)

#order_line
order_line = oracle2 %>%
  select(`Line`,`Order`,ordered_item,`eaches_qty`,extended_price)

#item table
item = oracle2 %>%
  distinct(ordered_item,item_desc)

#Price Table
#reannan will correct for there to be 400 unique item prices
item_price = ITEM_COST
names(item_price)[1]="ordered_item"
names(item_price)[3]="selling_price"

item_price$priceID = seq.int(nrow(item_price))
item_price = item_price %>% select(4,1,3)
