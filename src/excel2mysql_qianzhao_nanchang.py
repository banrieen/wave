import tomllib
import time
import pdb
from mysqlSync import mysql_sync
from excelParser import Parser as pe

"""
将 excel sheet 更新到mysql数据库

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
    insert_sql = "INSERT INTO %s (%s) VALUES (%s);" % (dut_info_tablename, dut_info_schema, ', '.join(['%s'] * len(vals)))
    my_client.execute(insert_sql, tuple(vals))
    my_client.cnx.commit()

def insert_dict_table(my_client, dut_list_tablename, table_schema,  columns, dut_rows):
    val_many = dut_rows
    insert_sql = "INSERT INTO %s (%s) VALUES (%s);" % (dut_list_tablename, table_schema, ', '.join(['%s'] * len(columns)))
    my_client.execute_many(insert_sql, val_many)
    my_client.cnx.commit()

def runner(source, table_name, conf_file="", select_colunms=(), project_name="default", truncate_ragged_lines=False, has_header=True):
    conf = get_conf(conf_file, project_name)

    # 获取 data list
    file_client = pe()
    select_colunms = conf[table_name].keys() if not len(select_colunms) else select_colunms
    
    df = file_client.get_row_list(source, 
                    conf["analysis_info"]["sheetID"], 
                    select_colunms,
                    truncate_ragged_lines=truncate_ragged_lines,
                    has_header=has_header)
    if has_header:
        columns, df_rows = file_client.get_rows(df)
    else:
        df_rows = file_client.get_rows(df, has_header)
        columns = tuple(conf["DataSource2"].keys())

    # Init mysql connection
    my_client = mysql_sync() 
    my_client.conn(conf["dataset_db"])
    tablename = conf["analysis_info"][table_name]

    # 插入 data list
    print(f"=====>>> data list Sql commit ended at {time.strftime('%X')}")
    table_schema = ["`"+col+"`" for col in columns]
    table_schema = ', '.join(table_schema)
    insert_dict_table(my_client, tablename, table_schema, columns, df_rows)

    print(f"finished at {time.strftime('%X')}")
    my_client.cnx.close()


if __name__ == "__main__":
    conf_file = "conf/cnf_qianzhao_nanchang.toml"
    project_name = "LED_CSV_QIANZHAO"
    has_header = True
    truncate_ragged_lines = True
    # truncate_ragged_lines = False
    select_colunms=("column_2","column_3")
    select_colunms=()
    source = r"C:\workspace\ProductManageSpace\25-乾照-厦门\乾照-南昌常用运用场景案例举例\DateSource\DataSource3.xlsx"
    table_name = "DataSource3"
    runner(source, table_name, conf_file, select_colunms, project_name, truncate_ragged_lines, has_header)