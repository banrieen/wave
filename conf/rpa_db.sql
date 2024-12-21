-- 流程作业任务数据结构
-- 适用于 Mariadb，MySQL
CREATE DATABASE IF NOT EXISTS RPA CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

-- Robot 原型构造数据
-- 指定数据库的字符集，则可以在 `CREATE DATABASE` 语句中使用 `CHARACTER SET` 选项。例如，创建一个使用 UTF-8 编码的数据库：
-- Robot 原型构造数据
-- 指定数据库的字符集，则可以在 `CREATE DATABASE` 语句中使用 `CHARACTER SET` 选项。例如，创建一个使用 UTF-8 编码的数据库：
-- CREATE DATABASE IF NOT EXISTS Robot CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
-- drop database RPA; 
-- SHOW CREATE DATABASE Robot;
USE Robot;
drop table task;
CREATE TABLE if not exists task(     -- 自动化作业任务列表
	TaskID  varchar(255)  PRIMARY KEY, 
	TaskName  varchar(255),
	FlowName  varchar(255) ,
    AutoBootup varchar(255) ,        -- 自动拉起开关
    StationModel    varchar(255),    -- 站点型号
    StationID    varchar(255),       -- 站点编号
	SiteArea  varchar(255),          -- 站点所在区域
    CurrentLot varchar(255),         -- 站点上当前批次的编号
    CurrentStep varchar(255),        -- 站点当前作业工步（工序）
    RunMethod varchar(255),
    `TaskStatus`  varchar(255),      -- 作业状态： 运行，完成，异常；
    Priority  INT,
    ExtendedVar  json,               -- 自定义参数, 扩展参数
    `Schedule` varchar(255),         -- 例行执行计划 
    AlarmRule  varchar(255) ,        -- 是否发送告警
	StartTime  DATETIME,
	Endtime  DATETIME,
	OperatorID  varchar(255),
    Note text
);
drop table task_log;
CREATE TABLE if not exists task_log(   -- 自动化作业日志记录
	TaskID  varchar(255)  PRIMARY KEY, 
	TaskName  varchar(255),
    `TaskStatus`  varchar(255),
	FlowName  varchar(255) ,
    StationID    varchar(255),       -- 站点编号
    CurrentLot varchar(255),         -- 站点上当前批次的编号
    CurrentStep varchar(255),        -- 站点当前作业工步（工序）
    WaferID    varchar(255),         -- 当前作业的晶圆片号
    ExeStep    varchar(255),         -- 执行步骤
    ExeRetryTimes   INT,             -- 重试次数
    ExeRsp     json,                 -- 执行结果
	ExeTime  DATETIME,               -- 执行时间
    Image    varchar(1024)           -- 快照图像链接
);
drop table flow;
CREATE TABLE if not exists flow(         -- 流程列表
	FlowID  varchar(255)  PRIMARY KEY,   -- 流程编号
	FlowName  varchar(255) ,             -- 流程名称
    FlowPath  varchar(1024) ,            -- 流程配置或脚本文件路径
    UpdateTime  DATETIME,                -- 更新时间
    ScriptType   varchar(255),           -- 脚本文件类型 .py, .tar
    Scriptpath   varchar(1024),          -- 脚本上传路径
    UseCase    varchar(255),             -- 适用场景
    FlowStatus    varchar(255),          -- 流程开发状态：开发中，验证中，已发布，废弃
	Version  varchar(255),               -- 版本号
    Maintainer varchar(255),             -- 维护人
    StartRule  varchar(255),             -- 触发规则
    RetryInternal INT,                   -- 重试时间间隔
    CheckFirstSlot bool,                 -- 首片检测开关
    AlarmIinfo   varchar(255),           -- 特殊告警信息
    ExampeImage varchar(255),            -- 示例快照图像
    ExtendedVar  json,                   -- 自定义参数, 扩展参数
    Note text                            -- 流程描述，备注信息
);
drop table station;
CREATE TABLE if not exists station(       -- 设备站点列表
	StationID  varchar(255)  PRIMARY KEY,  -- 站点编号 
	StationModel  varchar(255),            -- 站点型号
    StationMAC  varchar(255) ,             -- 站点MAC
	StationIP  varchar(255) ,              -- 站点IP
    StationAccount varchar(255) ,          -- 站点访问账号
    StationStatus varchar(255) ,           -- 站点状态
    TestID        varchar(255) ,           -- 测试机编号
    TestModel     varchar(255) ,           -- 测试机型号
    TestMac       varchar(255) ,           -- 测试机MAC
    TestIP        varchar(255) ,           -- 测试机IP
    TestAccount   varchar(255) ,           -- 测试机账号
    TestPinCardID varchar(255) ,           -- 针卡编号
    StationColorLamp  varchar(255) ,       -- 三色灯状态
    CurrentLot varchar(255),               -- 站点上当前批次的编号
    CurrentStep varchar(255),              -- 站点当前作业工步（工序）
    `TaskStatus`  varchar(255),            -- 作业状态： 运行，完成，异常；
    ExtendedVar  json,                     -- 自定义参数, 扩展参数
	UpTime  DATETIME,                      -- 站点上线时间
	Maintainer  varchar(255),              -- 站点负责人
    Note text
);


-- Debug 
SELECT * FROM Robot.task;

INSERT INTO Robot.task (TaskID, TaskName, FlowName, AutoBootup, StationModel, StationID, SiteArea, CurrentLot, CurrentStep, RunMethod, TaskStatus, Priority, ExtendedVar, `Schedule`, AlarmRule, StartTime, Endtime, OperatorID, Note) 
VALUES (60422626, '作业-154', '流程-8C5', '否', '运行中', 'WX-172', '二楼', '3429-9923-', 'CP6', '上线', '运行中', 100, '[]', '25 23 25 9 5', '调试流程：内部推送记录', '2024-11-17 23:41:03', '2024-11-17 23:59:21', '26C3D5', '验证作业：已经调试完成的自动化作业流程需要安排2~10台站点，小批量上线验证，务必有操作员和验证人员在线监视，观察执行中的异常情况和收集数据。');