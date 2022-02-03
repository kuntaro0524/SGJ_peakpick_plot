import scipy.spatial as ss                                      
from random import random
from matplotlib import pyplot as plt


# meas.csv read
lines = open("meas.csv","r").readlines()

arr=[]
for line in lines[1:]:
    print(line)
    cols=line.split(",")
    y=float(cols[1])
    z=float(cols[2])
    arr.append((y,z))

print(arr)

# データ数
N = 10000
# (x座標, y座標)のデータリスト
data = [(random()*100, random()*100) for _ in range(N)]
# kd tree の作成 (leafsizeは展開をしない節内点数上限)
tree = ss.KDTree(data, leafsize=10)

