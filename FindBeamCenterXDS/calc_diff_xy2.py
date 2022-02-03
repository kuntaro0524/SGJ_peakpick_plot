import os,sys
import numpy as np

# LOG LINE
# osc_295_0/beam_1132_1035/IDXREF.LP: UNIT CELL PARAMETERS     37.706    38.504   118.645 172.435   8.360 171.884

lines = open(sys.argv[1],"r").readlines()

for line in lines:
    #print(line)
    cols=line.split()
    cella=float(cols[4])
    cellb=float(cols[5])
    cellc=float(cols[6])

    alpha=float(cols[7])
    beta=float(cols[8])
    gamma=float(cols[9])

    diffa=np.fabs(cella-5.0)
    diffb=np.fabs(cellb-14.0)
    diffc=np.fabs(cellc-14.0)
    diff_alpha=np.fabs(alpha-90.0)
    diff_beta=np.fabs(beta-90.0)
    diff_gamma=np.fabs(gamma-90.0)
    diff_total = diffa + diffb+ diffc + diff_alpha + diff_beta + diff_gamma

    beam=line.split("/")[1].replace("beam_","")
    #print(beam)
    beam_param=beam.split("_")
    beamx=float(beam_param[0])
    beamy=float(beam_param[1])

    if diff_total < 20:
        print(beamx,beamy,diff_total,line.strip())
