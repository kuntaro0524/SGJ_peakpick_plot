# -*- coding: utf-8 -*-
import sys,os,glob
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

isDebug = False

# 絶対パスから２個上くらいのパスを取得する
# CSVファイルにそういうパスを書く必要があるため→おまじない・・・
abs_path = os.path.abspath("./")
path_parts = abs_path.split('/')
relative_path = ""
for p in path_parts[-2:]:
    relative_path = os.path.join(relative_path,p)

cheetah_logs = glob.glob("*master.log")
score_thresh = int(sys.argv[1])

# cheetah のログファイルを読む
# 1行ごとに　フレーム番号とスコアが書いてある
# linesはすべての行のリスト
def read_log(filename):
    # 一時的なリスト
    data_line=[]
    lines = open(filename,"r").readlines()
    # 3行目から読み込んでいる
    for line in lines[2:]:
        cols = line.split()
        frame_num = int(cols[0])
        score = int(cols[1])
        data_line.append((frame_num, score))

    # sorting by the frame number
    # このリストには行ごとにフレーム番号とスコアが格納されている
    # フレーム番号はY座標に相当する（横方向）
    data_line.sort(key=lambda x:x[0])

    # １次元のnumpy arrayに変換したい
    data_array = np.array(data_line)
    print(data_array.shape)

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
#print(np_code_map)
#print("CODE MAP SHAPE:",np_code_map.shape)

# Reading each log from cheethah
cheetah_logs.sort()
allmap=[]
for logfile in cheetah_logs:
    print("Processing %s"% logfile)
    # そもそもログファイル１個がスキャン１行に相当している
    # フレーム順にスコアが並んだリスト（各HD5ファイル）
    # Fast軸のフレーム数分ここにデータが入っている
    data_line=read_log(logfile)
    # 二次元マップを積み上げていくイメージ
    allmap.append(data_line)

np_map=np.array(allmap)
# print("<NPmap>")
print(np_map.shape)
# print("</NPmap>")

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
        # nhは各行の中でどの位置のイメージ番号かを示している
        # adxvなどでイメージを見れると良い
        final_map.append((i,j,x,y,score))
        # これまでの整数座標とYZ座標の対応を確認するためのマップ
        #check_map.append((i,j,x,y,score))

# マップをnumpy arrayに変換
new_map=np.array(final_map)
for elem_score, elem_code in zip(np_map, np_code_map):
    #print(elem_score)
    score=elem_score
    #print(score)

# Pandas treatment
import pandas as pd

# X,Y, Score という配列をPandas data frame へ変換
df = pd.DataFrame.from_dict((new_map))
#print(df)
df.columns = ['h','v','Y_value','Z_value','score']
df['score'] = pd.to_numeric(df['score'])
df['Y_value'] = pd.to_numeric(df['Y_value'])
df['Z_value'] = pd.to_numeric(df['Z_value'])
df['h'] = pd.to_numeric(df['h'])
df['v'] = pd.to_numeric(df['v'])

for i in df['v']:
    print(i)

# 一応、整数座標とYZ座標（あまねそふと）が対応していることは確認した
# 2022/01/26
#print(check_map)

# Z value があるしきい値よりも高い場合のもののみ dataframeを取り出す
df_new = df.copy()
df_new.describe()
z_sel = df_new['score']<3
df_new.loc[z_sel,'score']=0

# Making the final map .csv for the data collection with AMANE
df_for_csv = df.copy()
z_sel = df_for_csv['score']> score_thresh
df_final = df_for_csv[z_sel]

# カラムの名前を理解できるものにつけ直す
df.to_csv("all_results.csv",index=False)

# 行ごとに処理をしてCSVファイルを作成する
csv_name = "collect_list.csv"
csvfile = open(csv_name,"w")

for index,row in df_final.iterrows():
    int_z = int(row['Z_value'])
    int_y = int(row['Y_value'])
    int_score = int(row['score'])
    filename = "%s/osc_%s_%s.cbf" % (relative_path, int_y, int_z)
    csvfile.write("%s, %s, %s, %s\n" % (filename, int_score, int_y, int_z ))

### GUI FUNCTION
pivotted= df_new.pivot('Z_value','Y_value','score')
sns.heatmap(pivotted,cmap='RdBu')
plt.show()

# dataframe 1行ごとに
# for index,row in df_new.iterrows():
    # print(row['nh'], row['nv'], row['score'])

def onclick(event):
    ix, iy = int(round(event.xdata)), int(round(event.ydata))
    #print(f"Score: {data[ix, iy]['score']}, Filename: {data[ix, iy]['filename']}")
    # dfの中からnhがix、nvがiyのものを表示する
    print(ix,iy)
    print(df[(df['h']==ix) & (df['v']==iy)])

    # print("score: %s, filename: %s" % (data[ix, iy]['score'], data[ix, iy]['filename']))

fig, ax = plt.subplots()
scores = df['score'].values.reshape(nv, nh)
ax.imshow(scores, cmap='hot', interpolation='nearest', origin='upper')
fig.canvas.mpl_connect('button_press_event', onclick)
 
plt.show()

