# encoding: utf-8
import pandas as pd
import numpy as np

class MakeMap:
    def __init__(self):
        print("Makemap")

    # cheetah のログファイルを読む
    # cheetah log fileは自作フォーマット
    # 1行ごとに　フレーム番号とスコアが書いてある
    # linesはすべての行のリスト
    def read_cheetah_log(self, logname):
        # 一時的なリスト
        data_line=[]
        lines = open(logname,"r").readlines()
        # 1-2行目はヘッダー
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

        return data_line

    # Read cordinate log from Amane soft
    # あまねソフトのYZ座標が書いてあるやつ
    def read_coodrinate_log(self, logname):
        lines = open(logname,"r").readlines()
        code_map=[]
        for line in lines:
            cols=line.strip().split(",")
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

        return np_code_map

    def read_logs(self, cheetah_logs):
        # Reading each log from cheethah
        cheetah_logs.sort()
        allmap=[]
        filenamemap=[]
        for logfile in cheetah_logs:
            print("Processing %s"% logfile)
            # そもそもログファイル１個がスキャン１行に相当している
            # フレーム順にスコアが並んだリスト（各HD5ファイル）
            # Fast軸のフレーム数分ここにデータが入っている
            data_line=self.read_cheetah_log(logfile)
            # 二次元マップを積み上げていく
            allmap.append(data_line)
            filenamemap.append(logfile)

        np_map=np.array(allmap)
        print(np_map.shape)

        return np_map, filenamemap

    def merge_map_info(self, np_map, np_code_map, filename_map):
        print("Score map shape:",np_map.shape)
        (nv, nh, ndata) = np_map.shape

        # スポットの数とYZ座標を一緒に扱うためのマップ
        final_map=[]
        for i in range(0,nv):
            tmp_filename = filename_map[i]
            for j in range(0,nh):
                score=np_map[i][j][1]
                x,y=np_code_map[i][j]
                # Clickしたときに出てくるメッセージ
                message = "codes = %5.1f %5.1f score %5d : %s %d should be referred" % (x,y,score,tmp_filename, j+1)
                # nhは各行の中でどの位置のイメージ番号かを示している
                # adxvなどでイメージを見れると良い
                final_map.append((i,j,x,y,score,message))

        # マップをnumpy arrayに変換
        new_map=np.array(final_map)

        return new_map

    def prepMap(self, cheetah_logs, coordinate_log):
        # ログファイルを読み込む
        np_map,filenamemap=self.read_logs(cheetah_logs)
        # あまねログファイルを読み込む
        np_code_map=self.read_coodrinate_log(coordinate_log)
        # マップを結合する
        new_map=self.merge_map_info(np_map, np_code_map,filenamemap)

        # Pandas treatment
        # X,Y, Score という配列をPandas data frame へ変換
        df = pd.DataFrame.from_dict((new_map))
        #print(df)
        df.columns = ['h','v','Y_value','Z_value','score','message']
        df['score'] = pd.to_numeric(df['score'])
        df['Y_value'] = pd.to_numeric(df['Y_value'])
        df['Z_value'] = pd.to_numeric(df['Z_value'])
        df['h'] = pd.to_numeric(df['h'])
        df['v'] = pd.to_numeric(df['v'])
        df['message'] = df['message'].astype(str)

        return df

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
    # python2でprint
    print("Filename: %s" % filename_df.iloc[iy, ix])

def onclick(event):
    ix, iy = int(round(event.xdata)), int(round(event.ydata))
    # python2でprint
    print("Filename: %s" % filename_df.iloc[iy, ix])

fig, ax = plt.subplots()
sns.heatmap(pivot,cmap='RdBu')
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()