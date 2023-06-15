# manual

１．ピークサーチをするスクリプト
simple_peaksearch.sh -> 走らせる。.h5への相対パスをheaderに書いてから走らせる

走らせて終わるまで待つ。96 x 96 framesで5min程度かかる（PCの性能依存）

２．終わったらマップを描くスクリプトを走らせる
plot_results.py -> Gather .log information -> make 3D map plot -> make measurement csv.

[usage]
> python plot_results.py ../ 3.0

score threshold : 第二引数で指定(float)
好みによって、oscillation.csvを編集するのでも良い。