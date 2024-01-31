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

cheetah_logs = glob.glob("%s/*master.log"%relative_path)
df = p.prepMap(cheetah_logs, "coordinate.log")

messages = df['message'].values

# DataFrameを作成
pivot = df.pivot(index='Z_value', columns='Y_value', values='score')
filename_df = df.pivot(index='h', columns='v', values='message')

fig, ax = plt.subplots()
sns.heatmap(pivot,cmap='RdBu')

import matplotlib.patches as patches

# 初期選択を描画するためのパッチを作成します。
rect = patches.Rectangle((0,0),1,1,linewidth=1,edgecolor='yellow',facecolor='none')
ax.add_patch(rect)

def onclick(event):
    ix, iy = int(round(event.xdata - 0.5)), filename_df.shape[0] - 1 - int(round(event.ydata - 0.5))
    print("Filename: %s" % filename_df.iloc[iy, ix])
    
    # 古いパッチを削除し、新しいパッチを追加します。
    rect.set_xy((ix, filename_df.shape[0] - 1 - iy))
    fig.canvas.draw()

# ボタンプレスイベントとキープレスイベントに対応する関数を接続します。
fig.canvas.mpl_connect('button_press_event', onclick)

def on_key(event):
    # カーソルキーに応じて選択範囲を移動させます。
    if event.key == 'up':
        rect.set_y(min(filename_df.shape[0] - 1, rect.get_y() - 1))
    elif event.key == 'down':
        rect.set_y(max(0, rect.get_y() + 1))
    elif event.key == 'right':
        rect.set_x(min(filename_df.shape[1] - 1, rect.get_x() + 1))
    elif event.key == 'left':
        rect.set_x(max(0, rect.get_x() - 1))
    
    # 移動後の選択範囲の座標を取得します。
    ix, iy = int(rect.get_x()), filename_df.shape[0] - 1 - int(rect.get_y())
    print("Filename: %s" % filename_df.iloc[iy, ix])

    fig.canvas.draw()

fig.canvas.mpl_connect('key_press_event', on_key)
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

# score で thresholdを切る
df_final = df[df['score'] > 3.0]

# 測定用のCSVファイル
csv_out = "oscillation.csv"
ofile = open(csv_out, 'w')

for index,row in df_final.iterrows():
    int_z = int(row['Z_value'])
    int_y = int(row['Y_value'])
    int_score = int(row['score'])
    filename = "%s/osc_%s_%s.cbf" % (relative_path, int_y, int_z)
    ofile.write("%s,%s,%s,%s\n" % (filename, int_score, int_y, int_z))

ofile.close()
