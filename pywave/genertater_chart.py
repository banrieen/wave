"""
# 构造分析数据
"""

import polars as pl
import math
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

def liqunzhi_map(y):
    if y < 0.6 or y > 2.1:
        return y + random.uniform(-20.0,30.0)
    else:
        return y

def leff_map(y):
    if y> 17:
        return None
    elif y <3:
        return None
    else:
        return y

def generate_ldsat():
    RANDOM_SCOPE = 1000
    lsdsat:list(float) = [random.uniform(0.6,2.2) for i in range(RANDOM_SCOPE)]
    ldoff_con:list(int) = [52*x+random.uniform(7,32) for x in lsdsat[:RANDOM_SCOPE//2] if x>0.6 or x<1.8 ]
    ldoff_opt:list(int) = [25*x+random.uniform(7,30) for x in lsdsat[RANDOM_SCOPE//2:] if x>0.9 or x<2.5 ]
    ldoff = ldoff_con + ldoff_opt
    ldoff = list(map(liqunzhi_map,ldoff))

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
    dataset = {
        "leff" : [],
        "DIBL" : [],
        "technology" : ["NMOS", "PMOS"],
        "type" : ["7nm", "16nm"],
        }
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

def figure_ldsat(df):
    fig = px.scatter(df, x="lsdsat", y="ldoff", facet_col="technology", color="type_row",trendline="ols")
    fig.write_html("test/file.html")
    fig.show()
    results = px.get_trendline_results(fig)
    print(results)
    results_q = results.query("technology == 'NMOS' and type_row == 'Control'").px_fit_results.iloc[0].summary()
    print(results_q)

def figure_leff(df):
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

def figure_vg(df):
    fig = px.line(df, x='Vg', y='MTTF',facet_col="technology", color='type_row', markers=True)
    fig.show()

df = generate_ldsat()
figure_ldsat(df)
df = generate_leff() # 需要做
figure_leff(df)

# df = generate_vg()
# figure_vg(df)
