#!.venv/bin/python
"""生成任务列表
支持 rstful API
数据源管理
数据加载
数据生成
导出到 csv
"""

import random
import pdb

## 查询数据
# import polars as pl
# uri : "mysql://thomas:thomas@192.168.56.113:3306/rpa_vt"
# query : "SELECT * FROM rpa_vt.flow_target_record;"

# pl.read_database_uri(query:query, uri:uri)
# print(pl)
import concurrent.futures
import polars as pl
import datetime
import json
from mysqlSync import mysql_sync

def get_conf(conf_path="conf/rpa_datatable.toml"):
    import toml
    # 读取配置文件
    with open(conf_path, 'r') as f:
        config = toml.load(f)
        return config

def gen_batch_row(func_batch, batch=1000):
    # 批量生成数据 df
    with concurrent.futures.ThreadPoolExecutor(max_workers=(batch/10)) as executor:
        futures = [executor.submit(func_batch) for _ in range(batch)]
    results = [f.result() for f in futures]
    df = pl.DataFrame(results)
    return df

def export_csv(gen_data_df, csf_path="output.csv"):
    # 导出数据 df 到本地 csv 表格
    gen_data_df.write_csv("output.csv",include_header=True,separator=",")

def write_mysql(gen_data_df,table_name,conf,):
    # Init mysql connection
    my_client = mysql_sync() 
    my_client.conn(conf["mariadb"])
    data_schema = ', '.join(conf[table_name].keys())
    insert_sql = "INSERT INTO %s (%s) VALUES (%s);" % (table_name, data_schema, ', '.join(['%s'] * len(gen_data_df.columns)))
    data_tuples = [tuple(row) for row in gen_data_df.rows()]
    # breakpoint()
    my_client.execute_many(insert_sql, gen_data_df.rows())
    my_client.cnx.commit()
    pass

def random_cron():
    # 构造随机 cron 计划表达式
    minute = random.randint(0, 59)
    hour = random.randint(0, 23)
    day_of_month = random.randint(1, 31)
    month = random.randint(1, 12)
    day_of_week = random.randint(0, 6)
    return f"{minute} {hour} {day_of_month} {month} {day_of_week}"

def random_datetime(start_time=None,time_scope=30):
    # 构造一定时长内的随机时间
    now = start_time if start_time else datetime.datetime.now()
    start_time = now - datetime.timedelta(minutes=time_scope)
    t = start_time + datetime.timedelta(
        seconds=random.randint(0, 59),
        minutes=random.randint(0, 29))
    if (t > now) and (start_time==None):
        return "None"                                        ## 如果是生成启动时间，不设置start_time, 生成时间不宜晚于当前
    elif(t < now) and (start_time==None):
        return "None"                                        ## 如果是生成完成时间，设置start_time,生成时间不宜早于当前
    else:
        return (t.strftime("%Y-%m-%d %H:%M:%S"))

def gen_task_list():
    # 构造数据
    task_list = {
                "TaskID" : random.randint(10000000, 99999999),
                "TaskName" : "作业-"+str(random.randint(0, 200)),
                "FlowName" : "流程-"+''.join(random.sample('0123456789ABCDEF', 3)),
                "AutoBootup" : random.choice(["是","否"]),
                "StationModel" : random.choice(["运行中","空闲","停机","故障",]),
                "StationID" : "WX-"+str(random.randint(0, 400)),
                "SiteArea" :  random.choice(["二楼","三楼"]),
                "CurrentLot" : ''.join(random.sample('0123456789ABCDEF', 4)) + "-" + str(random.randint(1000, 9999)) + "-",
                "CurrentStep" : random.choice(["CP1","CP2","CP3","CP4","CP5","CP6",]),
                "RunMethod" : random.choice(["调试","验证中","上线"]),
                "TaskStatus" :  random.choice(["运行中","已完成","已下线","故障",]),
                "Priority" : 100,
                "ExtendedVar" : json.dumps([]),    ## Json dump as string
                "Schedule" : random_cron(),
                "AlarmRule" : random.choice(["验证流程：推送小组工作群","已发布上线：推送生产工作群","调试流程：内部推送记录",]),
                "StartTime" : random_datetime(time_scope=45),
                "Endtime" : random_datetime(datetime.datetime.now(),time_scope=15),
                "OperatorID" : ''.join(random.sample('0123456789ABCDEF', 6)),
                "Note" : random.choice(["调试作业：请与产线主管，QA协调借机，工程片，配套测试仪和针卡，在规定的时间内完成调试排查。",
                          "验证作业：已经调试完成的自动化作业流程需要安排2~10台站点，小批量上线验证，务必有操作员和验证人员在线监视，观察执行中的异常情况和收集数据。",
                          "上线作业: 已经验证通过的自动化作业流程，必须通知生产，质量和工艺主管确认后，与生产负责人协调上线，前期要求留人观察。" ]),
                             }
    return task_list
    

if __name__ == "__main__":
    # gen_task_list()
    csf_path = ""
    batch = 10000
    table_name = "task"   # mariadb
    conf = get_conf(conf_path="conf/rpa_datatable.toml")
    # print(conf[table_name])
    gen_data_df = gen_batch_row(gen_task_list, batch)
    # export_csv(gen_data_df)
    write_mysql(gen_data_df,table_name,conf,)
