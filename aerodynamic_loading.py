import numpy as np

data = np.genfromtxt("MainWing_a=0.00_v=10.00ms.txt",skip_header=40,skip_footer=1030)

ylst = data[:,0]
Cllst = data[:,3]
Cdlst = data[:,5]
Cmlst = data[:,7]

