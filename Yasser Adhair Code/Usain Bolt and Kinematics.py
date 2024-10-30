import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib as mpl 
from matplotlib.ticker import MultipleLocator

a = [0, 1.83,2.87,3.78, 4.65, 5.5, 6.32, 7.14, 7.96, 8.79, 9.69]
b = [0, 10,20,30,40,50,60,70,80,90,100]
c = [0, 1.89, 2.88, 3.78, 4.64, 5.47, 6.29, 7.10, 7.92, 8.75, 9.58]
graph1 = False
graph2 = False
graph3 = True
if graph1 == True:
    fig, ax= plt.subplots() #Graph 1 (distance)

if graph2 == True:
    fig1, ax1 = plt.subplots() #Graph 2 (velocity)

if graph3 == True:
    fig2, ax2 = plt.subplots()

#Function for initialising the polynomial and returning the desired x and y points
def initialise_Poly(a,b,order, points):
    cubic_coefficients = np.polyfit(a,b,order) # Creates the actual cubic/polynomal equation (ax^2 + bx + c), third number is polynomial order
    x_interp = np.linspace(min(a), max(a),points) # Makes 100 evenly spaced data points for x between its minimum and maximum values
    cubic_interpolation = np.poly1d(cubic_coefficients) # Actually makes a curve class using the coefficients
    y_interp_cubic = cubic_interpolation(x_interp) # Curve class / function now fed x points to produce y points.
    return x_interp, y_interp_cubic

#Finding and plotting for 2008 distance data
a_cubic_x, a_cubic_y = initialise_Poly(a,b,3, 100)
if graph1 == True:
    ax.plot(a_cubic_x,a_cubic_y, color = 'blue') # Plots curve
    ax.scatter(a,b, label = '2008', color = 'blue', marker = 'x') # Makes original datapoints visible


#Finding and plotting for 2008 velocity data
a_cubic_x,a_cubic_y = initialise_Poly(a,b,3,100)
a_cubic_grad = np.gradient(a_cubic_y,a_cubic_x) #Finds local gradient between each point
if graph2 == True:
    ax1.plot(a_cubic_x,a_cubic_grad, color = 'blue', label = '2008')

#Finding and plotting for 2008 acceleration data
if graph3 == True:
    a_cubic_acc = np.gradient(a_cubic_grad,a_cubic_x)
    ax2.plot(a_cubic_x,a_cubic_acc, color = 'blue', label = '2008')


#Finding and plotting for 2009 distance data
c_cubic_x, c_cubic_y = initialise_Poly(c,b,3, 100)
if graph1 == True:
    ax.plot(c_cubic_x,c_cubic_y, color = 'orange')
    ax.scatter(c,b, label = '2009', color = 'orange', marker = 'x')

#Finding and plotting for 2009 velocity data
c_cubic_x,c_cubic_y = initialise_Poly(c,b,3,100)
c_cubic_grad = np.gradient(c_cubic_y,c_cubic_x)
if graph2 == True:
    ax1.plot(c_cubic_x,c_cubic_grad,  color = 'orange', label = '2009')

#Finding and plotting for 2009 acceleration data
if graph3 == True:
    c_cubic_acc = np.gradient(c_cubic_grad,c_cubic_x)
    ax2.plot(c_cubic_x,c_cubic_acc, color = 'orange', label = '2009')


#ax.plot(a,b, label = '2008', color = 'blue', marker='x', markersize = 8 )
#ax.scatter(a,b, color = 'blue')
#ax.plot(c,b, label = '2009', color = 'orange', marker='x', markersize = 8)
#ax.scatter(c,b, color = 'orange')

#ax settings
if graph1 == True:
    ax.set_xlabel('time /s')
    ax.set_ylabel('Displacement x /m')
    ax.set_title('Usain Bolt 100m stats: (t,x) graph')
    ax.grid()
    ax.legend()
    locator_y = MultipleLocator(base=10.0)
    ax.yaxis.set_major_locator(locator_y)
    locator_x = MultipleLocator(base=1.0)
    ax.xaxis.set_major_locator(locator_x)

#ax1 settings
if graph2 == True:
    ax1.set_xlabel('time t /s')
    ax1.set_ylabel('Velocity v /(m/s)')
    ax1.set_title('Usain Bolt 100m stats: (t,v) graph')
    ax1.grid()
    ax1.legend()
    locator = MultipleLocator(base=1.0)
    ax1.yaxis.set_major_locator(locator)
    ax1.xaxis.set_major_locator(locator)

#ax2 settings
if graph3 == True:
    ax2.set_xlabel('time t /s')
    ax2.set_ylabel('Acceleration a /(m/s^2)')
    ax2.set_title('Usain Bolt 100m stats: (t,a) graph')
    ax2.grid()
    ax2.legend()
    locator = MultipleLocator(base=1.0)
    ax2.yaxis.set_major_locator(locator)
    ax2.xaxis.set_major_locator(locator)

#Figure settings
plt.show()