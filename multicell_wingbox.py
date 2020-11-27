# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 09:41:51 2020

@author: basti
"""
import numpy as np
from wingbox_model import e, f, d, g, x_mid_spar, lng_mid_spar as s, h
from wingbox_model import upper, lower, a, b, x_values, y_1, y_2
from Constants_list import t_skin, t_spar, x_mid_spar

G = 26E9 #AL6061-T6
A_left = 1/2*(s+b)*h
A_right = 1/2*(s+a)*h


#row 1
q1_coefficient = 1/(2*A_left*G) * (s/t_spar + d/t_skin + b/t_spar + g/t_skin)
q2_coefficient = 1/(2*A_left*G) * (-s/t_spar)

#row 2
q1_coefficient_2 = 1/(2*A_right*G) * (-s/t_spar)
q2_coefficient_2 = 1/(2*A_right*G) * (a/t_spar + e/t_skin + s/t_spar + f/t_skin)

matrix = np.array([[q1_coefficient, q2_coefficient, 1],
                  [q1_coefficient_2, q2_coefficient_2, 1],
                  [2*A_left,2*A_right,0]])
rhs = np.array([0,0,5])

solution = np.linalg.solve(matrix,rhs)