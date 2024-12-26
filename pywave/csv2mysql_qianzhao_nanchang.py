import tomllib
import time
import os
import pdb
from mysqlSync import mysql_sync
from csvParser import csvParser
from joblib import Parallel, delayed
from joblib import Memory
from joblib import cpu_count

"""
将csv更新到mysql数据库
etl_gan/pySpray/spray/csv2mysql.py
etl_gan/pySpray/test/test_parser.py

"""
CPU_CORES = cpu_count()
cachedir = '_cache_'
memory = Memory(cachedir, verbose=0)

@memory.cache
def get_conf(conf_file="default.toml", hostname="default"):
    """
    1. 读取toml格式配置文件
    2. 加载项目参数
    >>> get_conf("default.toml")
    if "default" in conf.keys():
        pass
    """
    conf = {}
    with open(conf_file, "rb") as f:
        conf = tomllib.load(f)
    conf = conf[hostname]
    return conf

@memory.cache
def insert_paras_table(my_client, dut_info_tablename, dut_info_schema, vals):
    insert_sql = "INSERT INTO %s (%s) VALUES (%s);" % (dut_info_tablename, dut_info_schema, ', '.join(['%s'] * len(vals)))
    my_client.execute(insert_sql, tuple(vals))
    my_client.cnx.commit()
    print(f"=====>>> Dut info Sql commit ended at {time.strftime('%X')}")

@memory.cache
def insert_df_table(my_client, dut_list_tablename, dut_list_schema,  columns, dut_rows):
    ## insert by rows values list at once
    val_many = dut_rows
    insert_sql = "INSERT INTO %s (%s) VALUES (%s);" % (dut_list_tablename, dut_list_schema, ', '.join(['%s'] * len(columns)))
    my_client.execute_many(insert_sql, val_many)
    my_client.cnx.commit()
    print(f"=====>>> Dut list Sql commit ended at {time.strftime('%X')}")

@memory.cache
def sync_to_sql(my_client, csv_client, csv_file, conf):
    dut_info_tablename = conf["analysis_info"]["dut_info_table"]
    dut_list_tablename = conf["analysis_info"]["dut_list_table"]
    dut_info, info_vals = csv_client.get_csv_info(csv_file, conf["analysis_info"]["dut_info_row"], conf["dut_info"].keys(), ("column_1","column_2"))
    dut_info_schema = ', '.join(conf["dut_info"].keys())
    # 插入头信息
    insert_paras_table(my_client, dut_info_tablename, dut_info_schema, info_vals)

    # 获取dut list
    dut_list = csv_client.get_csv_list(csv_file, conf["analysis_info"]["dut_list_row"], conf["dut_list"].keys())
    # 添加关联字段
    dut_list = csv_client.add_series(dut_list, dut_info, conf["dut_join"].values(), dut_info["TotalTested"][0])
    # breakpoint()
    # 插入 dut list
    columns, dut_rows = csv_client.get_rows(dut_list)
    dut_list_schema = ', '.join(columns)
    insert_dict_table(my_client, dut_list_tablename, dut_list_schema, columns, dut_rows)


def runner(conf_file="", project_name="default"):
    try:
        conf = get_conf(conf_file, project_name)
    except IOError as err:
        raise FileExistsError(f"{conf_file} is not exist !")
    
    csv_client = csvParser()
    csv_files = csv_client.get_filelist(conf["info"]["csv_path"])
    
    # Init mysql connection
    my_client = mysql_sync() 
    my_client.conn(conf["dataset_db"])
    # Get files
    for file in csv_files:
        print(f"=====>>> Executed {file} at {time.strftime('%X')}")
        sync_to_sql(my_client, csv_client, file, conf) 
    ## 调用多线程执行
    ## ====================================================================================
    ## generated an exception: 'mysql_sync' object is not subscriptable
    # with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
    #     print(f"Cached started at {time.strftime('%X')}")
    #     future_to_insert = {executor.submit(sync_to_sql, csv_file, conf["analysis_info"], my_client): csv_file for csv_file in csv_files} 
    #     for future in concurrent.futures.as_completed(future_to_insert):
    #         print(f"Executed {csv_files} at {time.strftime('%X')}")
    #         rst = future_to_insert[future]
    #         try:
    #             data = future.result()
    #         except Exception as exc:
    #             print('%r generated an exception: %s' % (rst, exc))
    #         else:
    #             pass
    ## ======================================================================================

    print(f"finished at {time.strftime('%X')}")
    my_client.cnx.close()

if __name__ == "__main__":
    conf_file = "conf/cnf_qianzhao_01.toml"
    project_name = "LED_CSV_QIANZHAO"

    # 获取信息头
    # csv = r"C:\workspace\etl_gan\pySpray\test\qianzhao.csv"
    # csv_info = cp.get_csv_info(csv_file=csv, rows=14)
    runner(conf_file=conf_file, project_name=project_name)