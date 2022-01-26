import os,sys
from scipy.optimize import leastsq
import numpy as np
from matplotlib import pyplot as plt


lines = open(sys.argv[1],"r").readlines()

radt = []
post = []
data =[]
obs = []
for line in lines:
    cols=line.split()
    degs = float(cols[0])
    rads = np.radians(degs)
    poss = float(cols[1])
    radt.append(rads)
    post.append(poss)
    data.append((degs,poss))

rada = np.array(radt)
data = np.array(post)

print(len(rada),len(data))

# 初期値が必要
# X,Z の値
params=[1,1]

# theta (radians)
def function(theta,params):
    x,z = params
    # radius
    r = np.sqrt(x*x+z*z)
    # theta 0
    theta0 = np.arctan(z/x)
    # distance on the microscope
    dist = r*np.sin(theta + theta0) - r*np.sin(theta0)

    return dist

# 残渣の計算
def residuals(params, data, theta):
    err = data - function(theta,params)
    return err

pbest = leastsq(residuals, params, args=(data,rada),full_output=1)
bestparams=pbest[0]
cov_x=pbest[1]

print(bestparams)
print(cov_x)

datafit = function(rada, bestparams)

plt.plot(rada, data, 'o')
plt.plot(rada, datafit)
plt.show()