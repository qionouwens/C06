import numpy as np
import scipy as sp
from scipy import interpolate

data = np.genfromtxt("MainWing_a=0.00_v=10.00ms.txt",skip_header=40,skip_footer=1030)

ylst = data[:,0]
chordlst = data[:,1]
Cllst = data[:,3]
Cdlst = data[:,5]
Cmlst = data[:,7]

V = 10 # m/s
rho = 1.225 # kg/m^3
S = 392.3 # m^2

q = 1/2 * rho * V**2 * S

f_chord = sp.interpolate.interp1d(ylst,chordlst,kind='linear',fill_value='extrapolate')
Cl_f = sp.interpolate.interp1d(ylst,Cllst,kind='cubic',fill_value='extrapolate')
Cd_f = sp.interpolate.interp1d(ylst,Cdlst,kind='cubic',fill_value='extrapolate')
Cm_f = sp.interpolate.interp1d(ylst,Cmlst,kind='cubic',fill_value='extrapolate')
functions = [Cl_f,Cd_f,Cm_f]

# ALL FUNCTIONS ARE PER UNIT SPAN

def localload(y):
    loading = []
    for function in functions:
        load = float(function(y)* q * f_chord(y))
        loading.append(load)
    return loading
    
    



    


