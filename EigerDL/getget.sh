#!/bin/bash

# 引数からデータ名を取得し、対応するディレクトリを作成します
data_name=$1
mkdir -p "${data_name}/scan"

while true; do
  # Pythonスクリプトを実行してファイルリストを取得します
  files=$(python eiger_communicate.py)

  # 各ファイルをダウンロードします
  for file in $files; do
    # URLからファイル名を取得します
    filename=$(basename "$file")

    # ファイルがすでに存在しない場合のみダウンロードします
    if [[ ! -f "${data_name}/scan/$filename" ]]; then
      wget -P "${data_name}/scan" "$file"
    fi
  done

  # 30秒待ちます
  sleep 30
done
