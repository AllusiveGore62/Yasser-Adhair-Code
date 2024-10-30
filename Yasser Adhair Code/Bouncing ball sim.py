import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib as mpl 
from matplotlib.ticker import MultipleLocator
from matplotlib.animation import FuncAnimation

x = np.array([1.0])
n = 0
v = np.array([0.0])
t = np.array([0.0])
g = 9.81
dt = 0.005
C = 0.8
max_bounce = 50
bounce = 0

def update_data(frame):
    global x,v,t,bounce,max_bounce
    a = frame - 1
    x = np.append(x,x[a]-v[a]*dt-0.5*g*(dt**2))
    v = np.append(v, v[a] + g*dt)
    t = np.append(t, t[a] + dt)
    if (x[a+1]<0) and (v[a+1]>0):
        bounce += 1
        v[a+1] = -C*v[a+1]
        x[a+1] = 0
    line1.set_data(t,x)
    #axd.set_xlim(min(t),max(t))
    #axd.set_ylim(min(x),max(x))
    return line1,

def init_func():
    axd.set_title('Ball bounce. C = '+ str(C)+', T = '+ str(T)+'s')
    axd.set_xlabel('time t/s')
    axd.set_ylabel('displacement x /m')
    locatordy = MultipleLocator(base=0.2)
    locatordx = MultipleLocator(base=1)
    axd.yaxis.set_major_locator(locatordy)
    axd.xaxis.set_major_locator(locatordx)
    axd.grid()
    global line1 
    line1, = axd.plot(t,x, color = 'blue')

T = 2*((2*x[0]/g)**(1/2))*((1/(1-C))-0.5)
ran = int((T/dt)//1)*4
fig, axd = plt.subplots()
#fig1, axv = plt.subplots()
"""
line1, = axd.plot(t,x, color = 'blue')
axd.set_title('Ball bounce. C = '+ str(C)+', T = '+ str(T)+'s')
axd.set_xlabel('time t/s')
axd.set_ylabel('displacement x /m')
locatordy = MultipleLocator(base=0.2)
locatordx = MultipleLocator(base=1)
axd.yaxis.set_major_locator(locatordy)
axd.xaxis.set_major_locator(locatordx)
axd.grid()"""

"""
axv.plot(t,v, color = 'blue')
axv.set_title('Ball bounce. C = '+ str(C)+', T = '+ str(T)+'s')
axv.set_xlabel('time t/s')
axv.set_ylabel('velocity x /ms^-1')
axv.yaxis.set_major_locator(locatordx)
axv.xaxis.set_major_locator(locatordx)
axv.grid()"""

ani = FuncAnimation(fig, update_data, frames=range(ran), blit = True, interval = 3, init_func=init_func(), repeat = False)
plt.axis([0,4,0,1])
plt.show()
