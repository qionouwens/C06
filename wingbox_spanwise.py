import numpy as np
from aerodynamic_loading import f_chord
from wingbox_model import a as aft,b as front, I_xx, I_yy

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

def I_x(y):
    return I_xx * f_chord(y)**3

def I_y(y):
    return I_yy * f_chord(y)**3

