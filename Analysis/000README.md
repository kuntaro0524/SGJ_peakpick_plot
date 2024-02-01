# manual(古い情報)

１．ピークサーチをするスクリプト
simple_peaksearch.sh -> 走らせる。.h5への相対パスをheaderに書いてから走らせる

走らせて終わるまで待つ。96 x 96 framesで5min程度かかる（PCの性能依存）

２．終わったらマップを描くスクリプトを走らせる
plot_results.py -> Gather .log information -> make 3D map plot -> make measurement csv.

[usage]
> python plot_results.py ../ 3.0

score threshold : 第二引数で指定(float)
好みによって、oscillation.csvを編集するのでも良い。

# 240131（平田記述）
１．ピークサーチをするスクリプト
simple_peaksearch.sh -> 走らせる。.h5への相対パスをheaderに書いてから走らせる
走らせて終わるまで待つ。96 x 96 framesで5min程度かかる（PCの性能依存）

２．終わったらマップを描くスクリプトを走らせる
python make_csv_from_scan5.py

CSV fileが出力されるのでこれを測定に利用する（GUIで読み込めるフォーマットに調整した気がしますが自信はない）

# 240201 (K. Hirata)
Confiremd.
>> run 'find_h5_and_ana.sh'

1. H5 processing
coordinate.log を探して処理を実行する。
coordinate.logが含まれるパスにある master.h5 を検出する。
master.h5ごとにピークサーチを実施する。
ピークサーチのパラメタはハードコードしてあるので注意。
解析の結果はログファイルに出力される。
ファイルのprefixと同じログファイルが出されるので、以降はそれがあれば「すでに処理されたもの」として扱われるので注意が必要。

2. Making a map picture and csv file.
ピークサーチの結果を集めてマップを作成する。
python $script_path/read_log.py 10
としてある。
第二引数はスコアの閾値。これより低いスコアのピークは無視される。

read_log.py

が実行されている。
この中で、１で解析した結果を集めて二次元マップを描く。
さらにデータ収集をするべき座標をあまね方式で出力する。
CSVファイルを好みの方法で出力したい場合にはこれを編集すべき。

2024/02/01　9:16　時点のコードはGithubに保管してあるのでローカルなファイルは編集しても削除しても復旧可能。ご自由においじりください。
