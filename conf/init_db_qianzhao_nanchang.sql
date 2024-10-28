-- 乾照-南昌 LOP BIN Code table
-- show databases;
CREATE DATABASE if not exists datasets_led_qianzhao_nanchang DEFAULT CHARACTER SET 'utf8';
-- Drop database `datasets_zhaochi`;
-- drop table  dut_info;
use datasets_led_qianzhao_nanchang;

-- Tabel for 每天COW点测站点的LOP的连续变化分布
CREATE TABLE if not exists DataSource1(
STARTTIME  DATETIME,
CREATELOT  varchar(255),
EPICOMPONENTID  varchar(255),
SMP_WLD1_AVG  FLOAT,
STRUCTCODE  varchar(255),
SUBSTRUCTCODE  INT,
COW_LOP1_AVG_K  FLOAT                                              
);

-- Table for 每天COW 点测的所有wafer的（内/中/外圈）
CREATE TABLE IF NOT EXISTS DataSource2(
slotID      INT,
Etch_quan  varchar(255)
);

-- Table for 每周COT站点LOP检测的BIN 统计及其亮度平均值趋势
CREATE TABLE IF NOT EXISTS DataSource3(
点测时间  varchar(255),
圆片片号  varchar(255),
产品      varchar(255),
BINNAME  varchar(255),
`BINNO.`   varchar(255),
中BIN芯粒数 INT,
WLD1BIN INT,
LOP1BIN INT,
VF1BIN   varchar(255)
);

CREATE TABLE IF NOT EXISTS DataSource4(
圆片片号  varchar(255),
来料批次号  varchar(255),
产品  varchar(255),
点测日期  varchar(255),
COT_VF1AVG  FLOAT,
COT_LOP1AVG  FLOAT,
COT_WLD1AVG  FLOAT
);
