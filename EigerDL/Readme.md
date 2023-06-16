K.Hirata 2023/06/16 14:40
> python download_eiger.py

このコマンドでサーバー上にあるファイルを順次取得することが可能。

+ このコマンドで現時点でサーバー上にあるファイルリストを取得
+ masterファイルのprefixをリストにする
+ prefixごとにディレクトリを作成(scan/も作成）
+ どのディレクトリにデータをダウンロード
+ ダウンロードが完了したらそのファイルを削除
+ というのを延々と繰り返す

Ueno, Nov2021 at BL19XU

Usage of download script.
 At current directory, issue following command, where DirName is directory name of data destination.
 ./download.sh  DirName

Usage of clear script, to clear the DUC data buffer.
 ./clear.sh
