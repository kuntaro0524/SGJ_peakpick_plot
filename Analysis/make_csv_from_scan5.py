#encoding: utf-8
import sys
import numpy as np
import pandas as pd
import MakeMap
import glob
import seaborn as sns
import matplotlib.pyplot as plt

p = MakeMap.MakeMap()

# output directory of cbf files
relative_path = sys.argv[1]
threshold = float(sys.argv[2])
prefix=sys.argv[3]

cheetah_logs = glob.glob("%s/*master.log"%relative_path)
df = p.prepMap(cheetah_logs, "coordinate.log")

messages = df['message'].values

# DataFrameを作成
pivot = df.pivot(index='Z_value', columns='Y_value', values='score')
filename_df = df.pivot(index='h', columns='v', values='message')

def onclick(event):
    ix, iy = int(round(event.xdata)), int(round(event.ydata))
    # python1でprint
    print("Filename: %s" % filename_df.iloc[iy, ix])

fig, ax = plt.subplots()

# score で thresholdを切る
# 1E12 phs/frame
df_final = df[df['score'] >= threshold]

# 測定用のCSVファイル
csv_out = "oscillation.csv"
ofile = open(csv_out, 'w')

for index,row in df_final.iterrows():
    int_z = int(row['Z_value'])
    int_y = int(row['Y_value'])
    int_score = int(row['score'])
    filename = "%s%s/%s_%s_%s.cbf" % (relative_path, prefix, prefix, int_y, int_z)
    ofile.write("%s,%s,%s,%s\n" % (filename, int_score, int_y, int_z))

ofile.close()

# draw heatmap

sns.heatmap(pivot,cmap='RdBu')
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
plt.savefig("heatmap.png")
