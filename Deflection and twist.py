from moment_of_inertia_wingbox import I_x
from Shear_Force_diagrams import moment_list, y_values
from Constants_list import upper_stringers, lower_stringers, young_modulus
import numpy as np
import scipy as sp
from scipy import integrate
import matplotlib
import matplotlib.pyplot as plt

moment_of_inertia_list = []
for y_value in y_values:
    moment_of_inertia_list.append(I_x(y_value, upper_stringers, lower_stringers))
moment_of_inertia_list = np.array(moment_of_inertia_list)

to_be_integrated = moment_list/(young_modulus*moment_of_inertia_list)

to_be_integrated = sp.integrate.cumtrapz(to_be_integrated, y_values, initial=0)
print(to_be_integrated)
deflection = sp.integrate.cumtrapz(to_be_integrated, y_values, initial=0)

plt.plot(deflection)
plt.show()
