#!/usr/bin/env python
# coding: utf-8

import os,sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# LOG LINE
# osc_295_0/beam_1132_1035/IDXREF.LP: UNIT CELL PARAMETERS     37.706    38.504   118.645 172.435   8.360 171.884

lines = open("cells.log","r").readlines()

dict_list=[]
for line in lines:
    #print(line)
    cols=line.split()
#     print(len(cols))
    if len(cols)!=10:
        print("Parsing failed. This line is skipped")
        continue
    cella=float(cols[4])
    cellb=float(cols[5])
    cellc=float(cols[6])

    alpha=float(cols[7])
    beta=float(cols[8])
    gamma=float(cols[9])

    diffa=np.fabs(cella-5.0)
    diffb=np.fabs(cellb-14.0)
    diffc=np.fabs(cellc-14.0)
    diff_alpha=np.fabs(alpha-90.0)
    diff_beta=np.fabs(beta-90.0)
    diff_gamma=np.fabs(gamma-90.0)
    diff_total = diffa + diffb+ diffc + diff_alpha + diff_beta + diff_gamma

    beam=line.split("/")[1].replace("beam_","")
    dataname=line.split("/")[0]
    #print(beam)
    beam_param=beam.split("_")
    beamx=float(beam_param[0])
    beamy=float(beam_param[1])

    # making dictionary
    tmpdict = {"data_name":dataname,"cella": cella, "cellb":cellb, "cellc": cellc, "alpha": alpha, "beta": beta, "gamma": gamma, "beamx":beamx, "beamy":beamy,"diffa":diffa, "diffb":diffb, "diffc":diffc, "diff_alpha":diff_alpha, "diff_beta":diff_beta, "diff_gamma":diff_gamma, "diff_total":diff_total}
    dict_list.append(tmpdict)

df = pd.DataFrame(dict_list)
print(df.describe())

# diff total が小さい
sel01 = df['diff_total'] < 10

# 格子定数の差は5未満
sel02 = df['diffa'] < 1.0
sel03 = df['diffb'] < 2.0
sel04 = df['diffc'] < 2.0

df01 = df[sel01 & sel02 & sel03 & sel04]
print(df01.describe())
print(df01['data_name'])

# diff total が小さい
sel01 = df['diff_total'] < 20

# 格子定数の差は5未満
sel02 = df['diffa'] < 1.0
sel03 = df['diffb'] < 2.0
sel04 = df['diffc'] < 2.0

df01 = df[sel01 & sel02 & sel03 & sel04]
print(df01.describe())
df01.to_csv("score20.csv")

count_identical_data = 0
for data_name, proc_group in df01.groupby(['data_name']):
    print(data_name)
    count_identical_data+=1

print(count_identical_data)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(df01.beamx, df01.beamy, df01.diff_total, s=100)


