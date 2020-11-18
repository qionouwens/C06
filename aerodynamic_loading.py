import numpy as np
import scipy as sp
from scipy import interpolate
from math import asin, sin, radians, degrees

data_0 = np.genfromtxt("MainWing_a=0.00_v=10.00ms.txt", skip_header=40, skip_footer=1030)
data_10 = np.genfromtxt("MainWing_a=10.00_v=10.00ms.txt", skip_header=40, skip_footer=1030)

ylst = data_0[:, 0]
chordlst = data_0[:, 1]
f_chord = sp.interpolate.interp1d(ylst, chordlst, kind='linear', fill_value='extrapolate')

V = 10 # m/s
rho = 1.225  # kg/m^3
S = 392.3  # m^2

q = 1 / 2 * rho * V ** 2 * S


def process_data(data):

    Cllst = data[:, 3]
    Cdlst = data[:, 5]
    Cmlst = data[:, 7]

    Cl_f = sp.interpolate.interp1d(ylst, Cllst, kind='cubic', fill_value='extrapolate')
    Cd_f = sp.interpolate.interp1d(ylst, Cdlst, kind='cubic', fill_value='extrapolate')
    Cm_f = sp.interpolate.interp1d(ylst, Cmlst, kind='cubic', fill_value='extrapolate')
    functions = [Cl_f, Cd_f, Cm_f]

    return functions


functions_0 = process_data(data_0)
functions_10 = process_data(data_10)

total_cl_0 = 0.508651
total_cl_10 = 1.345901

total_cd_0 = 0.008158
total_cd_10 = 0.055607

total_cm_0 = -0.702886
total_cm_10 = -1.73102

total_0 = [total_cl_0, total_cd_0, total_cm_0]
total_10 = [total_cl_10, total_cd_10, total_cm_10]


def cl_distribution(desired_cl, y):
    cl_0 = functions_0[0]
    cl_10 = functions_10[0]
    return cl_0(y) + ((desired_cl-total_cl_0)/(total_cl_10-total_cl_0))*(cl_10(y)-cl_0(y))


def angle_of_attack(desired_cl):
    return degrees(asin((desired_cl-total_cl_0)/(total_cl_10-total_cl_0)*sin(radians(10))))


def drag_distribution(aoa, y):
    interpolation = sin(radians(aoa))/sin(radians(10))
    cd_0 = functions_0[1]
    cd_10 = functions_10[1]
    return cd_0(y)+interpolation*(cd_10(y)-cd_0(y))


def moment_distribution(aoa, y):
    interpolation = sin(radians(aoa)) / sin(radians(10))
    cm_0 = functions_0[2]
    cm_10 = functions_10[2]
    return cm_0(y) + interpolation * (cm_10(y) - cm_0(y))


# ALL FUNCTIONS ARE PER UNIT SPAN
def force_distribution(y, desired_cl, aoa):
    chord_q = f_chord(y) * q
    L = float(cl_distribution(desired_cl,y) * chord_q)
    D = float(drag_distribution(aoa,y) * chord_q)
    M = float(moment_distribution(aoa,y) * chord_q)
    
    loading = [L,D,M]

    return loading


