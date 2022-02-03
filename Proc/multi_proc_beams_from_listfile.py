import os,sys
import numpy as np
import pandas as pd
import glob
import subprocess

# file list
file_list_file = sys.argv[1]
lines = open(file_list_file,"r").readlines()
h5files = []
for line in lines:
    h5files.append(line.strip())

# h5files = glob.glob("%s/*master.h5"%data_root)

# XDS template pathes
beam_xds_template = "/data01/SGJ/220128-BL19XU/Scripts/Proc/XDS.TEMPLATE"

# Beam x range
beam_ox = 1026
beam_oy = 1033

beam_xs = np.arange(beam_ox-10, beam_ox+10.1,5)
beam_ys = np.arange(beam_oy-10, beam_oy+10.1,5)

# Divide filename to 'directory name' and so on

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

def prepProc(proc_abs,prefix, beamx, beamy):
    # different beam center directory
    beamxy_proc_dir = "beam_%s_%s" % (beamx,beamy)
    to_be_made = os.path.join(proc_abs, beamxy_proc_dir)
    makeProcDir(to_be_made)
    # XDS.INP for this beam XY coordinates
    new_xdsinp_path=os.path.join(to_be_made, "XDS.INP")
    replaceBeamXY(prefix, new_xdsinp_path, beam_xds_template, beamx, beamy)

    return to_be_made

def replaceBeamXY(prefix, new_xdsinp, xds_template_file, beamx, beamy):
    new_xdsinp = open(new_xdsinp, "w")
    xds_lines = open(xds_template_file, "r").readlines()
    new_lines=[]
    for xds_line in xds_lines:
        if "ORGX" in xds_line:
            new_xdsinp.write("ORGX=%d\n"%beamx)
            new_xdsinp.write("ORGY=%d\n"%beamy)
            continue
        elif "ORGY" in xds_line:
            continue
        # Path
        if "QQQQQQ" in xds_line:
            data_relative_path = "../../../%s_??????.h5" % prefix
            xds_line = xds_line.replace("QQQQQQ", data_relative_path)
        new_xdsinp.write("%s"%xds_line)

print(beam_xs, beam_ys)

for fi in h5files:
    gy,gz,prefix = divideDirName(fi)

    for beamx in beam_xs:
        for beamy in beam_ys:
            print(prefix)
            proc_abs=makeProcDir(prefix)
            final_proc_path = prepProc(proc_abs,prefix, beamx, beamy)
            print("Data processing in %s" % final_proc_path)
            subprocess.run("xds", cwd=final_proc_path)
