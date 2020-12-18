from math import sqrt, atan
from scipy import interpolate
from Constants_list import t_skin, t_spar, spar_location, x_mid_spar
import math
from aerodynamic_loading import f_chord
from Constants_list import half_span
from moment_of_inertia_wingbox import I_x
from Shear_Force_diagrams import moment_list
import numpy as np
import matplotlib.pyplot as plt
from wingbox_model import a, b, lng_lower, lng_upper



#Number of sections

n = 30

sp = half_span/n

#LIST OF PROGRESSIVE RIB PROP
n_stringers_up = 38
n_stringers_bm = 26
y_stringer = 5.555*10**(-3)
A_stringer = 6*10**(-4)
n_safety = 1.5
n_steps = 200
n_steps_section = int(2000/n)
nribs1 = list(range(31))
nribs = nribs1[1:]
C_r = 9.555
n_stringers_up_2 = 10
n_stringers_bm_2 = 10
n_stringers_up_3 = 4
n_stringers_bm_3 = 4



#Centroid with stringers


y_wo_stringers = - 0.008138957996105993
A_wo_stringers = ((b+a)*t_spar+(lng_lower+lng_upper)*t_skin)
A_stringers = A_stringer*(n_stringers_bm + n_stringers_up)
y_upper = 0.0585
y_lower = -0.04685
y_new = ((y_upper)*n_stringers_up*A_stringer + (y_lower)*n_stringers_bm*A_stringer + y_wo_stringers*A_wo_stringers)/(A_wo_stringers+A_stringers)

y_new_2 = ((y_upper)*n_stringers_up_2*A_stringer + (y_lower)*n_stringers_bm_2*A_stringer + y_wo_stringers*A_wo_stringers)/(A_wo_stringers+A_stringer*(n_stringers_bm_2+n_stringers_up_2))

y_new_3 = y_new_2 = ((y_upper)*n_stringers_up_3*A_stringer + (y_lower)*n_stringers_bm_3*A_stringer + y_wo_stringers*A_wo_stringers)/(A_wo_stringers+A_stringer*(n_stringers_bm_3+n_stringers_up_3))
# Distance from the centroid of furthest points on panels

distance_upper = 0.0633 - y_new
distance_lower = -0.0633 - y_new

distance_upper_2 = 0.0633 - y_new_2
distance_lower_2 = -0.0633 - y_new_2

distance_upper_3 = 0.0633 - y_new_3
distance_lower_3 = -0.0633 - y_new_3

d_upper = [distance_upper*f_chord(0)]
d_down = [distance_lower*f_chord(0)]
for i in nribs:
    if i < 10:
        d_upp = distance_upper*f_chord(i*sp)
        d_d = distance_lower*f_chord(i*sp)
        d_upper.append(d_upp)
        d_down.append(d_d)
    elif 10<= i < 20:
        d_upp = distance_upper_2*f_chord(i*sp)
        d_d = distance_lower_2*f_chord(i*sp)
        d_upper.append(d_upp)
        d_down.append(d_d)
    else:
        d_upp = distance_upper_3*f_chord(i*sp)
        d_d = distance_lower_3*f_chord(i*sp)
        d_upper.append(d_upp)
        d_down.append(d_d)

upper_stringer_distance = np.repeat(d_upper, n_steps_section)
lower_stringer_distance = np.repeat(d_down, n_steps_section)
print(upper_stringer_distance)
print(lower_stringer_distance)
#Moments of inertia
y_list_1 = np.linspace(0, 10, 10)
y_list_2 = np.linspace(10, 20, 10)
y_list_3 = np.linspace(20, 31.315, 10)
I_x_1 = []
for i in y_list_1:
    I = I_x(i, n_stringers_up, n_stringers_bm)
    I_x_1.append(I)
I_x_2 = []
for i in y_list_2:
    I2 = I_x(i, n_stringers_up_2, n_stringers_bm_2)
    I_x_2.append(I2)
I_x_3 = []
for i in y_list_3:
    I3 = I_x(i, n_stringers_up_3, n_stringers_bm_3)
    I_x_3.append(I3)


I_xxx = I_x_1 + I_x_2 + I_x_3
I_x_total = np.repeat(I_xxx, 67)[:2000]

My = [b*y for b,y in zip(moment_list, upper_stringer_distance)]
My2 = [b*y for b,y in zip(moment_list, lower_stringer_distance)]
stress = [-m/i for m, i in zip(My, I_x_total)]
stress2 = [m/i for m,i in zip(My2, I_x_total)]
print(stress)
print(stress2)
# Make lists of distances from centroids
with open("tensionnegative.txt", "w") as output:
    output.write(str(stress2))


Force_upper_stringers = [1.5 *b / m for b,m in zip(moment_list, upper_stringer_distance)]
Force_lower_stringers = [1.5*b / m for b,m in zip(moment_list, lower_stringer_distance)]



#Critical forces per section

steps = 2000/30

Cr_force = [(math.pi**2*4*68.9*10**9)*(t_skin)**2/(12*(1-0.33**2)*(0.5*f_chord(0)/n_stringers_up)**2)]
for i in nribs:
    if i < 10:
        stringer_spacing = (math.pi**2*4*68.9*10**9)*(t_skin)**2/(12*(1-0.33**2)*(0.5*f_chord(i)/(n_stringers_up-1))**2)
        Cr_force.append(stringer_spacing)
    elif 10 <= i <20:
        stringer_spacing = (math.pi ** 2 * 4 * 68.9 * 10 ** 9) * (t_skin) ** 2 / (12 * (1 - 0.33 ** 2) * (0.5 * f_chord(i) / (n_stringers_up_2-1)) ** 2)
        Cr_force.append(stringer_spacing)
    else:
        stringer_spacing = (math.pi ** 2 * 4 * 68.9 * 10 ** 9) * (t_skin) ** 2 / (12 * (1 - 0.33 ** 2) * (0.5 * f_chord(i) / (n_stringers_up_3-1)) ** 2)
        Cr_force.append(stringer_spacing)

Cr_FORCES = np.repeat(Cr_force, n_steps_section)[:2000]
print(Cr_FORCES)
y_values = np.linspace(0, half_span, 2000)

safety_margin = [a/b for a,b in zip(Cr_FORCES[:-200], stress[:-200])]
print(safety_margin)
#GRAPHS
plt.title("Margin of Safety")
plt.subplot(1, 2, 1)
plt.plot(y_values, Cr_FORCES, label = "Critical stress", color = "orange")
plt.plot(y_values, stress, label = "Applied stress, bottom panel", color = "royalblue")
plt.xlabel("Distance along the wingspan [m]")
plt.ylabel("Stress [Pa]")
plt.subplot(1,2,2)
plt.plot(y_values, stress2, label = "Applied stress, tension", color = "darkturquoise")
plt.plot(y_values, stress, label = "Applied stress, compression", color = "royalblue")
plt.xlabel("Distance along the wingspan [m]")
plt.ylabel("Stress [Pa]")
plt.plot(y_values[:-200], safety_margin, color = "royalblue")
plt.xlabel("Distance along the wingspan [m]")
plt.legend()
plt.show()

