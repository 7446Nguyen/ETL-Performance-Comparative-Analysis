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
-- Table `planning`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `planning` (
  `planning_num` INT NOT NULL,
  `warehouse` INT NULL,
  `site_no` INT NULL,
  `po_no` INT NULL,
  `mfg_cd` VARCHAR(15) NULL,
  `description` VARCHAR(30) NULL,
  `eaches_qty` INT NULL,
  `date` INT NULL,
  PRIMARY KEY (`planning_num`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
commit;