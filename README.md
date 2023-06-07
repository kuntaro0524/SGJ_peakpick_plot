# Analysis/ 
にあるスクリプトを利用してRaster scanの結果からデータ収集用の座標CSVを出力する
## プログラムを利用するための前提条件
+ scan/ディレクトリがある
+ イメージデータは .h5 である
+ .h5はスキャンの各行あたりに出力されている
+ coordinate.log 測定の際に出てくる座標(ゴニオ Y,Z 座標がスキャンの行ごとに１行情報がある)

## ディレクトリの構成の例
cytidine_window05_retry_01291531_line001_master.h5  cytidine_window05_retry_01291535_line022_master.h5  cytidine_window05_retry_01291539_line043_master.h5
cytidine_window05_retry_01291532_line002_master.h5  cytidine_window05_retry_01291535_line023_master.h5  cytidine_window05_retry_01291539_line044_master.h5
cytidine_window05_retry_01291532_line003_master.h5  cytidine_window05_retry_01291535_line024_master.h5  cytidine_window05_retry_01291539_line045_master.h5
....
....
....
cytidine_window05_retry_01291535_line021_master.h5  cytidine_window05_retry_01291539_line042_master.h5  cytidine_window05_retry_01291542_line063_master.h5

coordinate.log

## プログラムの使い方
find_h5_and_ana.sh を走らせたら以下のことを実施
+ ディレクトリの中に master .h5 があればリストを作成（行ごとにmasterファイルがあるので行数分ファイルがあるはず）（測定を停止した際は注意）
+ それぞれのファイルごとにcheetahを走らせて行ごとのスポットファインドログを作成する
    + スポットファインドログはmasterファイルのプレフィクスそのまま + ".log" というファイル名
    + このログファイルがあると解析は行わない　という仕様→これも要注意（解析が進まないなぁという場合、logの内容をチェックして必要なら削除すること）
+ １行毎に列座標があるが、これは coordinate.log 一行に相当しており、スキャンの結果とcoordinate.logはこのスクリプトの中で対応付けている
+ スポットファインドがリストの .h5 すべてで実施されたら、次に read_log.py が実施される
    + すべてのログファイルを読み込んでヒートマップを作成
    + 引数として　「ピークのしきい値」をとるのでスクリプト中でこの数値を変更することで「測定試料の数を決定」することもできる

## プログラムの出力ファイル
+ heatmap_original.png : すべてのスコアをそのまま入れてヒートマップを描いた図
+ heatmap_threshold.png: read_log.py の引数で指定したスコアのしきい値以上の点だけをヒートマップに描いた図
+ meas.csv : read_log.py でしきい値に設定したスコア以上を有する座標のみを .csv にしたもの
+ meas_all.csv: すべての座標を .csvファイルにしたもの（これを直接使うことはないが、編集して利用できることはあるかも）

## 使い方のコツ
+ うまくいけば find_h5_and_ana.sh をスキャンディレクトリで流して終了→meas.csvをoscillation測定に利用すれば良い
+ 失敗した場合
    + 例えば、何らかの理由で cheetah が失敗してしまったら、空の.logファイルができて、再計算がうまくいかなくなる(find_h5_and_ana.sh)
    + これに気づいたら .log を全部消してfind_h5_and_ana.shをやり直すのが楽
    + ただ、単純に「しきい値を変えて実行し直したい」みたいな場合には、read_log.py のみ実行するという手もある。
        + 該当するfind_h5_and_ana.sh の read_log.py の部分だけ実行すれば良い（.logファイルのリストを全解析して heatmapと CSVを作る）

# cheetah のパラメータチューン
現時点での設定（2023/06/07　13:56時点）
/oys/xtal/cheetah-eiger-zmq/eiger-zmq/bin/cheetah.local $hd5file --nproc=32 --params="cheetah.MinPixCount=4" --params="cheetah.MaxPixCount=20" --params="cheetah.MinSNR=1.9" > $logname

+ MinPixCount = 4
+ MaxPixCount = 20
+ MinSNR = 1.9

となっている。ピークのサイズによって MinPixCount, MaxPixCount。
ピークのSNRによって MinSNR を変更する必要がある。これは事前にシチジンのパラメータを調整した結果なので、タンパクだとどうなるか試したほうが良い。

## スクリプトのパス
find_h5_and_ana.sh は
+ cheetahのパス
+ read_log.py のパス
が正確に切れている必要があるので、必要に応じて find_h5_and_ana.sh を実行するディレクトリにコピーして内容を編集して利用するなどの工夫は必要

## cheetahのインストール
過去のcheetah関係のをインストールしようとすると多分はまる。
このcheetahはpybind11が入っていたら走るバージョンなので最新版をインストールしたら問題ない
### 手順
https://github.com/keitaroyam/cheetah/tree/eiger-zmq
+ Download ZIP。
+ ZIPファイルをunzipする。
+ yamtbx.python -mpip install pybind11
+ cd eiger-zmq/
+ yamtbx.python setup.py install
たぶんこれで走る(yamtbx.pythonは事前にインストールされている必要はある)