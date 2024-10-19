"""
# 构造分析数据
"""

import polars as pl
import numpy as np
import pathlib
import random
import plotly.express as px
import pandas as pd
import pdb
RANDOM_SCOPE:int = 10000
random.seed(2023)
# import plotly.io as pio

def ploars2csv(filepath, df):
    path: pathlib.Path = filepath
    df.write_csv(path, separator=",")

def pandas2csv(filepath, df):
    path: pathlib.Path = filepath
    df.to_csv(path, index = False)

def ldsat_naturl(y):
    if y < 0.6 or y > 2.1:
        return y + random.uniform(-20.0,30.0)
    else:
        return y

def leff_map(y):
    if y > 17:
        return None
    elif y < 3:
        return None
    else:
        return y

def generate_ldsat()->pd.DataFrame:
    RANDOM_SCOPE = 1000
    lsdsat:list(float) = [random.uniform(0.6,2.2) for i in range(RANDOM_SCOPE)]
    ldoff_con:list(int) = [52*x+random.uniform(7,32) for x in lsdsat[:RANDOM_SCOPE//2] if x>0.6 or x<1.8 ]
    ldoff_opt:list(int) = [25*x+random.uniform(7,30) for x in lsdsat[RANDOM_SCOPE//2:] if x>0.9 or x<2.5 ]
    ldoff = ldoff_con + ldoff_opt
    ldoff = list(map(ldsat_naturl,ldoff))

    type_row:list(str) = ["Control"]*len(ldoff_con) + ["Optimized"]*len(ldoff_opt)
    
    default_technology:list(str) = ["NMOS", "PMOS"]
    technology:list(str) = [random.choice(default_technology) for i in range(len(ldoff))]
    df = pd.DataFrame(
        {
        "lsdsat" : lsdsat,
        "ldoff" : ldoff,
        "technology" : technology,
        "type_row" : type_row,
        }
        )
    pandas2csv("test/ldsat.csv",df)
    return df

def generate_leff():
    RANDOM_SCOPE = 1000
    leff:list(float) = [random.randint(10,30) for i in range(RANDOM_SCOPE)]
    DIBL_7:list(int) = [3000/(x**2)-random.uniform(0.3,5) for x in leff[:RANDOM_SCOPE//2] ]
    DIBL_16:list(int) = [3000/(x**2)+random.uniform(1,7)  for x in leff[RANDOM_SCOPE//2:] ]
    DIBL = DIBL_7 + DIBL_16
    DIBL = list(map(leff_map,DIBL))
    type_row:list(str) = ["7nm"]*len(DIBL_7) + ["16nm"]*len(DIBL_16)
    
    default_technology:list(str) = ["NMOS", "PMOS"]
    technology:list(str) = [random.choice(default_technology) for i in range(len(DIBL))]
    df = pd.DataFrame(
        {
        "leff" : leff,
        "DIBL" : DIBL,
        "technology" : technology,
        "type_row" : type_row,
        }
        )
    # breakpoint()
    pandas2csv("test/leff.csv",df)
    return df

import scipy
from scipy.stats import ecdf
import math
def generate_vgs():
    RANDOM_SCOPE = 10000
    NMOS_Vgs = np.linspace(-0.3, 0.8, RANDOM_SCOPE)
    PMOS_Vgs = np.linspace(-0.8, 0.3, RANDOM_SCOPE)
    NMOS_Vgs = [y+0.3 for y in np.sort(NMOS_Vgs)]
    NMOS_Vgs = list(map(vgs_naturl, NMOS_Vgs))
    PMOS_Vgs = [y+1 for y in np.sort(PMOS_Vgs)]
    PMOS_Vgs = list(map(vgs_naturl_PMOS, PMOS_Vgs))

    Vgs = [*NMOS_Vgs, *PMOS_Vgs]
    data_x = np.random.randn(RANDOM_SCOPE)
    cdf_values = ecdf(data_x)
    NMOS_lds = [-x+0.23 for x in cdf_values.cdf.quantiles]
    PMOS_lds = [x+0.23 for x in cdf_values.cdf.quantiles]
    lds = [*NMOS_lds, *PMOS_lds]

    technology_row:list(str) = ["PMOS"]*(RANDOM_SCOPE)+ ["NMOS"]*(RANDOM_SCOPE)
    Vds_scope = ','.join(["0.5", "0.7"])  ## 0.5~0.7v
    DIBL = -35  ## -35mV/V
    Swing = 65 # mV/Dec
    notes = f"""
        |Vds| = {Vds_scope}V
        DIBL = {DIBL}mV/V
        Swing = {Swing}mV/Dec
    """
    # breakpoint()
    dataset = {
        "Vgs" : lds,
        "lds" : Vgs,
        "technology" : technology_row,
        }
    df = pl.DataFrame(dataset)
    
    # df = zhuangzhi_df(df)
    ploars2csv("test/Vgs.csv",df)
    return df, notes

def zhuangzhi_df(df):
    # breakpoint()
    v_df = df.select("Vgs", "lds")
    rows = [np.dot(v_df.row(i), [[0, 1], [-1, 0]]) for i in range(v_df.shape[0])]
    v_df = pl.DataFrame(rows, ["Vgs", "lds"])
    v_df = v_df.with_columns(df.select("technology"))
    return v_df

def vgs_naturl(y):
    # 凑数据
    if y <= 0.18 :
        return None
    elif y<=0.37:
        return y + (1-y*2.8)**2  #np.random.uniform(low=0, high=0.12)
    else:
        return y


def vgs_naturl_PMOS(y):
    # 凑数据
    if y <= 0.23 :
        return None
    elif y<=0.37:
        return y + (1-y*2.8)**2  #np.random.uniform(low=0, high=0.12)
    else:
        return y

def generate_sqrt()->pd.DataFrame:
    RANDOM_SCOPE = 1000
    sqrt:list(int) = [random.uniform(0,30) for i in range(RANDOM_SCOPE)]
    sigma_7:list(int) = [1.2*x+random.uniform(0,7) for x in sqrt[:RANDOM_SCOPE//2] ]
    sigma_16:list(int) = [0.9*x+random.uniform(0,6) for x in sqrt[RANDOM_SCOPE//2:] ]
    # sigma_7:list(int) = [1.2*x for x in sqrt[:RANDOM_SCOPE//2] ]
    # sigma_16:list(int) = [0.9*x for x in sqrt[RANDOM_SCOPE//2:] ]
    sigma = sigma_7 + sigma_16
    sigma = list(map(sqrt_naturl,sigma)) # 抽取离散值

    type_row:list(str) = ["16nm"]*len(sigma_7) + ["7nm"]*len(sigma_16)
    
    default_technology:list(str) = ["NMOS", "PMOS"]
    technology:list(str) = [random.choice(default_technology) for i in range(len(sigma))]
    dataset = pd.DataFrame(
        {
        "sqrt" : sqrt,
        "Sigma_Vt" : sigma,
        "technology" : technology,
        "type_row" : type_row,
        }
        )
    df = pd.DataFrame(dataset)
    pandas2csv("test/sqrt.csv",df)
    return df

def sqrt_naturl(y):
    if y > 30:
        return None
    elif 28 < y and y > 20:
        y = y + random.uniform(-7.0,0)
        sample = [None, None, None, None, None, None, y]
        # random.shuffle(sample)
        return random.choice(sample)
    elif 18<y and y < 20:
        return y + random.uniform(0.0,5.0)
    else:
        return y

def generate_device_vt_options():
    dataset = {
        "Vts" : [],
        "LVT" : [],
        "technology" : ["NMOS", "PMOS"],
        "Device_Vt_Options" : ["nLVT", "LVT", "SVT", "HVT"],
        }
    df = pd.DataFrame(dataset)
    pandas2csv("test/device_vt_options.csv",df)

def generate_vg():
    RANDOM_SCOPE = 100
    Vg:list(float) = [random.uniform(1.4,2.8) for i in arange(RANDOM_SCOPE)]

    MTTF:list(float) = [-3*Vg[i] for i in arange(RANDOM_SCOPE)]
    Vt_shift:list(float) = [3*Vg[i]+6 for i in arange(RANDOM_SCOPE)]

    default_technology:list(str) = ["N_TDDB", "P_NBTI"]
    technology:list(str) = [random.choice(default_technology) for i in narange(RANDOM_SCOPE)]
    default_type_row:list(str) = ["7nm", "16nm"]
    type_row:list(str) = [random.choice(default_type_row) for i in arange(RANDOM_SCOPE)]

    dataset = {
        "Vg" : Vg,
        "MTTF" : MTTF,
        "Vt_shift":Vt_shift,
        "type_row" : type_row,
        "technology" : technology,
        }

    df = pd.DataFrame(dataset)
    pandas2csv("test/vg.csv",df)
    return df
'''Test chart

'''
def chart_ldsat(df):
    fig = px.scatter(df, x="lsdsat", y="ldoff", facet_col="technology", color="type_row",trendline="ols")
    fig.write_html("test/file.html")
    fig.show()
    results = px.get_trendline_results(fig)
    print(results)
    results_q = results.query("technology == 'NMOS' and type_row == 'Control'").px_fit_results.iloc[0].summary()
    print(results_q)

def chart_sqrt(df):
    """
        "sqrt" : sqrt,
        "Sigma_Vt" : sigma,
        "technology" : technology,
        "type_row" : type_row,
    """
    fig = px.scatter(df, x="sqrt", y="Sigma_Vt", facet_col="technology", color="type_row",trendline="ols")
    fig.write_html("test/sqrt.html")
    fig.show()
    results = px.get_trendline_results(fig)
    print(results)
    results_q = results.query("technology == 'NMOS' and type_row == 'Control'").px_fit_results.iloc[0].summary()
    print(results_q)

def chart_leff(df):
    fig = px.scatter(df, x="leff", y="DIBL", 
            facet_col="technology", 
            color="type_row",
            trendline="lowess",
            )
    fig.write_html("test/file.html")
    fig.show()
    results = px.get_trendline_results(fig)
    print(results)
    results_q = results.query("technology == 'NMOS' and type_row == 'Control'").px_fit_results.iloc[0].summary()
    print(results_q)

def chart_DeviceVtOption():
    df = px.data.tips()
    fig = px.box(df, y="total_bill")
    fig.show()
    pandas2csv("test/quxian.csv",df)
    pass

def chart_vgs(df):
    """
    dataset = {
    "NMOS_Vgs" : NMOS_Vgs,
    "PMOS_Vgs" : PMOS_Vgs,
    "technology" : technology_row,
    }
    """
    fig = px.line(df, 
        x="Vgs", # Vgs
        y="lds", # lds
        color="technology", 
        )
    fig.show()


def chart_vg(df):
    # df = px.data.gapminder().query("continent == 'Oceania'")
    fig = px.line(df, x='Vg', y='MTTF',facet_col="technology", color='type_row', markers=True)
    fig.show()

# df = generate_ldsat()
# scater_trendline(df)
# df = generate_leff() # 需要做
# scater_log_line(df)

df, notes = generate_vgs()
df = df.to_pandas()
chart_vgs(df)
# df = generate_sqrt()
# chart_sqrt(df)
# generate_device_vt_options() # 需要做
# df = generate_vg()
# vg_linx_chart(df)
