-- LED CSV BIN Code table
-- show databases;
CREATE DATABASE if not exists datasets_led_qianzhao DEFAULT CHARACTER SET 'utf8';
-- Drop database `datasets_zhaochi`;
-- drop table  dut_info;
use datasets_led_qianzhao;

-- Tabel for dut info
CREATE TABLE if not exists dut_info(
FileName  varchar(255), 
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
IR1 FLOAT,
PosX FLOAT,
PosY FLOAT,
FileName  varchar(255),
Operator  varchar(255),
TesterModel  varchar(255)
);

CREATE TABLE IF NOT EXISTS dut_summary(
STARTTESTT varchar(255),
COMPONENTID varchar(255),
外延机台 varchar(255),
PROBER_RECORD_SID varchar(255),
WAFERQTY varchar(255),
ELE_YIELD varchar(255),
OPERATORID varchar(255),
STARTTESTTIME varchar(255),
ENDTESTTIME varchar(255),
MACHINENO varchar(255),
UPDATETIME varchar(255),
VF1_MIN   FLOAT,
VF1_AVG   FLOAT,
VF1_MAX   FLOAT,
VF1_STD   FLOAT,
VF1_YIELD   FLOAT,
VF2_MIN   FLOAT,
VF2_AVG   FLOAT,
VF2_MAX   FLOAT,
VF2_STD   FLOAT,
VF2_YIELD   FLOAT,
VF3_MIN   FLOAT,
VF3_AVG   FLOAT,
VF3_MAX   FLOAT,
VF3_STD   FLOAT,
VF3_YIELD   FLOAT,
VF4_MIN   FLOAT,
VF4_AVG   FLOAT,
VF4_MAX   FLOAT,
VF4_STD   FLOAT,
VF4_YIELD   FLOAT,
VF5_MIN   FLOAT,
VF5_AVG   FLOAT,
VF5_MAX   FLOAT,
VF5_STD   FLOAT,
VF5_YIELD   FLOAT,
VFM2_MIN   FLOAT,
VFM2_AVG   FLOAT,
VFM2_MAX   FLOAT,
VFM2_STD   FLOAT,
VFM2_YIELD   FLOAT,
DVF_MIN   FLOAT,
DVF_AVG   FLOAT,
DVF_MAX   FLOAT,
DVF_STD   FLOAT,
DVF_YIELD   FLOAT,
VF_MIN   FLOAT,
VF_AVG   FLOAT,
VF_MAX   FLOAT,
VF_STD   FLOAT,
VF_YIELD   FLOAT,
VFD_MIN   FLOAT,
VFD_MAX   FLOAT,
VFD_STD   FLOAT,
VFD_YIELD   FLOAT,
VZ1_MIN   FLOAT,
VZ1_AVG   FLOAT,
VZ1_MAX   FLOAT,
VZ1_STD   FLOAT,
VZ1_YIELD   FLOAT,
IR1_MIN   FLOAT,
IR1_AVG   FLOAT,
IR1_MAX   FLOAT,
IR1_STD   FLOAT,
IR1_YIELD   FLOAT,
IR2_MIN   FLOAT,
IR2_AVG   FLOAT,
IR2_MAX   FLOAT,
IR2_STD   FLOAT,
IR2_YIELD   FLOAT,
LOP1_MIN   FLOAT,
LOP1_AVG   FLOAT,
LOP1_MAX   FLOAT,
LOP1_STD   FLOAT,
LOP1_YIELD   FLOAT,
LOP2_MIN   FLOAT,
LOP2_AVG   FLOAT,
LOP2_MAX   FLOAT,
LOP2_STD   FLOAT,
LOP2_YIELD   FLOAT,
LOP3_MIN   FLOAT,
LOP3_AVG   FLOAT,
LOP3_MAX   FLOAT,
LOP3_STD   FLOAT,
LOP3_YIELD   FLOAT,
LOP4_MIN   FLOAT,
LOP4_AVG   FLOAT,
LOP4_MAX   FLOAT,
LOP4_STD   FLOAT,
LOP4_YIELD   FLOAT,
LOP5_MIN   FLOAT,
LOP5_AVG   FLOAT,
LOP5_MAX   FLOAT,
LOP5_STD   FLOAT,
LOP5_YIELD   FLOAT,
WLP1_MIN   FLOAT,
WLP1_AVG   FLOAT,
WLP1_MAX   FLOAT,
WLP1_STD   FLOAT,
WLP1_YIELD   FLOAT,
WLD1_MIN   FLOAT,
WLD1_AVG   FLOAT,
WLD1_MAX   FLOAT,
WLD1_STD   FLOAT,
WLD1_YIELD   FLOAT,
WLC1_MIN   FLOAT,
WLC1_AVG   FLOAT,
WLC1_MAX   FLOAT,
WLC1_STD   FLOAT,
WLC1_YIELD   FLOAT,
HW1_MIN   FLOAT,
HW1_AVG   FLOAT,
HW1_MAX   FLOAT,
HW1_STD   FLOAT,
HW1_YIELD   FLOAT,
PURITY1_MIN   FLOAT,
PURITY1_AVG   FLOAT,
PURITY1_MAX   FLOAT,
PURITY1_STD   FLOAT,
PURITY1_YIELD   FLOAT,
WLP2_MIN   FLOAT,
WLP2_AVG   FLOAT,
WLP2_MAX   FLOAT,
WLP2_STD   FLOAT,
WLP2_YIELD   FLOAT,
WLD2_MIN   FLOAT,
WLD2_AVG   FLOAT,
WLD2_MAX   FLOAT,
WLD2_STD   FLOAT,
WLD2_YIELD   FLOAT,
ESD_HBM_YIELD   FLOAT,
ESD_MM_YIELD   FLOAT
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