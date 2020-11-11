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

aero_lst = (Cllst,Cdlst,Cmlst)

f_chord = sp.interpolate.interp1d(ylst,chordlst,kind='cubic',fill_value='extrapolate')

aero_loading = [0,0,0]

c=0
for function in aero_lst:
    f = sp.interpolate.interp1d(ylst,function,kind='cubic',fill_value='extrapolate')
    
    F_per_span = f(ylst) * q * f_chord(ylst)

    aero_loading[c]= F_per_span
    
    c = c + 1


aero_lst = np.array(aero_lst).T #This array returns 3 columns: col 1 is the lift
                                #per unit span, col 2 the drag and col 3 the moment
