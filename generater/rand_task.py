#!.venv/bin/python
"""生成任务列表
支持 rstful API
数据源管理
数据加载
数据生成

"""

# 
import polars as pl
uri = "mysql://thomas:thomas@192.168.56.113:3306/rpa_vt"
query = "SELECT * FROM rpa_vt.flow_target_record;"

pl.read_database_uri(query=query, uri=uri)
print(pl)