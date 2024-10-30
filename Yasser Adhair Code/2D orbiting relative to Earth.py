import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
import numpy as np
from matplotlib.animation import FuncAnimation
import math 

def find_theta(m_pos):
    theta = math.atan2(m_pos[1],m_pos[0])
    return theta

def find_r(m_pos):
    r = math.hypot(m_pos[0],m_pos[1])
    return r

def update_acceleration(G,M,m,r,theta):
    conv = 1.496*(10**11)
    r = r * conv
    r_square = r**2
    F = (G*m*M)/r_square
    a = F/m
    a = a/conv
    a_x = -a*math.cos(theta)
    a_y = -a*math.sin(theta)
    a = [a_x,a_y]
    return a

def update_v(m_v,dt,a):
    m_v[0] = m_v[0] + dt*a[0]
    m_v[1] = m_v[1] + dt*a[1]
    return m_v

def update_pos(m_pos,dt,m_v):
    m_pos[0] = m_pos[0] + dt*m_v[0]
    m_pos[1] = m_pos[1] + dt*m_v[1]
    return m_pos

def update_pos_rel_earth(earth_pos,m_pos):
    rel_earthx = m_pos[0]-earth_pos[0]
    rel_earthy = m_pos[1]-earth_pos[1]
    rel_earth = [rel_earthx,rel_earthy]
    return rel_earth

#Simulation constants
G = 6.67*(10**-11)
#dt = 31540
dt = 100000

#Masses
M = 1.989 * (10**30)
earth_mass = 5.9722 * (10**24)
mercury_mass = 3.285 * (10**23)
venus_mass = 4.867 * (10**24)
mars_mass = 0.64169 * (10**24)
jupiter_mass = 1898.13 * (10**24)
saturn_mass = 568.32 * (10**24)
uranus_mass = 86.811 * (10**24)
neptune_mass = 102.409 * (10**24)

#Starting points
earth_pos = [1.0167257013,0]

earth_pos_rel_earth = update_pos_rel_earth(earth_pos,earth_pos)


M_pos = [0,0]

M_pos_rel_earth = update_pos_rel_earth(earth_pos,M_pos)


mercury_pos = [0.467, 0]

mercury_pos_rel_earth = update_pos_rel_earth(earth_pos,mercury_pos)


venus_pos = [0.72821700963,0]

venus_pos_rel_earth = update_pos_rel_earth(earth_pos,venus_pos)


mars_pos = [1.66620687,0]

mars_pos_rel_earth = update_pos_rel_earth(earth_pos,mars_pos)


jupiter_pos = [5.4570496,0]

jupiter_pos_rel_earth = update_pos_rel_earth(earth_pos,jupiter_pos)


saturn_pos = [10.070511,0]

saturn_pos_rel_earth = update_pos_rel_earth(earth_pos,saturn_pos)


uranus_pos = [20.0630529,0]

uranus_pos_rel_earth = update_pos_rel_earth(earth_pos,uranus_pos)


neptune_pos = [30.4740768,0]

neptune_pos_rel_earth = update_pos_rel_earth(earth_pos,neptune_pos)


earth_x=[earth_pos_rel_earth[0]]
earth_y=[earth_pos_rel_earth[1]]

M_x_rel_earth = [M_pos_rel_earth[0]]
M_y_rel_earth = [M_pos_rel_earth[1]]

mercury_x=[mercury_pos_rel_earth[0]]
mercury_y=[mercury_pos_rel_earth[1]]

venus_x = [venus_pos_rel_earth[0]]
venus_y = [venus_pos_rel_earth[1]]

mars_x= [mars_pos_rel_earth[0]]
mars_y = [mars_pos_rel_earth[1]]

jupiter_x= [jupiter_pos_rel_earth[0]]
jupiter_y= [jupiter_pos_rel_earth[1]]

saturn_x = [saturn_pos_rel_earth[0]]
saturn_y = [saturn_pos_rel_earth[1]]

uranus_x = [uranus_pos_rel_earth[0]]
uranus_y = [uranus_pos_rel_earth[1]]

neptune_x = [neptune_pos_rel_earth[0]]
neptune_y = [neptune_pos_rel_earth[1]]


