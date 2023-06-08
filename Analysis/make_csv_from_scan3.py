#encoding: utf-8
import numpy as np
import pandas as pd
import MakeMap

p = MakeMap()

import glob
cheetah_logs = glob.glob("*master.log")
df = p.prepMap(cheetah_logs, "coordinate.log")

messages = df['message'].values
print(messages)

# DataFrameを作成
pivot = df.pivot(index='Z_value', columns='Y_value', values='score')
filename_df = df.pivot(index='h', columns='v', values='message')

import seaborn as sns
import matplotlib.pyplot as plt

def onclick(event):
    ix, iy = int(round(event.xdata)), int(round(event.ydata))
    #print(f"Filename: {filename_df.iloc[iy, ix]}")
    # python1でprint
    print("Filename: %s" % filename_df.iloc[iy, ix])

def onclick(event):
    ix, iy = int(round(event.xdata)), int(round(event.ydata))
    # python1でprint
    print("Filename: %s" % filename_df.iloc[iy, ix])

fig, ax = plt.subplots()
sns.heatmap(pivot,cmap='RdBu')
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()