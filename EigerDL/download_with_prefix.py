# encoding: utf-8
import EigerDL
import time
import sys

eigerdl = EigerDL.EigerDL()

# prefix 
prefix = sys.argv[1]

# ３回ループ
for i in range(3):
    eigerdl.normalProc(prefix, isRemove=False)
