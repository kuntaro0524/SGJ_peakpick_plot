import sys,os
import pandas as pd

# 絶対パスから２個上くらいのパスを取得する
abs_path = os.path.abspath("./")
path_parts = abs_path.split('/')
relative_path = ""
for p in path_parts[-2:]:
    relative_path = os.path.join(relative_path,p)

df = pd.read_csv(sys.argv[1])

# 行ごとに処理をしてCSVファイルを作成する
csv_name = "sokutei.csv"
csvfile = open(csv_name,"w")

for index,row in df.iterrows():
    #print(row['score'],row['Z_value'],row['Y_value'])
    int_z = int(row['Z_value'])
    int_y = int(row['Y_value'])
    int_score = int(row['score'])
    filename = "%s/osc_%s_%s.cbf" % (relative_path, int_z, int_y)
    csvfile.write("%s, %s, %s, %s\n" % (filename, int_score, int_y, int_z ));
