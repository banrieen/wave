import os
import pandas as pd
import polars as pl
import pdb

class Parser:
    def __init__(self):
        pass

    def get_filelist(self, file_dir, filetype="xlsx"):
        """
        获取文件列表,判断文件后缀
        >>> get_filelist("tests.")
        "tests.csv"
        >>> get_filelist(r"tests/")
        ["tests.xlsx","tests1.xlsx","tests2.xlsx",]
        """
        if os.path.isdir(file_dir):
            return [os.path.join(root,ifile) for (root,dirs,files) in os.walk(file_dir, topdown=True) if len(files) for ifile in files if filetype in os.path.splitext(ifile)[-1]]
        elif os.path.isfile(file_dir):
            return file_dir
        else:
            raise FileExistsError(f"{file_dir} is not a dir or a file !")

    def get_file_info(self, csv_file, rows, schema, select_colunms=("column_1","column_2")):
        csv_info = ( 
             pl.scan_csv(source=csv_file, n_rows=rows, has_header=False, try_parse_dates=True, truncate_ragged_lines=True)
             .select(select_colunms)
             ).collect()
        csv_info = csv_info.transpose(include_header=False, column_names="column_1")
        return csv_info.to_dict(as_series=False), csv_info.select(schema).rows()[0]

    def get_row_list(self, filepath, sheet_id, select_colunms, truncate_ragged_lines=False, has_header=True):
        data_list = pl.read_excel(source=filepath, 
                    sheet_id=sheet_id, 
                    xlsx2csv_options={"skip_empty_lines": False},
                    read_csv_options={"infer_schema_length": 200, 
                                "truncate_ragged_lines": truncate_ragged_lines,
                                "has_header": has_header,},
                    ).select(select_colunms)
        return data_list

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

    def get_rows(self, df, has_header=True):
        if 'DataFrame' == type(df).__name__ and has_header:
            return df.columns, df.rows()
        elif 'DataFrame' != type(df).__name__ and has_header:
            return df.columns, df.collect().rows()
        elif 'DataFrame' != type(df).__name__ and not has_header:
            return df.collect().rows()
        else:
            return df.rows()

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