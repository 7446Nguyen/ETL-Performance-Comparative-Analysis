-- drop schema project1;
create schema project1;
use project1;

-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema project1
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table `OrderHeader`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OrderHeader` (
  `po_no` VARCHAR(15) NOT NULL,
  `site_num` INT NULL,
  `request_date` DATE NULL,
  PRIMARY KEY (`po_no`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `itemPrice`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `itemPrice` (
  `priceID` VARCHAR(45) NOT NULL,
  `selling_price` VARCHAR(45) NULL,
  PRIMARY KEY (`priceID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `item` (
  `ordered_item` VARCHAR(30) NOT NULL,
  `item_desc` VARCHAR(45) NULL,
  `itemPrice_priceID` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ordered_item`),
  INDEX `fk_item_itemPrice1_idx` (`itemPrice_priceID` ASC) VISIBLE,
  CONSTRAINT `fk_item_itemPrice1`
    FOREIGN KEY (`itemPrice_priceID`)
    REFERENCES `itemPrice` (`priceID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `order_line`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `order_line` (
  `Line` INT NOT NULL,
  `order` INT NULL,
  `eaches_qty` INT NULL,
  `extended_price` INT NULL,
  `OrderHeader_po_no` VARCHAR(15) NOT NULL,
  `item_ordered_item` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`Line`),
  INDEX `fk_order_line_OrderHeader1_idx` (`OrderHeader_po_no` ASC) VISIBLE,
  INDEX `fk_order_line_item1_idx` (`item_ordered_item` ASC) VISIBLE,
  CONSTRAINT `fk_order_line_OrderHeader1`
    FOREIGN KEY (`OrderHeader_po_no`)
    REFERENCES `OrderHeader` (`po_no`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_line_item1`
    FOREIGN KEY (`item_ordered_item`)
    REFERENCES `item` (`ordered_item`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
