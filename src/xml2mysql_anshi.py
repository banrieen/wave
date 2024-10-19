import tomllib
import time
import pdb
from mysqlSync import mysql_sync
from xmlParser import Parser as pe

"""
将 xml map list 更新到mysql数据库

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
        root, ns = file_client.get_content(source, conf["txt_parser"]["info_rows"], conf["txt_parser"]["list_rows"])
        map_info = file_client.parse_file_info(root, ns, conf=[])
        map_bin_table = file_client.parse_bin_table(root, ns, conf=[])
        map_list = file_client.parse_map_list(root, ns, conf=[])

    except FileExistsError as fe:
        raise FileExistsError(f"=====>>> {source} parser fail.")
    # Init mysql connection
    my_client = mysql_sync() 
    my_client.conn(conf["dataset_db"])
    
    # 插入 map info
    print(f"=====>>> data info Sql commit ended at {time.strftime('%X')}")
    # info_colunms = conf["E142_map_info"].keys() 
    insert_paras_table(my_client, 
                conf["map_info"]["E142_map_info_table"], 
                tuple(conf["E142_map_info"].keys()), 
                map_info.values())
    ## insert bintable
    # 转换为 map dataframe
    colunms = tuple(conf["E142_map_list"].keys())
    map_bin_table_df = file_client.get_df(map_bin_table)
    # 给 bin table 添加外键，用于区分不同的wafer
    join_colunms = tuple(conf["E142_foreign_key"].keys())
    map_bin_table_df = file_client.add_series(map_bin_table_df, map_info, join_colunms, len(map_bin_table))
    # 获取表结构schema, 数据行，导入数据库
    columns, rows = file_client.get_rows(map_bin_table_df, has_header=True)
    insert_dict_table(my_client, 
            conf["map_info"]["E142_map_bintable_table"], 
            columns, 
            rows)

    ## Insert map list
    # 转换为 map dataframe
    columns = tuple(conf["E142_map_list"].keys())
    
    map_list_df = file_client.combine_df(columns, map_list)
    # 给 map list 添加外键，用于区分不同的wafer
    join_colunms = tuple(conf["E142_foreign_key"].keys())
    map_list_df = file_client.add_series(map_list_df, map_info, join_colunms, len(map_list))
    # 获取表结构schema, 数据行，导入数据库
    columns, rows = file_client.get_rows(map_list_df, has_header=True)
    
    insert_dict_table(my_client, 
            conf["map_info"]["E142_map_list_table"], 
            columns, 
            rows)

    print(f"finished at {time.strftime('%X')}")
    my_client.cnx.close()
    print(f"=====>>> data list Sql commit ended at {time.strftime('%X')}")

if __name__ == "__main__":
    conf = "conf/cnf_anshi.toml"
    project = "LED_anshi"
    # truncate_ragged_lines = False
    join_colunms=("Device_Name", "Lot_Number", "Vendor_Lot", "Wafer_Number")
    source = r"C:\workspace\ProductManageSpace\00-示例数据\安世-Map数据\E142Sample\WLJ2LW01-B6_E3.xml"
    file_type = "xml"
    select_colunms = ()
    runner(source, conf, project)
