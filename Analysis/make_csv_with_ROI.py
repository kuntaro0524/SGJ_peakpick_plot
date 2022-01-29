import sys,os,glob
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# しきい値

# 絶対パスから２個上くらいのパスを取得する
abs_path = os.path.abspath("./")
path_parts = abs_path.split('/')
relative_path = ""
for p in path_parts[-2:]:
    relative_path = os.path.join(relative_path,p)

# 行ごとに処理をしてCSVファイルを作成する
csv_name = "collect_list.csv"
df = pd.read_csv(csv_name)

df.columns = ['filename','score','Y_value','Z_value']
new_csv = "collect_list_ROI.csv"
ofile=open(new_csv, "w")

for index,row in df.iterrows():
    int_z = int(row['Z_value'])
    int_y = int(row['Y_value'])
    int_score = int(row['score'])
    if int_z < 1600:
        filename = "%s/osc_%s_%s.cbf" % (relative_path, int_y, int_z)
        ofile.write("%s, %s, %s, %s\n" % (filename, int_score, int_y, int_z ));

