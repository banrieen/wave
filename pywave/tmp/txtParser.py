import os
import polars as pl
import pdb

class Parser:
    def __init__(self):
        pass

    def get_filelist(self, file_dir, filetype="txt"):
        """
        获取文件列表,判断文件后缀
        >>> get_filelist("tests.")
        "tests.txt"
        >>> get_filelist(r"tests/")
        ["tests.txt","tests1.txt","tests2.txt",]
        """
        if os.path.isdir(file_dir):
            return [os.path.join(root,ifile) for (root,dirs,files) in os.walk(file_dir, topdown=True) if len(files) for ifile in files if filetype in os.path.splitext(ifile)[-1]]
        elif os.path.isfile(file_dir):
            return file_dir
        else:
            raise FileExistsError(f"{file_dir} is not a dir or a file !")


    def get_content(self, source, row_info_tag, row_list_tag):
        with open(source, newline='', encoding='utf-8') as f:
            lines = f.readlines()
            info = lines[:row_info_tag]
            list = lines[row_list_tag:]
            return tuple(info), tuple(list)

    def parse_file_info(self, info_list, split_tag=":", select_colunms=("column_1","column_2")):
        return {item.split(split_tag)[0]:item.split(":")[1].replace("\r\n","") for item in info_list if len(item.strip())}


    def parse_map_list(self, map_list, non_die_tag):
        map_list = [(map_list[posy][posx].strip(), posx, posy) for posy in range(len(map_list)) if len(map_list[posy].strip()) for posx in range(len(map_list[posy].replace("\r\n",""))) if len(map_list[posy][posx].strip()) and non_die_tag not in map_list[posy][posx].strip()]        
        return map_list

    def add_series(self, df, addIn_df, addIn_culumns, row_counts):
        if df.width and len(addIn_df):
            for ac in addIn_culumns:
                # 准备插入的信息头
                add_col = pl.Series(ac, [addIn_df[ac]]*int(row_counts))
                df = df.with_columns(add_col)
            return df
        else:
            return False
    def get_df(self, column, rows):
        df = pl.DataFrame(rows, column)
        return df
    
    def get_dict(self, df):
        to_dict = df.collect().to_dict(as_series=False)
        # to_list = list(df.collect().to_arrow())
        return df.columns, to_dict

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
    conf_file = "conf/cnf_anshi.toml"
    project_name = "LED_anshi"
    source = r"C:\workspace\ProductManageSpace\00-示例数据\安世-amp数据\02_BINMAP_E74900B_W04.txt"
    pa = Parser()
    conf = {
        "info_rows" : 15,
        "list_rows" : 15,
        "split_tag" : ":",
    }
    info, list = pa.get_content(source, conf)
    # 获取信息头
    select_colunms = []
    pa.parse_file_info(info, conf, select_colunms)
    # 获取map list
    pa.parse_map_list(list, conf, select_colunms)

