import numpy as np
from aerodynamic_loading import f_chord
from wingbox_model import a as aft,b as front,I_polar, lng_upper, lng_lower

dihedral = 5#deg
cr = 9.555 #m
ct = 2.972 #m
tc = 0.14
b = 62.63 #m

y_range = np.arange(0,b/2,0.001)

# INPUTS IN METERS

def front_spar(y):
    return front * f_chord(y)

def aft_spar(y):
    return aft * f_chord(y)

def upper(y):
    return lng_upper * f_chord(y)

def lower(y):
    return lng_lower * f_chord(y)

#def I_y(y):
#    return I_yy * f_chord(y)**3

def J(y):
    return I_polar * f_chord(y)**3

