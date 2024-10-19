import csv
import os
import pandas as pd
import polars as pl
import pdb

class csvParser:
    def __init__(self):
        pass

    def get_filelist(self, file_dir):
        """
        获取csv文件列表,判断文件后缀
        >>> get_filelist("tests.")
        "tests.csv"
        >>> get_filelist(r"tests/")
        ["tests.csv","tests1.csv","tests2.csv",]
        """
        if os.path.isdir(file_dir):
            return [os.path.join(root,ifile) for (root,dirs,files) in os.walk(file_dir, topdown=True) if len(files) for ifile in files if "csv" in os.path.splitext(ifile)[-1]]
        elif os.path.isfile(file_dir):
            return file_dir
        else:
            raise FileExistsError(f"{file_dir} is not a dir or a file !")

    def extract_csv_read(self, csv_file="", conf={}): 
        """
        将不规范的csv文件按内容需要分类2类,默认读取本地文件
        :csv_file: str 可读取的csv文件，包含可访问的路径
        :conf: dict 隐射字段配置
        :return: list
        :csv_info_raw: 基础信息，每行一项配置
        :csv_dut_raw: 主要数据表头 + 行数据
        >>> extract_csv(xxx.csv)
        tupel(csv_info_raw, csv_dut_raw)

        """                        
        csv_info_raw = []
        csv_dut_raw = []
        with open(csv_file, newline='', encoding='utf-8') as spamreader:
            spamreader = csv.reader(spamreader, delimiter=' ', quotechar='|')
            spamreader = list(filter(None,spamreader))
            csv_info_raw = spamreader[:conf['dut_info_row']]
            csv_dut_raw = spamreader[conf['dut_list_row']:]
        return csv_info_raw, csv_dut_raw

    def parse_dut_info(self, csv_info_raw):
        """
        将info内容解析为 dict
        :csv_info_raw: 基础信息，每行一项配置
        :return: 行数据的 dict生成式，
        >>> extract_csv(xxx.csv)
        tupel(csv_info_raw, csv_dut_raw)

        """  
        return {itm[0].split(",,")[0]:itm[0].split(",,")[1] for itm in csv_info_raw }

    def parse_dut_list(self, csv_dut_raw, dut_list_schema):
        """
        将结果内容解析为 df
        :csv_dut_raw: 主要数据表头 + 行数据
        :dut_list_schema: 人工分析需要的列
        :return: 行数据的 dataframe， 便于之后的filter
        >>> extract_csv(xxx.csv)
        tupel(csv_info_raw, csv_dut_raw)

        """  
        header = csv_dut_raw[0][0].split(',')
        value_len = len(header)
        values = [iv[0].split(',')[:value_len] for iv in csv_dut_raw[1:]]
        df = pd.DataFrame(columns=header, data=values)
        dut_list = df.filter(items=[itm.strip() for itm in dut_list_schema.split(',')])
        return dut_list

    def get_csv_info(self, csv_file, rows, schema, select_colunms=("column_1","column_2")):
        csv_info = ( 
             pl.scan_csv(source=csv_file, n_rows=rows, has_header=False, try_parse_dates=True, truncate_ragged_lines=True)
             .select(select_colunms)
             ).collect()
        csv_info = csv_info.transpose(include_header=False, column_names="column_1")
        return csv_info.to_dict(as_series=False), csv_info.select(schema).rows()[0]

    def get_csv_list(self, csv_file, rows, select_colunms):
        csv_list = ( 
                pl.scan_csv(source=csv_file, skip_rows=rows, ignore_errors=True)
                .select(select_colunms)
                )
        return csv_list

    def add_series(self, df, add_series, add_culumns, row_counts):
        if df.width and len(add_series):
            for ac in add_culumns:
                # 准备插入的信息头
                add_col = pl.Series(ac, [add_series[ac][0]]*int(row_counts))
                df = df.with_columns(add_col)
            return df
        else:
            return False

    
    def get_dict(self, df):
        to_dict = df.collect().to_dict(as_series=False)
        # to_list = list(df.collect().to_arrow())
        return df.columns, to_dict
    
    def get_pandas(self, df):
        to_pndas = df.collect().to_pandas()
        return df.columns, to_pndas

    def get_rows(self, df):
        return df.columns, df.collect().rows()

if __name__ == "__main__":
    conf_file = "conf/cnf_qianzhao.toml"
    project_name = "LED_CSV_QIANZHAO"
    csv = r"C:\workspace\etl_gan\pySpray\test\qianzhao.csv"
    cp = csvParser()
    # 获取信息头
    csv_info = cp.get_csv_info(csv_file=csv, rows=14)
    # 获取信息列表
    select_colunms = ("TEST","BIN","VF1","IR","PosX","PosY")
    
    csv_list = cp.get_csv_list(csv_file=csv, 
            rows=52,
            select_colunms=select_colunms, 
            )
    add_culumns = ("FileName","Operator","TesterModel")
    # 插入需要关联的信息头
    added_list = cp.add_series(df=csv_list, 
                  add_series=csv_info, 
                  add_culumns=add_culumns, 
                  row_counts=csv_info["TotalTested"])
    print(f"======>>> {added_list.width}")
    print(f"======>>> {added_list.collect()}")
    to_dict = cp.get_dict(added_list)