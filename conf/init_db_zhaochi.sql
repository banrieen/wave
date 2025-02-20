-- LED CSV BIN Code table
-- show databases;
CREATE DATABASE if not exists datasets_zhaochi DEFAULT CHARACTER SET 'utf8';
-- Drop database `datasets_zhaochi`;
-- drop table  dut_info;
use datasets_zhaochi;

-- Tabel for dut info
CREATE TABLE if not exists dut_info(
	DeviceID  varchar(255),
	LotID  varchar(255),
	WaferID  varchar(255) PRIMARY KEY,
	ToolID  varchar(255),
	Starttime  DATETIME,
	Endtime  DATETIME,
	OperatorID  varchar(255),
    Specification  varchar(255),
	Scancount  INT,
	Testcount  INT,
	NGcount  INT,
    BinTable varchar(255),
BARCODE varchar(255)
);

-- Table for dut test result with posx，posy, BIN, r1 
CREATE TABLE IF NOT EXISTS dut_list(
TEST INT,
BIN  FLOAT,
PosX FLOAT,
PosY FLOAT,
Channel FLOAT,
Cycle FLOAT,
ESDPASS FLOAT,
ESDSTOP FLOAT,
ESDIR FLOAT,
ESDVF1 FLOAT,
VF1 FLOAT,
VF2 FLOAT,
VF3 FLOAT,
VF4 FLOAT,
VF5 FLOAT,
VFM1 FLOAT,
VFM2 FLOAT,
DVF FLOAT,
VFDVF FLOAT,
VFD FLOAT,
VZ1 FLOAT,
VZ2 FLOAT,
VZ3 FLOAT,
IR1 FLOAT
);

/* dut list other cows
TEST INT,
BIN  FLOAT,
PosX FLOAT,
PosY FLOAT,
Channel FLOAT,
Cycle FLOAT,
ESDPASS FLOAT,
ESDSTOP FLOAT,
ESDIR FLOAT,
ESDVF1 FLOAT,
VF1 FLOAT,
VF2 FLOAT,
VF3 FLOAT,
VF4 FLOAT,
VF5 FLOAT,
VFM1 FLOAT,
VFM2 FLOAT,
DVF FLOAT,
VFDVF FLOAT,
VFD FLOAT,
VZ1 FLOAT,
VZ2 FLOAT,
VZ3 FLOAT,
IR1 FLOAT,
IR2 FLOAT,
IR3 FLOAT,
IR4 FLOAT,
IR5 FLOAT,
IR6 FLOAT,
IR7 FLOAT,
IR8 FLOAT,
IR9 FLOAT,
IR10 FLOAT,
IF1 FLOAT,
IF2 FLOAT,
IF3 FLOAT,
WLD1 FLOAT,
WLP1 FLOAT,
WLC1 FLOAT,
IV1 FLOAT,
PO1 FLOAT,
HW1 FLOAT,
PURITY1 FLOAT,
X1 FLOAT,
Y1 FLOAT,
Z1 FLOAT,
CCT1 FLOAT,
ST1 FLOAT,
INT1 FLOAT,
WLD2 FLOAT,
WLP2 FLOAT,
WLC2 FLOAT,
IV2 FLOAT,
PO2 FLOAT,
HW2 FLOAT,
PURITY2 FLOAT,
X2 FLOAT,
Y2 FLOAT,
Z2 FLOAT,
CCT2 FLOAT,
ST2 FLOAT,
INT2 FLOAT,
WLD3 FLOAT,
WLP3 FLOAT,
WLC3 FLOAT,
IV3 FLOAT,
PO3 FLOAT,
HW3 FLOAT,
PURITY3 FLOAT,
X3 FLOAT,
Y3 FLOAT,
Z3 FLOAT,
CCT3 FLOAT,
ST3 FLOAT,
INT3 FLOAT,
Outside FLOAT,
PartTestDie FLOAT
*/