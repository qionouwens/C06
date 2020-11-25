import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, sin, atan, cos
import scipy as sp
from scipy import interpolate
from Constants_list import t_skin as t_sk, t_spar as t_sp, spar_loc

data = np.genfromtxt('sc20714.txt',skip_header=1)
x = data[:,0]
y = data[:,1]

spar_location = spar_loc
t_skin = t_sk
t_spar = t_sp

x_values = spar_location
y_1 = [-0.0633,-0.0304]
y_2 = [0.0633,0.0537]

b = (y_2[0]-y_1[0])
a = (y_2[1]-y_1[1])
c = y_2[0] - y_2[1]
h = x_values[1]-x_values[0]


# numerical integration
upper = sp.interpolate.interp1d(x_values, y_2, kind='linear',fill_value='extrapolate')
lower = sp.interpolate.interp1d(x_values, y_1, kind='linear',fill_value='extrapolate')

lng_upper = sqrt((x_values[0]-x_values[1])**2 + (y_2[0]-y_2[1])**2)
lng_lower = sqrt((x_values[0]-x_values[1])**2 + (y_1[0]-y_1[1])**2)

beta_upper = atan((y_2[0]-y_2[1])/0.5)
beta_lower = atan((-y_1[0]+y_1[1])/0.5)


dx = t_skin
dA = dx**2


xs = np.arange(0.2,0.701,dx)

sum_Q = 0
count = 0
go = True

while go:
    
    for xi in xs:
        sum_Q = sum_Q + float(upper(xi))*dA
        count += 1

    for xi in xs:
        sum_Q = sum_Q + float(lower(xi)) *dA
        count += 1

    go = False
    
y_bar = (sum_Q + b * t_spar * 0 + a * t_spar * a/2)/((b+a)*t_spar+(lng_lower+lng_upper)*t_skin)

x_bar = 0.2 + ((lng_upper + lng_lower)*t_skin * 0.25 + 0.5 * a * t_skin) / ((b+a)*t_spar+(lng_lower+lng_upper)*t_skin)


I_polar = 4 * ((a+b)/2 * h)**2 / ((a+b)/t_spar+(lng_upper+lng_lower)/t_skin)

# Uncomment to plot the cross section of the wing box ##

#plt.plot(x,y)
#plt.vlines(0.2,-0.0633,0.0633,color='r')
#plt.vlines(0.7,-0.0304,0.053700,color='r')
#plt.hlines(y_bar,0,1)
#plt.vlines(x_bar,lower(x_bar),upper(x_bar))
#plt.plot(x_values,y_1,color='r')
#plt.plot(x_values,y_2,color='r')
#plt.plot(x_bar,y_bar,'rp',markersize=6)
#plt.xlabel('x/c')
#plt.ylabel('y/c')
#plt.show()



        

