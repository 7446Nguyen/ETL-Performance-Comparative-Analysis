create schema project1;

-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema project1
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema project1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `project1` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
USE `project1` ;

-- -----------------------------------------------------
-- Table `project1`.`item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `project1`.`item` (
  `orderedItem` VARCHAR(30) NOT NULL,
  `item_desc` VARCHAR(45) NULL,
  `selling_price` DECIMAL(5,2) NULL,
  PRIMARY KEY (`orderedItem`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `project1`.`order_header`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `project1`.`order_header` (
  `POnum` VARCHAR(15) NOT NULL,
  `site_num` INT NULL,
  `request_date` DATE NULL,
  PRIMARY KEY (`POnum`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `project1`.`order_line`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `project1`.`order_line` (
  `Line` INT NOT NULL,
  `order` INT NULL,
  `eaches_qty` INT NULL,
  `orderedItem` VARCHAR(30) NOT NULL,
  `POnum` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`Line`),
  INDEX `fk_order_line_item1_idx` (`orderedItem` ASC),
  INDEX `fk_order_line_order_header1_idx` (`POnum` ASC),
  CONSTRAINT `fk_order_line_item1`
    FOREIGN KEY (`orderedItem`)
    REFERENCES `project1`.`item` (`orderedItem`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_line_order_header1`
    FOREIGN KEY (`POnum`)
    REFERENCES `project1`.`order_header` (`POnum`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
