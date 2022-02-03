import os,sys
import numpy as np

lines = open(sys.argv[1],"r").readlines()

for line in lines:
    print(line)
    cols=line.split()
    cella=float(cols[4])
    cellb=float(cols[5])
    cellc=float(cols[6])

    diffa=np.fabs(cella-5.0)
    diffb=np.fabs(cellb-14.0)
    diffc=np.fabs(cellc-14.0)
    diff_total = diffa + diffb+ diffc
    #print(cella,cellb,cellc)

    beam=line.split("/")[0]
    beam_param=beam.split("_")
    beamx=float(beam_param[0])
    beamy=float(beam_param[1])

    if diff_total < 10:
        print(beamx,beamy,diff_total)