#Velocity
earth_v = [0,(1.95791561*(10**-7))]
mercury_v = [0, (3.07491*(10**-7))]
venus_v = [0,(2.3248994*(10**-7))]
mars_v = [0,(1.4686038*(10**-7))]
jupiter_v = [0,(8.3156264*(10**-8))]
saturn_v = [0,(6.109713*(10**-8))]
uranus_v = [0,(4.338297*(10**-8))]
neptune_v = [0,(3.589623*(10**-8))]

#Acceleration
earth_r = find_r(earth_pos)
earth_theta = find_theta(earth_pos)
earth_a = update_acceleration(G,M,earth_mass,earth_r,earth_theta)
mercury_r = find_r(mercury_pos)
mercury_theta = find_theta(mercury_pos)
mercury_a = update_acceleration(G,M,mercury_mass,mercury_r,mercury_theta)
venus_r = find_r(venus_pos)
venus_theta = find_theta(venus_pos)
venus_a = update_acceleration(G,M,venus_mass,venus_r,venus_theta)
mars_r = find_r(mars_pos)
mars_theta = find_theta(mars_pos)
mars_a = update_acceleration(G,M,mars_mass,mars_r,mars_theta)
jupiter_r = find_r(jupiter_pos)
jupiter_theta = find_theta(jupiter_pos)
jupiter_a = update_acceleration(G,M,jupiter_mass,jupiter_r,jupiter_theta)
saturn_r = find_r(saturn_pos)
saturn_theta = find_theta(saturn_pos)
saturn_a = update_acceleration(G,M,saturn_mass,saturn_r,saturn_theta)
uranus_r = find_r(uranus_pos)
uranus_theta = find_theta(uranus_pos)
uranus_a = update_acceleration(G,M,uranus_mass,uranus_r,uranus_theta)
neptune_r = find_r(neptune_pos)
neptune_theta = find_theta(neptune_pos)
neptune_a = update_acceleration(G,M,neptune_mass,neptune_r,neptune_theta)



