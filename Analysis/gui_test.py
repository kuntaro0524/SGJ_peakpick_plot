# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# グリッドサイズ
grid_size = 10

# 仮のスコアとファイル名を生成
data = np.zeros((grid_size, grid_size), dtype=[('x', 'i4'), ('y', 'i4'), ('score', 'f4'), ('filename', 'U10')])

for x in range(grid_size):
    for y in range(grid_size):
        score = np.random.random() # ランダムなスコア
        filename = "file_%s_%s" % (x, y) # ファイル名
        data[x, y] = (x, y, score, filename)

# スコアだけの配列を作成
scores = data['score']

# ヒートマップを描画
plt.imshow(scores, cmap='hot', interpolation='nearest', origin='upper')
plt.colorbar()
plt.show()

def onclick(event):
    ix, iy = int(round(event.xdata)), int(round(event.ydata))
    #print(f"Score: {data[ix, iy]['score']}, Filename: {data[ix, iy]['filename']}")
    print("score: %s, filename: %s" % (data[ix, iy]['score'], data[ix, iy]['filename']))

fig, ax = plt.subplots()
ax.imshow(scores, cmap='hot', interpolation='nearest', origin='upper')
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
