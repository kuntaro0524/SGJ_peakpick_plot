# encoding: utf-8
from typing import Any
import requests
import pandas as pd

class EIGER:
    def __init__(self):
        self.url = "http://192.168.91.202/data/"
        self.filewriter = "http://192.168.91.202/filewriter/api/1.8.0/files/"

        # curl command
        self.curl_com = "curl -X GET --header 'Content-Type: application/json' http://192.168.91.202/filewriter/api/1.8.0/files/"
    
    def getList(self):
        # self.curl_com の戻り値を取得
        response = requests.get(self.filewriter)
        listjson=response.json()

        # listjson からファイル名を取得
        filelist=listjson['value']
        
        return filelist

    def get(self):
        response = requests.get(self.url)
        # print(response)
        # response にはファイル名がリストで .html形式で書かれている
        # print(response.text)
        #print(response.content)
        #print(response.json())
        #print(response.headers)
        # print(response.status_code)
        # print(response.url)
        # print(response.encoding)
        #print(response.raw)
        # print(response.reason)
        # print(response.cookies)
        

        # responseをどうデコードするかを指定
        # print(response.json())

        if response.status_code == 200:
            # リクエストが成功した場合、応答から数値を取得します
            data = response.json()  # 応答データをJSON形式で取得します
            print(data)
            # 受け取ったJSONをPandas DataFrameに変換します
            # df = pd.DataFrame(data) 
            # print(df)
            
            #value = data['exp_raster']  # 応答データから必要な数値を取得します（'key'は実際のデータのキーに置き換えてください）
            #print("取得した数値:", value)
        else:
            # リクエストが失敗した場合のエラーハンドリング
            print("リクエストが失敗しました。ステータスコード:", response.status_code)

        return 1


eiger=EIGER()
filelist = eiger.getList()
for fn in filelist:
    print(fn)
