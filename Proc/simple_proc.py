import os
import numpy as np
import pandas as pd
import glob
import subprocess

# file list
data_root = "../"
h5files = glob.glob("%s/*master.h5"%data_root)

# XDS template pathes
xds_template_file = "/data01/SGJ/220128-BL19XU/Scripts/Proc/XDS.INP.220129.ver1.1"

def divideDirName(h5name):
    undiv_cols = h5name.split('_')
    # Data collection coordinate(y,z on the goniometer)
    gy = int(undiv_cols[1])
    gz = int(undiv_cols[2])
    # Directory name
    prefix=h5name.split("/")[-1].replace("_master.h5","")
    return(gy,gz,prefix)

def makeProcDir(prefix):
    # make directory with 'prefix' as it is
    if os.path.exists(prefix)==False:
        print("making a directory")
        os.makedirs(prefix)
        absdir = os.path.abspath(prefix)
    else:
        print("already exists!")
        absdir = os.path.abspath(prefix)
    
    return absdir

def prepProc(proc_abs,prefix):
    # XDS.INP for this beam XY coordinates
    new_xdsinp_path=os.path.join(proc_abs, "XDS.INP")
    new_xdsinp = open(new_xdsinp_path, "w")
    xds_lines = open(xds_template_file, "r").readlines()
    new_lines=[]
    for xds_line in xds_lines:
        if "QQQQQQ" in xds_line:
            data_relative_path = "../../%s_??????.h5" % prefix
            xds_line = xds_line.replace("QQQQQQ", data_relative_path)
        new_xdsinp.write("%s"%xds_line)

for fi in h5files:
    gy,gz,prefix=divideDirName(fi)
    proc_abs=makeProcDir(prefix)
    
    prepProc(proc_abs,prefix)
    print("Data processing in %s" % proc_abs)
    subprocess.run("xds", cwd=proc_abs)
