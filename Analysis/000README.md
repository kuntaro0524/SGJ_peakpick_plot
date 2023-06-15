# manual

１．ピークサーチをするスクリプト
simple_peaksearch.sh -> 走らせる。.h5への相対パスをheaderに書いてから走らせる

走らせて終わるまで待つ。96 x 96 framesで5min程度かかる（PCの性能依存）

２．終わったらマップを描くスクリプトを走らせる
plot_results.py -> Gather .log information -> make 3D map plot -> make measurement csv.

score threshold : 3 以上のものをCSVファイルに書き出す(oscillation.csv)
threshold は ハードコード。適宜修正。
もしくはoscillation.csvを編集しても良いかと。