def update_frame(frame):
    global earth_v,earth_a,earth_mass,dt,earth_pos,earth_r,earth_theta,earth_pos_rel_earth
    global M,G
    earth_v = update_v(earth_v,dt,earth_a)
    earth_pos = update_pos(earth_pos,dt,earth_v)
    earth_pos_rel_earth = update_pos_rel_earth(earth_pos,earth_pos)
    earth_x.append(earth_pos_rel_earth[0])
    earth_y.append(earth_pos_rel_earth[1])
    earth_r = find_r(earth_pos)
    earth_theta = find_theta(earth_pos)
    earth_a = update_acceleration(G,M,earth_mass,earth_r,earth_theta)
    earth.set_center(earth_pos_rel_earth)
    earth_line.set_data(earth_x,earth_y)

    global M_pos, M_pos_rel_earth
    M_pos_rel_earth = update_pos_rel_earth(earth_pos,M_pos)
    M_x_rel_earth.append(M_pos_rel_earth[0])
    M_y_rel_earth.append(M_pos_rel_earth[1])
    sun.set_center(M_pos_rel_earth)
    M_line.set_data(M_x_rel_earth,M_y_rel_earth)


    global mercury_v,mercury_a,mercury_mass,mercury_pos,mercury_r,mercury_theta, mercury_pos_rel_earth
    mercury_v = update_v(mercury_v,dt,mercury_a)
    mercury_pos = update_pos(mercury_pos,dt,mercury_v)
    mercury_pos_rel_earth = update_pos_rel_earth(earth_pos,mercury_pos)
    mercury_x.append(mercury_pos_rel_earth[0])
    mercury_y.append(mercury_pos_rel_earth[1])
    mercury_r = find_r(mercury_pos)
    mercury_theta = find_theta(mercury_pos)
    mercury_a = update_acceleration(G,M,mercury_mass,mercury_r,mercury_theta)
    mercury.set_center(mercury_pos_rel_earth)
    mercury_line.set_data(mercury_x,mercury_y)

    global venus_v,venus_a,venus_mass,venus_pos,venus_r,venus_theta, venus_pos_rel_earth
    venus_v = update_v(venus_v,dt,venus_a)
    venus_pos = update_pos(venus_pos,dt,venus_v)
    venus_pos_rel_earth = update_pos_rel_earth(earth_pos,venus_pos)
    venus_x.append(venus_pos_rel_earth[0])
    venus_y.append(venus_pos_rel_earth[1])
    venus_r = find_r(venus_pos)
    venus_theta = find_theta(venus_pos)
    venus_a = update_acceleration(G,M,venus_mass,venus_r,venus_theta)
    venus.set_center(venus_pos_rel_earth)
    venus_line.set_data(venus_x,venus_y)

    global mars_v,mars_a,mars_mass,mars_pos,mars_r,mars_theta, mars_pos_rel_earth
    mars_v = update_v(mars_v,dt,mars_a)
    mars_pos = update_pos(mars_pos,dt,mars_v)
    mars_pos_rel_earth = update_pos_rel_earth(earth_pos,mars_pos)
    mars_x.append(mars_pos_rel_earth[0])
    mars_y.append(mars_pos_rel_earth[1])
    mars_r = find_r(mars_pos)
    mars_theta = find_theta(mars_pos)
    mars_a = update_acceleration(G,M,mars_mass,mars_r,mars_theta)
    mars.set_center(mars_pos_rel_earth)
    mars_line.set_data(mars_x,mars_y)

    global jupiter_v,jupiter_a,jupiter_mass,jupiter_pos,jupiter_r,jupiter_theta, jupiter_pos_rel_earth
    jupiter_v = update_v(jupiter_v,dt,jupiter_a)
    jupiter_pos = update_pos(jupiter_pos,dt,jupiter_v)
    jupiter_pos_rel_earth = update_pos_rel_earth(earth_pos,jupiter_pos)
    jupiter_x.append(jupiter_pos_rel_earth[0])
    jupiter_y.append(jupiter_pos_rel_earth[1])
    jupiter_r = find_r(jupiter_pos)
    jupiter_theta = find_theta(jupiter_pos)
    jupiter_a = update_acceleration(G,M,jupiter_mass,jupiter_r,jupiter_theta)
    jupiter.set_center(jupiter_pos_rel_earth)
    jupiter_line.set_data(jupiter_x,jupiter_y)

    global saturn_v,saturn_a,saturn_mass,saturn_pos,saturn_r,saturn_theta, saturn_pos_rel_earth
    saturn_v = update_v(saturn_v,dt,saturn_a)
    saturn_pos = update_pos(saturn_pos,dt,saturn_v)
    saturn_pos_rel_earth = update_pos_rel_earth(earth_pos,saturn_pos)
    saturn_x.append(saturn_pos_rel_earth[0])
    saturn_y.append(saturn_pos_rel_earth[1])
    saturn_r = find_r(saturn_pos)
    saturn_theta = find_theta(saturn_pos)
    saturn_a = update_acceleration(G,M,saturn_mass,saturn_r,saturn_theta)
    saturn.set_center(saturn_pos_rel_earth)
    saturn_line.set_data(saturn_x,saturn_y)

    global uranus_v,uranus_a,uranus_mass,uranus_pos,uranus_r,uranus_theta, uranus_pos_rel_earth
    uranus_v = update_v(uranus_v,dt,uranus_a)
    uranus_pos = update_pos(uranus_pos,dt,uranus_v)
    uranus_pos_rel_earth = update_pos_rel_earth(earth_pos,uranus_pos)
    uranus_x.append(uranus_pos_rel_earth[0])
    uranus_y.append(uranus_pos_rel_earth[1])
    uranus_r = find_r(uranus_pos)
    uranus_theta = find_theta(uranus_pos)
    uranus_a = update_acceleration(G,M,uranus_mass,uranus_r,uranus_theta)
    uranus.set_center(uranus_pos_rel_earth)
    uranus_line.set_data(uranus_x,uranus_y)

    global neptune_v,neptune_a,neptune_mass,neptune_pos,neptune_r,neptune_theta, neptune_pos_rel_earth
    neptune_v = update_v(neptune_v,dt,neptune_a)
    neptune_pos = update_pos(neptune_pos,dt,neptune_v)
    neptune_pos_rel_earth = update_pos_rel_earth(earth_pos,neptune_pos)
    neptune_x.append(neptune_pos_rel_earth[0])
    neptune_y.append(neptune_pos_rel_earth[1])
    neptune_r = find_r(neptune_pos)
    neptune_theta = find_theta(neptune_pos)
    neptune_a = update_acceleration(G,M,neptune_mass,neptune_r,neptune_theta)
    neptune.set_center(neptune_pos_rel_earth)
    neptune_line.set_data(neptune_x,neptune_y)

    return earth, sun, M_line, earth_line, mercury, mercury_line, venus, venus_line, mars, mars_line, jupiter,jupiter_line, saturn,saturn_line, uranus, uranus_line, neptune, neptune_line


