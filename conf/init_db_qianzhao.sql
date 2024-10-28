-- LED CSV BIN Code table
-- show databases;
CREATE DATABASE if not exists datasets_led_qianzhao DEFAULT CHARACTER SET 'utf8';
-- Drop database `datasets_zhaochi`;
-- drop table  dut_info;
use datasets_led_qianzhao;

-- Tabel for dut info
CREATE TABLE if not exists dut_info(
FileName  varchar(255), 
TestTime   DATETIME,
TestStartTime  DATETIME,
TestEndTime  DATETIME,
TesterModel  varchar(255),                                                                                                    
TesterNumber  varchar(255),                                               
Specification  varchar(255),                                                                                                                                                        
TotalTested  INT,                                                
Operator  varchar(255)                                               
);

-- Table for dut test result with posx，posy, BIN, r1 
CREATE TABLE IF NOT EXISTS dut_list(
TEST INT,
BIN varchar(255),
VF1 FLOAT,
IR FLOAT,
IR1 FLOAT,
PosX FLOAT,
PosY FLOAT
);
-- CREATE TABLE IF NOT EXISTS dut_list_full(
-- TEST INT,
-- BIN INT,
-- CONTA FLOAT,
-- CONTC FLOAT,
-- POLAR FLOAT,
-- VF1 FLOAT,
-- VF2 FLOAT,
-- VF3 FLOAT,
-- VF4 FLOAT,
-- VFM1 FLOAT,
-- VFM2 FLOAT,
-- DVF FLOAT,
-- VF FLOAT,
-- VFD FLOAT,
-- VZ1 FLOAT,
-- VZ2 FLOAT,
-- IR FLOAT,
-- LOP1 FLOAT,
-- LOP2 FLOAT,
-- LOP3 FLOAT,
-- WLP1 FLOAT,
-- WLD1 FLOAT,
-- WLC1 FLOAT,
-- HW1 FLOAT,
-- PURITY1 FLOAT,
-- X1 FLOAT,
-- Y1 FLOAT,
-- Z1 FLOAT,
-- ST1 FLOAT,
-- `INT1` FLOAT,
-- WLP2 FLOAT,
-- WLD2 FLOAT,
-- WLC2 FLOAT,
-- HW2 FLOAT,
-- PURITY2 FLOAT,
-- X2 FLOAT,
-- Y2 FLOAT,
-- Z2 FLOAT,
-- CCT2 FLOAT,
-- ST2 FLOAT,
-- `INT2` FLOAT,
-- WLP3 FLOAT,
-- WLD3 FLOAT,
-- WLC3 FLOAT,
-- HW3 FLOAT,
-- PURITY3 FLOAT,
-- X3 FLOAT,
-- Y3 FLOAT,
-- Z3 FLOAT,
-- CCT3 FLOAT,
-- Result FLOAT,
-- ESDR FLOAT,
-- PosX FLOAT,
-- PosY FLOAT,
-- IR2 FLOAT,
-- CHAN INT
-- );