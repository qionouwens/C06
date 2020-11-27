from aerodynamic_loading import force_distribution, angle_of_attack
from math import cos, sin, radians
import numpy as np
import scipy
from scipy import integrate
import matplotlib.pyplot as plt
from Constants_list import half_span, desired_cl

aoa = angle_of_attack(desired_cl)


def normal_force(y):
    lift, drag, _ = force_distribution(y, desired_cl, aoa)
    return lift*cos(radians(aoa))+sin(radians(aoa))*drag


def shear_force(y):
    add = 0
    Sin = -767926.5287 + 34501.01 * y - 318.645 * y ** 2
    if y <= 10.7:
        add = -71259.84
    return scipy.integrate.quad(normal_force, y, half_span)[0]+add+Sin


def moment(y):
    return scipy.integrate.quad(shear_force, y, half_span)[0]


y_values = np.linspace(0, half_span, 2000)
shear = []
moment_list = []
previous_shear = shear_force(0)
previous_y_value = 0
for y_value in y_values:
    shear.append(shear_force(y_value))
moment_list = scipy.integrate.cumtrapz(shear, y_values, initial=0)
moment_list = max(moment_list) - moment_list

plt.figure()
plt.subplot(211)
plt.plot(y_values, shear)

plt.subplot(212)
plt.plot(y_values, moment_list)
plt.show()

