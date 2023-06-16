# encoding: utf-8
import time
import sys
from typing import Any
import requests
import pandas as pd
import urllib
import os
import EigerDL

eigerdl = EigerDL.EigerDL()

for i in range(100):
    prefix_list = eigerdl.getPrefixListOnServer()
    for prefix in prefix_list:
        eiger.normalProc(prefix, isRemove=False)
    time.sleep(600)
    print("GOTO NEXT CYCLE")