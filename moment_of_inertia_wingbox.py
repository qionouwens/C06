from wingbox_model import x_values, y_1, y_2, h, t, a, b, x_bar, y_bar, spar_location, lng_upper,lng_lower, upper, lower, beta_upper, beta_lower
from aerodynamic_loading import f_chord
from math import sin, cos
import numpy as np
import pdb


### moment of inertia computations
A = 1/12 * t * b**3 + (b*t)*((y_2[0] - b/2)-y_bar)**2 
B = 1/12 * t * a**3 + (a*t)*((y_2[1] - a/2)-y_bar)**2
C = (t * lng_upper**3 * (sin(beta_upper)**2)) / 12 + (lng_upper)*t * (upper(0.45)-y_bar)**2
D = (t * lng_lower**3 * (sin(beta_lower)**2)) / 12 + (lng_lower)*t * (lower(0.45)-y_bar)**2


## stringer placement upper skin##
stringer_area = (2*t)**2 * 20

def I_x(y,n_stringers_upper,n_stringers_lower):
    skins = [[upper,n_stringers_upper],[lower,n_stringers_lower]]
    for n in skins:
        x = np.linspace(x_values[0],x_values[1],n[1])
        z = (n[0](x)-y_bar)*float(f_chord(y))

        steiner = stringer_area*z**2
        I_induced = np.sum(steiner)
        
    return (A+B+C+D)*f_chord(y)**3 #+I_induced

E = (b*t)*(spar_location[1]-x_bar)**2
F = (b*t)*(spar_location[0]-x_bar)**2
G = (t * lng_upper**3 * (cos(beta_upper)**2)) / 12 + (lng_upper)*t * ((spar_location[1]-spar_location[0])-x_bar)**2
H = (t * lng_lower**3 * (cos(beta_lower)**2)) / 12 + (lng_lower)*t * ((spar_location[1]-spar_location[0])-x_bar)**2

I_yy = (E+F+G+H)


