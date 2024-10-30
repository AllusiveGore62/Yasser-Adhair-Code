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

def calculate_distance(pos1,pos2):
    x_distance = abs(pos1[0] - pos2[0])
    y_distance = abs(pos1[1] - pos2[1])
    distance_squared = (x_distance**2)+(y_distance**2)
    distance = distance_squared**(1/2)
    return distance

def check_earth_collision(min_distance, distance):
    if min_distance > distance:
        return True
    else:
        return False

def update_mv(mass, v):
    mvx = mass * v[0]
    mvy = mass * v[1]
    mv = [mvx,mvy]
    return mv

def find_V(mv1,mv2,m1,m2):
    Vx = (mv1[0]+mv2[0])/(m1+m2)
    Vy = (mv1[1]+mv2[1])/(m1+m2)
    V = [Vx,Vy]
    return V

def collide(V,c,u1,u2):
    v1x = -c*(u1[0]-V[0])+V[0]
    v1y = -c*(u1[1]-V[1])+V[1]
    v2x = -c*(u2[0]-V[0])+V[0]
    v2y = -c*(u2[1]-V[1])+V[1]
    v1 = [v1x,v1y]
    v2 = [v2x,v2y]
    return v1,v2 

def update_v(m_v,dt,a):
    m_v[0] = m_v[0] + dt*a[0]
    m_v[1] = m_v[1] + dt*a[1]
    return m_v

def update_pos(m_pos,dt,m_v):
    m_pos[0] = m_pos[0] + dt*m_v[0]
    m_pos[1] = m_pos[1] + dt*m_v[1]
    return m_pos

#Simulation constants
G = 6.67*(10**-11)
#dt = 31540
c = 0.95
dt = 10000


#Masses
M = 1.989 * (10**30)
earth1_mass = 5.9722 * (10**24)
earth2_mass = 5.9722 * (10**24)

#Radii and minimum distance
earth1_radius = 40.26352 * (10**-4)
earth2_radius = 40.26352 * (10**-4)
#earth1_radius = 0.05
#earth2_radius = 0.05
min_distance = earth1_radius+earth2_radius

#Starting positions
M_pos = [0,0]
earth1_pos = [1.0167257013,0]
#earth2_pos = [-1.0167257013,0]
earth2_pos = [-0.98326934275, 0]

earth1_x = [earth1_pos[0]]
earth1_y = [earth1_pos[1]]
earth2_x = [earth2_pos[0]]
earth2_y = [earth2_pos[1]]


#Starting velocities
earth1_v = [0,(1.95791561*(10**-7))]
#earth2_v = [0,(1.95791561*(10**-7))]
earth2_v = [0,(2.0247614*(10**-7))]

#Momentuum
earth1_mv = update_mv(earth1_mass, earth1_v)
earth2_mv = update_mv(earth2_mass, earth2_v)

#Acceleration
earth1_r = find_r(earth1_pos)
earth1_theta = find_theta(earth1_pos)
earth1_a = update_acceleration(G,M,earth1_mass,earth1_r,earth1_theta)
earth2_r = find_r(earth2_pos)
earth2_theta = find_theta(earth2_pos)
earth2_a = update_acceleration(G,M,earth2_mass,earth2_r,earth2_theta)


def update_frame(frame):
    global earth1_mass, earth1_mv, earth1_pos, earth1_v, earth1_radius, earth1_theta, earth1_a, earth1_r
    global earth2_mass, earth2_mv, earth2_pos, earth2_v, earth2_radius, earth2_theta, earth2_a, earth2_r
    global dt, M, G
    earth1_v = update_v(earth1_v,dt,earth1_a)
    earth2_v = update_v(earth2_v,dt,earth2_a)
    earth1_mv = update_mv(earth1_mass, earth1_v)
    earth2_mv = update_mv(earth2_mass, earth2_v)
    distance = calculate_distance(earth1_pos, earth2_pos)
    collision = check_earth_collision(min_distance, distance)
    if collision == True:
        V = find_V(earth1_mv, earth2_mv, earth1_mass, earth2_mass)
        earth1_v, earth2_v = collide(V, c, earth1_v, earth2_v)
        earth1_mv = update_mv(earth1_mass, earth1_v)
        earth2_mv = update_mv(earth2_mass, earth2_v)
    earth1_pos = update_pos(earth1_pos,dt,earth1_v)
    earth1_x.append(earth1_pos[0])
    earth1_y.append(earth1_pos[1])
    earth2_pos = update_pos(earth2_pos,dt,earth2_v)
    earth2_x.append(earth2_pos[0])
    earth2_y.append(earth2_pos[1])
    earth1_r = find_r(earth1_pos)
    earth1_theta = find_theta(earth1_pos)
    earth1_a = update_acceleration(G,M,earth1_mass,earth1_r,earth1_theta)
    earth2_r = find_r(earth2_pos)
    earth2_theta = find_theta(earth2_pos)
    earth2_a = update_acceleration(G,M,earth2_mass,earth2_r,earth2_theta)
    earth1.set_center(earth1_pos)
    earth1_line.set_data(earth1_x,earth1_y)
    earth2.set_center(earth2_pos)
    earth2_line.set_data(earth2_x,earth2_y)

    return earth1, earth2, earth1_line, earth2_line, sun

def init_func():
    ax.grid()
    ax.set_title('Solar System Orbit Simulation with 2 earth collisions')
    ax.set_xlabel('Semi-major axis /AU')
    ax.set_ylabel('Semi-minor axis /AU')
    global earth1, earth2, sun
    earth1 = patches.Circle(earth1_pos, radius = 0.05,fc= 'b')
    earth2 = patches.Circle(earth2_pos, radius = 0.05,fc= 'r')
    sun = patches.Circle(M_pos, radius= 0.1, fc= 'yellow')
    ax.add_patch(earth1)
    ax.add_patch(earth2)
    ax.add_patch(sun)
    ax.set_aspect('equal')
    global earth1_line, earth2_line
    earth1_line, = ax.plot(earth1_x,earth1_y, color = 'blue', label = 'Normal Earth')
    earth2_line, = ax.plot(earth2_x,earth2_y, color = 'red', label = 'Alternate Earth')
    return earth1, earth2, sun

fig, ax = plt.subplots()
earth1_line, = ax.plot(earth1_x,earth1_y, color = 'blue', label = 'Normal Earth')
earth2_line, = ax.plot(earth2_x,earth2_y, color = 'red', label = 'Alternate Earth')
ax.legend()
ax.axis([-1.5,1.5,-1.5,1.5])
ani = FuncAnimation(fig, update_frame, frames = 6000, interval =0.01, init_func=init_func, repeat = False, blit = True)
plt.show()