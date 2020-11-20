from wingbox_model import x_values, y_2, h, t_skin, t_spar, a, b, x_bar, y_bar, lng_upper,lng_lower, upper, lower, beta_upper, beta_lower
from aerodynamic_loading import f_chord
from math import sin
import numpy as np



height_stringer = 20 #1/skin_thickness

### moment of inertia computations
A = 1/12 * t_spar * b**3 + (b*t_spar)*((y_2[0] - b/2)-y_bar)**2 
B = 1/12 * t_spar * a**3 + (a*t_spar)*((y_2[1] - a/2)-y_bar)**2
C = (t_skin * lng_upper**3 * (sin(beta_upper)**2)) / 12 + (lng_upper)*t_skin * (upper(0.45)-y_bar)**2
D = (t_skin * lng_lower**3 * (sin(beta_lower)**2)) / 12 + (lng_lower)*t_skin * (lower(0.45)-y_bar)**2


## stringer placement upper skin##
stringer_area = (2*t_skin)**2 * height_stringer

def I_x(y,n_stringers_upper,n_stringers_lower):
    z_str = []
    x_str = []
    skins = [[upper,n_stringers_upper],[lower,n_stringers_lower]]
    for n in skins:
        x = np.linspace(x_values[0],x_values[1],n[1])
        z = (n[0](x)-y_bar)
        x_str.append(x)
        z_str.append(z)
        steiner = stringer_area*z**2
        I_induced = np.sum(steiner)
        
    return (A+B+C+D)*f_chord(y)**3 +I_induced*float(f_chord(y))**2, x_str, z_str


