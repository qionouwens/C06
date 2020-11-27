from scipy import interpolate
from math import cos, radians
import numpy as np
import scipy
from scipy import integrate
import matplotlib.pyplot as plt
from Constants_list import half_span, desired_cl
from aerodynamic_loading import force_distribution, angle_of_attack, f_chord

y_values = np.linspace(0, half_span, 2000)

#fig, ax = plt.subplots()
#ax.plot(y_values, shear)
#plt.show()


aoa = angle_of_attack(desired_cl)

#TORSION DIAGRAMS

momentc_4 = []
for y_value in y_values:
    M = force_distribution(y_value, desired_cl, aoa)[2] + 0.1912*force_distribution(y_value, desired_cl, aoa)[0]*f_chord(y_value)
    momentc_4.append(M)

#Convert to a function

def conversion(moment):
    M_shear_centre_f = scipy.interpolate.interp1d(y_values, moment, kind='cubic', fill_value='extrapolate')
    return M_shear_centre_f

M_shear_centre_f = conversion(momentc_4)

#Integrate
Torsion = []

def Torsion_moment(y):
    Torsion_moment = scipy.integrate.quad(M_shear_centre_f, y, half_span)[0]
    return Torsion_moment
#THRUST

Thrust_t = cos(radians(27.87))*440550*1.525

for y_value in y_values:
    t = Torsion_moment(y_value)
    if y_value <= 10.965:
        T = t + Thrust_t
    else:
        T = t
    Torsion.append(T)

Cm_4 = []
for y_value in y_values:
    Cm_41 = force_distribution(y_value, desired_cl, aoa)[2]
    Cm_4.append(Cm_41)

#CONTRIBUTION OF INERTIAL FORCES
m_fuel = 59242.52

def inertial_f(m_fuel, y):
    func = 6178.26 - 14.22*y + (0.478 - 0.011*y)*m_fuel
    return func

W_en = 71259.84 #N

T_inertial = []

for y_value in y_values:
    T_section = inertial_f(m_fuel, y_value)*f_chord(y_value)*0.0588 #positive
    T_en = 71259.84*f_chord(10.965)*0.6412 #negative
    if y_value <= 10.965:
        T_in = T_section - T_en
    else:
        T_in = T_section
    T_inertial.append(T_in)

#ADD INERTIAL AND AERODYNAMIC
T_total = np.array(T_inertial) + np.array(Torsion)

fig=plt.figure()
fig.suptitle('Graphs')
plt.subplot(2,2,1)
plt.plot(y_values, T_inertial)
plt.title('Inertial Torsion')
plt.subplot(2,2,2)
plt.plot(y_values, momentc_4, 'tab:orange')
plt.title('Moment about shear centre')
plt.subplot(2,2,3)
plt.plot(y_values, T_total, 'tab:green')
plt.title('T total')
plt.subplot(2,2,4)
plt.plot(y_values, Torsion, 'tab:red')
plt.title('Torsion without inertial forces')


plt.show()