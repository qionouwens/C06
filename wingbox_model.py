import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import scipy as sp
from scipy import interpolate

data = np.genfromtxt('sc20714.txt',skip_header=1)
x = data[:,0]
y = data[:,1]

spar_location = [0.2,0.7]

x_values = spar_location
y_1 = [-0.0633,-0.0304]
y_2 = [0.0633,0.0537]

b = (y_2[0]-y_1[0])
a = (y_2[1]-y_1[1])
c = y_2[0] - y_2[1]



# numerical integration
upper = sp.interpolate.interp1d(x_values, y_2, kind='linear',fill_value='extrapolate')
lower = sp.interpolate.interp1d(x_values, y_1, kind='linear',fill_value='extrapolate')

lng_upper = sqrt((x_values[0]-x_values[1])**2 + (y_2[0]-y_2[1])**2)
lng_lower = sqrt((x_values[0]-x_values[1])**2 + (y_1[0]-y_1[1])**2)

dA = 0.0001
dx = 0.01
t = dx

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
    
y_bar = (sum_Q + b * t * 0 + a * t * a/2)/(count*dA + (b+a)*t)

x_bar = 0.2 + ((lng_upper + lng_lower)*t * 0.25 + 0.5 * a * t) / ((b+a+lng_lower+lng_upper)*t)

### moment of inertia computations ###
A = 1/12 * t * b**3 + (b*t)*((y_2[0] - b/2)-y_bar)**2 
B = 1/12 * t * a**3 + (a*t)*((y_2[1] - a/2)-y_bar)**2
C = (t * lng_upper**3 * (sin(beta_upper)**2)) / 12 + (lng_upper)*t * (upper(0.45)-y_bar)**2
D = (t * lng_lower**3 * (sin(beta_lower)**2)) / 12 + (lng_lower)*t * (lower(0.45)-y_bar)**2

I_xx = A+B+C+D

E = (b*t)*(spar_location[1]-x_bar)**2
F = (b*t)*(spar_location[0]-x_bar)**2
G = (t * lng_upper**3 * (cos(beta_upper)**2)) / 12 + (lng_upper)*t * ((spar_location[1]-spar_location[0])-x_bar)**2
H = (t * lng_lower**3 * (cos(beta_lower)**2)) / 12 + (lng_lower)*t * ((spar_location[1]-spar_location[0])-x_bar)**2

I_yy = E+F+G+H

plt.plot(x,y)
plt.vlines(0.2,-0.0633,0.0633,color='r')
plt.vlines(0.7,-0.0304,0.053700,color='r')
plt.hlines(y_bar,0,1)
plt.vlines(x_bar,lower(x_bar),upper(x_bar))
plt.plot(x_values,y_1,color='r')
plt.plot(x_values,y_2,color='r')
plt.plot(x_bar,y_bar,'rp',markersize=6)
plt.show()



        

