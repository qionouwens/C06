from moment_of_inertia_wingbox import I_x
from Shear_Force_diagrams import moment_list, y_values
from Constants_list import upper_stringers, lower_stringers, young_modulus, shear_modulus
from Torsion import T_total
from wingbox_spanwise import J
import numpy as np
import scipy as sp
from scipy import integrate
import matplotlib.pyplot as plt
from math import degrees

moment_of_inertia_list = []
for y_value in y_values:
    moment_of_inertia_list.append(I_x(y_value, upper_stringers, lower_stringers))
moment_of_inertia_list = np.array(moment_of_inertia_list)

to_be_integrated = moment_list/(young_modulus*moment_of_inertia_list)

to_be_integrated = sp.integrate.cumtrapz(to_be_integrated, y_values, initial=0)
deflection = sp.integrate.cumtrapz(to_be_integrated, y_values, initial=0)

plt.plot(y_values, deflection)
plt.show()

polar_moment_of_inertia = []
for y_value in y_values:
    polar_moment_of_inertia.append(J(y_value))
polar_moment_of_inertia = np.array(polar_moment_of_inertia)

to_be_integrated = T_total/(shear_modulus*polar_moment_of_inertia)
twist = sp.integrate.cumtrapz(to_be_integrated, y_values, initial=0)
final_twist = []
for value in twist:
    final_twist.append(degrees(value))

plt.plot(y_values, final_twist)
plt.show()
