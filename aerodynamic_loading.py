import numpy as np
import scipy as sp
from scipy import interpolate

data = np.genfromtxt("MainWing_a=0.00_v=10.00ms.txt",skip_header=40,skip_footer=1030)

ylst = data[:,0]
chordlst = data[:,1]
Cllst = data[:,3]
Cdlst = data[:,5]
Cmlst = data[:,7]

aero_lst = (Cllst,Cdlst,Cmlst)

f_Cllst = sp.interpolate.interp1d(ylst,Cllst,kind='cubic',fill_value='extrapolate')

