SELECT count(FileName) FROM datasets_qianzhao.dut_info;
-- truncate datasets_qianzhao.dut_info;
-- SELECT * FROM datasets_qianzhao.dut_info;
-- truncate datasets_qianzhao.dut_list;
-- SELECT count(FileName) FROM datasets_qianzhao.dut_list; 
Select * from datasets_qianzhao.dut_list  limit 100000; 
-- DELETE FROM datasets_qianzhao.dut_info WHERE `FileName` = 'TMC2306B208311.csv';
SET SQL_SAFE_UPDATES = 0;
DELETE FROM datasets_qianzhao.dut_info WHERE FileName ="TMC2306B208311.csv";
--   and TesterModel = null
DELETE FROM datasets_qianzhao.dut_list where FileName ="TMC2306B208311.csv";