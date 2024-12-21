import tomllib
import time
import pdb
from mysqlSync import mysql_sync
from txtParser import Parser as pe

"""
将 txt map list 更新到mysql数据库

"""

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

def insert_paras_table(my_client, dut_info_tablename, dut_info_schema, vals):
    dut_info_schema = ', '.join(["`"+col+"`" for col in dut_info_schema])
    insert_sql = "INSERT INTO %s (%s) VALUES (%s);" % (dut_info_tablename, dut_info_schema, ', '.join(['%s'] * len(vals)))
    my_client.execute(insert_sql, tuple(vals))
    my_client.cnx.commit()

def insert_dict_table(my_client, dut_list_tablename, columns, dut_rows):
    val_many = dut_rows
    table_schema = ', '.join(["`"+col+"`" for col in columns])
    insert_sql = "INSERT INTO %s (%s) VALUES (%s);" % (dut_list_tablename, table_schema, ', '.join(['%s'] * len(columns)))
    my_client.execute_many(insert_sql, val_many)
    my_client.cnx.commit()

def runner(source, conf="", project="default"):
    conf = get_conf(conf, project)

    # 获取 data list
    try:
        file_client = pe()
        map_info, map_list = file_client.get_content(source, conf["txt_parser"]["info_rows"], conf["txt_parser"]["list_rows"])
        select_colunms = conf["txt_map_info"].keys() 
        map_info = file_client.parse_file_info(map_info, split_tag=conf["txt_parser"]["split_tag"])
        select_colunms = conf["txt_map_list"].keys() 

        map_list = file_client.parse_map_list(map_list, conf["txt_parser"]["non_die_tag"])
    except FileExistsError as fe:
        raise FileExistsError(f"=====>>> {source} parser fail.")
    # Init mysql connection
    my_client = mysql_sync() 
    my_client.conn(conf["dataset_db"])

    # 插入 data list
    print(f"=====>>> data info Sql commit ended at {time.strftime('%X')}")
    
    insert_paras_table(my_client, 
                conf["map_info"]["txt_map_info_table"], 
                tuple(conf["txt_map_info"].keys()), 
                map_info.values())
    # 转换为 map dataframe
    columns = tuple(conf["txt_map_list"].keys())
    df = file_client.get_df(columns, map_list)
    # 给 map list 添加外键，用于区分不同的wafer
    join_colunms = tuple(conf["columns4join"].keys())
    df = file_client.add_series(df, map_info, join_colunms, len(map_list))
    # 获取表结构schema, 数据行，导入数据库
    columns, rows = file_client.get_rows(df, has_header=True)
    print(f"=====>>> data list Sql commit ended at {time.strftime('%X')}")
    insert_dict_table(my_client, 
            conf["map_info"]["txt_map_list_table"], 
            columns, 
            rows)

    print(f"finished at {time.strftime('%X')}")
    my_client.cnx.close()


if __name__ == "__main__":
    conf = "conf/cnf_anshi.toml"
    project = "LED_anshi"
    # truncate_ragged_lines = False
    join_colunms=("Device_Name", "Lot_Number", "Vendor_Lot", "Wafer_Number")
    source = r"C:\workspace\ProductManageSpace\00-示例数据\安世-Map数据\CYG DBL1\02_BINMAP_E74900B_W03.txt"
    file_type = "txt"
    select_colunms = ()
    runner(source, conf, project)