def init_func():
    ax.grid()
    ax.set_title('Solar System Orbit Simulation Relative To Earth')
    ax.set_xlabel('Semi-major axis /AU')
    ax.set_ylabel('Semi-minor axis /AU')
    global earth, mercury, venus, mars, jupiter, saturn, sun, uranus, neptune
    earth = patches.Circle(earth_pos_rel_earth, radius = 0.08,fc= 'b')
    sun = patches.Circle(M_pos_rel_earth, radius= 0.1, fc= 'yellow')
    mercury = patches.Circle(mercury_pos_rel_earth, radius = 0.05, fc = 'r')
    venus = patches.Circle(venus_pos_rel_earth, radius =0.08, fc = 'orange')
    mars = patches.Circle(mars_pos_rel_earth, radius=0.1, fc = 'r')
    jupiter = patches.Circle(jupiter_pos_rel_earth, radius = 0.2, fc = 'brown')
    saturn = patches.Circle(saturn_pos_rel_earth, radius = 0.2, fc = 'sandybrown')
    uranus = patches.Circle(uranus_pos_rel_earth, radius = 0.2,fc= 'lightblue')
    neptune = patches.Circle(neptune_pos_rel_earth, radius = 0.2,fc= 'darkblue')
    ax.add_patch(earth)
    ax.add_patch(sun)
    ax.add_patch(mercury)
    ax.add_patch(venus)
    ax.add_patch(mars)
    ax.add_patch(jupiter)
    ax.add_patch(saturn)
    ax.add_patch(uranus)
    ax.add_patch(neptune)
    ax.set_aspect('equal')
    global earth_line, mercury_line, venus_line, mars_line, jupiter_line, saturn_line, uranus_line, neptune_line, M_line
    earth_line, = ax.plot(earth_x,earth_y, color = 'blue', label = 'Earth')
    mercury_line, = ax.plot(mercury_x,mercury_y, color = 'red', label = 'Mercury')
    venus_line, = ax.plot(venus_x,venus_y, color = 'orange',label = 'Venus')
    mars_line, = ax.plot(mars_x,mars_y, color = 'red', label = 'Mars')
    jupiter_line, = ax.plot(jupiter_x,jupiter_y, color = 'brown', label = 'Jupiter')
    saturn_line, = ax.plot(saturn_x,saturn_y, color = 'sandybrown', label = 'Saturn')
    uranus_line, = ax.plot(uranus_x,uranus_y, color = 'blue', label = 'Uranus')
    neptune_line, = ax.plot(neptune_x,neptune_y, color = 'darkblue', label = 'Neptune')
    M_line, = ax.plot(M_x_rel_earth,M_y_rel_earth, color = 'yellow', label = 'Sun')
    return earth, sun, mercury, venus, mars, jupiter, saturn, uranus, neptune

fig, ax = plt.subplots()
earth_line, = ax.plot(earth_x,earth_y, color = 'blue', label = 'Earth')
mercury_line, = ax.plot(mercury_x,mercury_y, color = 'red', label = 'Mercury')
venus_line, = ax.plot(venus_x,venus_y, color = 'orange',label = 'Venus')
mars_line, = ax.plot(mars_x,mars_y, color = 'red', label = 'Mars')
jupiter_line, = ax.plot(jupiter_x,jupiter_y, color = 'brown', label = 'Jupiter')
saturn_line, = ax.plot(saturn_x,saturn_y, color = 'sandybrown', label = 'Saturn')
uranus_line, = ax.plot(uranus_x,uranus_y, color = 'blue', label = 'Uranus')
neptune_line, = ax.plot(neptune_x,neptune_y, color = 'darkblue', label = 'Neptune')
M_line, = ax.plot(M_x_rel_earth,M_y_rel_earth, color = 'yellow', label = 'Sun')
ax.legend()
ax.axis([-31,31,-31,31])
ani = FuncAnimation(fig, update_frame, frames = 1000000, interval =0.001, init_func=init_func, repeat = False, blit = True)
plt.show()
