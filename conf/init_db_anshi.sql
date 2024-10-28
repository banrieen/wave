-- LED CSV BIN Code table
-- show databases;
CREATE DATABASE if not exists datasets_led_anshi DEFAULT CHARACTER SET 'utf8';
-- Drop database `datasets_zhaochi`;
-- drop table  dut_info;
use datasets_led_anshi;

-- Tabel for dut info
CREATE TABLE if not exists txt_map_info(
`Format Version`  varchar(255), 
`Device Name`  varchar(255), 
`Lot Number`  varchar(255), 
`Vendor Lot Id`  varchar(255), 
`Wafer Number`    INT, 
`Origin Loc`  varchar(255), 
`Wafer Flat`  varchar(255), 
`Column Count`  INT,
`Row Count`  INT,
`Null Bin`  varchar(255),
`Gross Die`  INT,
`Pass Die`  INT,
BinInformation_PASS varchar(255),  -- 1, 482, PASS
BinInformation_FAIL varchar(255)  -- 0, 6, FAIL                                       
);

-- Table for dut test result with posx，posy, BIN, r1 
CREATE TABLE IF NOT EXISTS txt_map_list(
`Device Name` varchar(255),  -- MMKC550F00W0
`Lot Number` varchar(255),  --  E74900B
`Vendor Lot Id` varchar(255),  --  CMD ERROR
`Wafer Number` varchar(255),  --  04
bin_code INT,
posX INT,
posY INT
);

CREATE TABLE IF NOT EXISTS xml_map_info(
WAFER_OCR_ID  varchar(255),
WAFER_BATCH_ID  varchar(255),
WAFER  INT,
PRODUCT   varchar(255),
WAFER_UNIT  varchar(255),
WAFER_SIZE  INT,
XSTEP   float4,
YSTEP   float4,
FLAT_LOCATION   int,
PRQUAD  int,
COQUAD  int,
START_DATE_TIME   datetime,
`DATE`   DATE, 
`TIME`   time,
END_DATE_TIME   datetime,
XOFFSET   float,
YOFFSET   FLOAT,
COLUMN_COUNT  int,
ROW_COUNT   INT
);

CREATE TABLE IF NOT EXISTS xml_map_bincode(
FAIL  varchar(255),
BIN1  INT,
SIMPLE  varchar(255),
PARSET_EM_OVERFLOW   varchar(255),
BIN32  char,
BIN40  char,
BIN42  char,
BIN44  char,
REF_DIE  char,
OPTIREJ  char,
EDGE  char,
SKIPDIE  char,
ELEC__FAIL  char,
NSX_FINAL___TOOL  char,
NSX_FINAL___SPR  char,
NSX_FINAL___SPR_POST_PROCESSING  char,
ULPY  char,
MANUELLE_NACHMARKIERUNG_IN_TDS  char,
FAIL_IN_TEMPLATE  char,
OUTSIDE  char
);


CREATE TABLE IF NOT EXISTS xml_map_list(
bin_code INT,
posX INT,
posY INT
);

CREATE TABLE IF NOT EXISTS E142_map_info(
LayoutId  varchar(255),  -- 'Map', 
DefaultUnits  varchar(255),  -- 'mm', 
TopLevel   varchar(255), -- 'true'
wafer_Dimension_X   int,   -- ="1" 
wafer_Dimension_Y   int,   -- ="1" 
wafer_DeviceSize_X  float,   -- ="150" 
wafer_DeviceSize_Y  float,   -- ="150"/
die_Dimension_X   int,  -- ="474" 
die_Dimension_Y   int,  -- ="406"
die_DeviceSize_X  float,  -- ="0.32" 
die_DeviceSize_Y  float,  -- ="0.32"
StepSize_X    float,  -- ="0.32" 
StepSize_Y    float,  -- ="0.32"
ProductId    varchar(255),
LotId       varchar(255),   -- >WKK020</LotId>
StartDate   datetime,  -- >2022-06-09T08:52:24+08:00
FinishDate   datetime,    -- >2022-06-09T08:52:24+08:00
SubstrateId    varchar(255),  -- ="WKK02W01-C6"
BinType        varchar(255),     -- ="HexaDecimal" 
NullBin         char(255),    -- ="FF"
Orientation int, 
OriginLocation varchar(255), 
AxisDirection varchar(255), 
OriginX int,
OriginY int
);


CREATE TABLE IF NOT EXISTS E142_map_bintable(
SubstrateId varchar(255),      -- ="WLJ2LW01-B6_E1"
BinCode varchar(255),
BinDescription  varchar(255),
BinQuality  varchar(255),
BinCount  INT, 
Pick  varchar(255)
);

CREATE TABLE IF NOT EXISTS E142_map_list(
SubstrateId varchar(255),      -- ="WLJ2LW01-B6_E1"
bin_code varchar(255),
posX INT,
posY INT
);