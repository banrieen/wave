import os
import polars as pl
from xml.etree import ElementTree as et
from xml.etree import ElementPath as xpath
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

    def get_content(self, source, namespaces, type="xml"):
        tree = et.parse(source)
        root = tree.getroot()
        ns = dict([node for _, node in et.iterparse(source, events=['start-ns'] )])
        return root, ns

    def parse_file_info(self, root, ns, conf=[]):
        map_info = {}
        """
        Add layout info
        """
        actor = root.find('Layouts', ns)
        # Add layout
        actor = root.findall('Layouts/Layout', ns)
        layout = [a.attrib for a in actor][0]
        map_info.update(layout)
        # Add Dimension
        actor_Dimension = root.findall('Layouts//Layout/Dimension', ns)
        wafer_Dimension = [a.attrib for a in actor_Dimension][0]
        map_info.update({"wafer_Dimension_X":wafer_Dimension["X"],"wafer_Dimension_Y":wafer_Dimension["Y"]})
        die_Dimension = [a.attrib for a in actor_Dimension][1]
        map_info.update({"die_Dimension_X":die_Dimension["X"],"die_Dimension_Y":die_Dimension["Y"]})
        # Add DeviceSize
        actor_DeviceSize = root.findall('Layouts//Layout/DeviceSize', ns)
        wafer_DeviceSize = [a.attrib for a in actor_Dimension][0]
        map_info.update({"wafer_DeviceSize_X":wafer_DeviceSize["X"],"wafer_DeviceSize_Y":wafer_DeviceSize["Y"]})
        die_DeviceSize = [a.attrib for a in actor_DeviceSize][1]
        map_info.update({"die_DeviceSize_X":die_DeviceSize["X"],"die_DeviceSize_Y":die_DeviceSize["Y"]})
        # Add stepsize
        actor_StepSize = root.find('Layouts//Layout/StepSize', ns)
        map_info.update({"StepSize_X":actor_StepSize.attrib["X"],"StepSize_Y":actor_StepSize.attrib["Y"]})
        # Add productID
        actor_ProductId = root.find('Layouts//Layout/ProductId', ns)
        map_info.update({"ProductId":actor_ProductId.text})
        """
        Add run info
        """
        actor_run = root.find('Substrates', ns)
        # Add lotID
        actor_LotId = actor_run.find("Substrate/LotId",ns)
        map_info.update({"LotId":actor_LotId.text})
        # Add run time
        actor_DATE_TIME = actor_run.findall('Substrate/AliasIds/AliasId', ns) 
        DATE_TIME = [a.attrib for a in actor_DATE_TIME][1:]
        DATE_TIME = {tuple(val.values())[0]:tuple(val.values())[1] for val in DATE_TIME}
        map_info.update(DATE_TIME)
        """ 解析 bin table 基础信息
        SubstrateType="Wafer" 
        SubstrateId="WLJ2LW01-B6_E1"
        BinType="HexaDecimal" 
        NullBin="FF"
        """
        actor_map = root.find('SubstrateMaps', ns)
        actor_SubstrateMap = actor_map.find("SubstrateMap",ns)
        SubstrateMap = actor_SubstrateMap.attrib
        map_info.update({"SubstrateId":SubstrateMap["SubstrateId"]})
        act_binmap = actor_map.find("SubstrateMap/Overlay/BinCodeMap",ns)
        map_info.update(act_binmap.attrib)
        RefCoordinates = actor_SubstrateMap.find("nxp:RefCoordinates",ns)
        map_info.update(RefCoordinates.attrib)
        return map_info

    def parse_bin_table(self, root, ns, conf=[]):
        bin_table = []
        actor_map = root.find('SubstrateMaps', ns)
        actor_SubstrateMap = actor_map.find("SubstrateMap",ns)
        act_binmap = actor_map.find("SubstrateMap/Overlay/BinCodeMap",ns)
        act_bincode = act_binmap.findall("BinDefinitions/BinDefinition",ns)
        return [bin.attrib for bin in act_bincode]
        

    def parse_map_list(self, root, ns, conf=[]):
        actor_map = root.find('SubstrateMaps', ns)
        actor_binmap = actor_map.find("SubstrateMap/Overlay/BinCodeMap",ns)
        actor_bincode = actor_binmap.findall("BinCode",ns)
        map_list = [dut.text for dut in actor_bincode]
        NullBin="FF"
        map_list = [(map_list[posY][posX:posX+2],posX,posY) for posY in range(len(map_list)) for posX in range(0, len(map_list[posY]), 2) if NullBin not in map_list[posY][posX:posX+2] ] 
        return map_list

    def get_df(self, list_dict):
        return pl.DataFrame(list_dict)

    def combine_df(self, column, rows):
        df = pl.DataFrame(rows, column)
        return df

    def add_series(self, df, addIn_df, addIn_culumns, row_counts):
        if df.width and len(addIn_df):
            for ac in addIn_culumns:
                # 准备插入的信息列
                add_col = pl.Series(ac, [addIn_df[ac]]*int(row_counts))
                df = df.with_columns(add_col)
            return df
        else:
            return False

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
    source = r"C:\workspace\ProductManageSpace\00-示例数据\安世-Map数据\E142Sample\WLJ2LW01-B6_E1.xml"
    parser = Parser()
    namespaces = "{urn:semi-org:xsd.E142-1.V0211.SubstrateMap}"

    root, ns = parser.get_content(source, namespaces, type="xml")
    info = parser.parse_file_info(root, ns, conf=[])
    bintable = parser.parse_bin_table(root, ns )
    list = parser.parse_map_list(root, ns, conf=[])



