from aerodynamic_loading import force_distribution, angle_of_attack
from math import cos, sin, radians
import numpy as np
import scipy
from scipy import integrate
import matplotlib.pyplot as plt

half_span = 31.315
desired_cl = 0.5
aoa = angle_of_attack(desired_cl)


def normal_force(y):
    lift, drag, moment = force_distribution(y, desired_cl)
    return lift*cos(radians(aoa))+sin(radians(aoa))*drag


def shear_force(y):
    return scipy.integrate.quad(normal_force, y, half_span)[0]


y_values = np.linspace(0, half_span, 200)
shear = []
for y_value in y_values:
    shear.append(shear_force(y_value))

fig, ax = plt.subplots()
ax.plot(y_values, shear)
plt.show()
