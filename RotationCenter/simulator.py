import os,sys
import numpy as np
from matplotlib import pyplot as plt

# 回転中心を下流の顕微鏡カメラで覗いたときの左右の動きとX,Z座標の関係をシミュレートする
# 初期 X,Zの座標 [mm]
x = 4.0
z = 2.0

# これから計算できる原点からの距離
r = np.sqrt(x**2+z**2)
#print(r)

# このX,Zがピント方向となす角度
theta0 = np.arctan(z/x) # [rad.]

x=[]
y=[]
#こいつをハード的にdthetaずつ回したときの挙動
for theta_deg in range(0,360,5):
    dtheta = np.radians(theta_deg)
    d_dist = r*np.sin(theta0+dtheta) - r*np.sin(theta0) + np.random.rand(1)[0]
    x.append(theta_deg)
    y.append(d_dist)
    print(np.degrees(dtheta), d_dist)

xa=np.array(x)
ya=np.array(y)
plt.plot(xa,ya,'o-')
plt.show()