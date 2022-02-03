import os,sys
import numpy as np
import pandas as pd
import glob
import subprocess

# file list
list_file = sys.argv[1]
lines=open(list_file,"r").readlines()

h5files=[]
for line in lines:
    h5files.append(line.strip())

# XDS template pathes
# Beam center from gridsearch03
xds_template_file = "/isilon/users/khirata/khirata/SGJ/Scripts/Proc/XDS.TEMPLATE.220201"
# Beam center from gridsearch03 & provided pre-known unit cell parameters
#xds_template_file = "/isilon/users/khirata/khirata/SGJ/Scripts/Proc/XDS.TEMPLATE.220201.cell"

def getPrefix(h5name):
    undiv_cols = h5name.split('_')
    # Directory name
    prefix=h5name.split("/")[-1].replace("_master.h5","")
    return(prefix)

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
    # different beam center directory
    makeProcDir(to_be_made)
    # XDS.INP for this beam XY coordinates
    new_xdsinp_path=os.path.join(to_be_made, "XDS.INP")
    replaceBeamXY(prefix, new_xdsinp_path, beam_xds_template, beamx, beamy)

    return to_be_made

def makeXDSINP(prefix, new_xdsinp):
    new_xdsinp = open(new_xdsinp, "w")
    xds_lines = open(xds_template_file, "r").readlines()
    new_lines=[]
    for xds_line in xds_lines:
        # JOB controls
        if "JOB=" in xds_line:
            continue
        # Path
        if "QQQQQQ" in xds_line:
            data_relative_path = "../../%s_??????.h5" % prefix
            xds_line = xds_line.replace("QQQQQQ", data_relative_path)
        new_xdsinp.write("%s"%xds_line)

    # JOB control in the last line
    new_xdsinp.write("JOB= DEFPIX INTEGRATE CORRECT\n")

def prepSGEcom(final_proc_path):
    xds_com_path = os.path.join(final_proc_path,"xds.sh")
    xds_file_writer = open(xds_com_path, "w")
    xds_file_writer.write("#!/bin/bash\n")
    xds_file_writer.write("#$ -wd %s\n" % final_proc_path)
    xds_file_writer.write("#$ -o %s\n" % final_proc_path)
    xds_file_writer.write("#$ -e %s\n"% final_proc_path)
    xds_file_writer.write("xds_par\n")
    xds_file_writer.close()

    os.system("chmod 744 %s" % xds_com_path)
    return xds_com_path

for fi in h5files:
    prefix = getPrefix(fi)
    proc_abs=makeProcDir(prefix)
    new_xdsinp = os.path.join(proc_abs, "XDS.INP")
    makeXDSINP(prefix, new_xdsinp)
    print("Data processing in %s" % proc_abs)
    compath = prepSGEcom(proc_abs)
    #subprocess.run("qsub %s" % compath, cwd=final_proc_path)
    os.system("qsub %s" % compath)
