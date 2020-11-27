from wingbox_model import x_values, y_2, h, t_skin, t_spar, a, b, x_bar, y_bar, lng_upper,lng_lower, upper, lower, beta_upper, beta_lower
from aerodynamic_loading import f_chord
from math import sin
from Constants_list import height_stringer
import numpy as np


### moment of inertia computations
A = 1/12 * t_spar * b**3 + (b*t_spar)*((y_2[0] - b/2)-y_bar)**2 
B = 1/12 * t_spar * a**3 + (a*t_spar)*((y_2[1] - a/2)-y_bar)**2
C = (t_skin * lng_upper**3 * (sin(beta_upper)**2)) / 12 + (lng_upper)*t_skin * (upper(0.45)-y_bar)**2
D = (t_skin * lng_lower**3 * (sin(beta_lower)**2)) / 12 + (lng_lower)*t_skin * (lower(0.45)-y_bar)**2


### moment of inertia of the mid spar
E = 1/12 * t_spar *s**3 + (s*t_spar)*(upper(x_mid_spar - s/2)-y_bar)**2

## stringer placement upper skin##
stringer_area = (2*t_skin)**2 * height_stringer

def I_x(y,n_stringers_upper,n_stringers_lower):
    skins = [[upper,n_stringers_upper],[lower,n_stringers_lower]]
    for n in skins:
        x = np.linspace(x_values[0],x_values[1],n[1])
        z = (n[0](x)-y_bar)*float(f_chord(y))

        steiner = stringer_area*z**2
        I_induced = np.sum(steiner)
        
    return (A+B+C+D)*f_chord(y)**3 + I_induced

def I_x_multicell(y,n_stringers_upper,n_stringers_lower):
    without_spar = I_x(y,n_stringers_upper,n_stringers_lower)
    
    if y <= 5:
        return without_spar + E*f_chord(y)**3
    else:
        return without_spar

def plot():
    ys = np.arange(0.0,31.325,0.01)
    I = []
    for y in ys:
        Is = I_x_multicell(y,0,0)
        I.append(Is)
    plt.plot(ys,I)
    plt.show()

