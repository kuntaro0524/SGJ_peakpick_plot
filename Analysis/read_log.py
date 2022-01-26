import sys,os,glob
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

#cheetah_logs = glob.glob("*001*master.log")
cheetah_logs = glob.glob("*master.log")

# cheetah のログファイルを読んでフレーム番号でソートする
def read_log(filename):
    data_line=[]
    lines = open(filename,"r").readlines()
    for line in lines[2:]:
        cols = line.split()
        frame_num = int(cols[0])
        score = int(cols[1])
        data_line.append((frame_num, score))

    #print(data_line)
    # sorting by the frame number
    data_line.sort(key=lambda x:x[0])

    return data_line

# Read cordinate log from Amane soft
# あまねソフトのYZ座標が書いてあるやつ
lines = open("coordinate.log","r").readlines()
code_map=[]
for line in lines:
    cols=line.strip().split(",")
    #print(cols)
    code_box=[]
    for col in cols:
        ridstr=col.replace("(","").replace(")","")
        value = ridstr.split("/")
        xcode = float(value[0])
        ycode = float(value[1])
        # 座標として単純に取り込んでいる
        code_box.append((xcode,ycode))
    # １行のリストを格納している
    code_map.append(code_box)

# numpy array へ変換している
# 測定順に座標が格納されていると思えば良い
np_code_map = np.array(code_map)
print(np_code_map)

print("CODE MAP SHAPE:",np_code_map.shape)

# Reading each log from cheethah
cheetah_logs.sort()
allmap=[]
for logfile in cheetah_logs:
    print("Processing %s"% logfile)
    # フレーム順にスコアが並んだリスト（各HD5ファイル）
    data_line=read_log(logfile)
    print(type(data_line))
    print(data_line)
    allmap.append(data_line)

np_map=np.array(allmap)
print("<NPmap>")
print(np_map)
print("</NPmap>")
print("Score map shape:",np_map.shape)
(nv, nh, ndata) = np_map.shape
print(nv,nh,ndata)

# スポットの数とYZ座標を一緒に扱うためのマップ
final_map=[]
check_map=[]
for i in range(0,nv):
    for j in range(0,nh):
        score=np_map[i][j][1]
        x,y=np_code_map[i][j]
        final_map.append((x,y,score))
        # これまでの整数座標とYZ座標の対応を確認するためのマップ
        #check_map.append((i,j,x,y,score))

# マップをnumpy arrayに変換
new_map=np.array(final_map)
print("##############################")
for elem_score, elem_code in zip(np_map, np_code_map):
    print(elem_score)
    score=elem_score
    print(score)

# Pandas treatment
import pandas as pd

# X,Y, Score という配列をPandas data frame へ変換
df = pd.DataFrame.from_dict((new_map))
print(df)
df.columns = ['X_value','Y_value','Z_value']
df['Z_value'] = pd.to_numeric(df['Z_value'])
df['X_value'] = pd.to_numeric(df['X_value'])
df['Y_value'] = pd.to_numeric(df['Y_value'])

pivotted= df.pivot('Y_value','X_value','Z_value')
sns.heatmap(pivotted,cmap='RdBu')

# Making the final map .csv
df.to_csv("test.csv")

plt.savefig("ana_ooo.png")
plt.show()

# 一応、整数座標とYZ座標（あまねそふと）が対応していることは確認した
# 2022/01/26
#print(check_map)

# Z value があるしきい値よりも高い場合のもののみ dataframeを取り出す
df_new = df.copy()
z_sel = df_new['Z_value']<3
df_new.loc[z_sel,'Z_value']=0

pivotted= df_new.pivot('Y_value','X_value','Z_value')
sns.heatmap(pivotted,cmap='RdBu')
plt.savefig("ana_iii.png")