import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
import numpy as np
from matplotlib.animation import FuncAnimation
import math 
import random

def find_theta(m_pos):
    theta = math.atan2(m_pos[1],m_pos[0])
    return theta

def find_r(m_pos):
    r = math.hypot(m_pos[0],m_pos[1])
    return r

def find_x(m_pos, r, start_pos):
    if r == 0:
        x = 0
        return x
    elif start_pos[0] == 0:
        if start_pos[1]/m_pos[1] > 0:
            x = r
        else:
            x = -r
    elif start_pos[1] == 0:
        if start_pos[0]/m_pos[0] > 0:
            x = r
        else:
            x = -r
    else:
        if start_pos[0]/m_pos[0] > 0:
            x = r
        else:
            x = -r
    return x


def update_acceleration(G,M_mass,m,r,theta, M_radius):
    conv = 1
    r = r * conv
    ratio = (r/M_radius)
    r_square = r**2
    if r_square == 0:
        F = 0
    else:
        F = ((G*m*M_mass)/(r_square))
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

def update_rel_mass(r, M_density):
    rel_mass = (4/3) * math.pi * (r**3)*M_density
    return rel_mass

#Simulation constants
G = 6.67*(10**-11)
dt = 1
line = True
t = [0]
t_count = 0


#Starting points
M_pos = [0,0]
M_radius = 6371000
theta = math.radians(random.randrange(0,360,step=1))
x = M_radius*math.cos(theta)
y = M_radius*math.sin(theta)
ball_pos = [x,y]
start_pos = [x,y]
#ball_pos = [0,6371000.0]
#start_pos = [0,6371000.0]
ball_x = [ball_pos[0]]
ball_y = [ball_pos[1]]
ball_r = find_r(ball_pos)
M_x = find_x(ball_pos, ball_r,start_pos)
M_x_list = [M_x]

#Masses
M_density = 5513
M_mass_true = (4/3) * math.pi * (M_radius**3)*M_density
M_mass = update_rel_mass(M_radius, M_density)
ball_mass = 400

#Velocity
ball_v = [0,0]

#Acceleration
ball_theta = find_theta(ball_pos)
ball_a = update_acceleration(G,M_mass,ball_mass,ball_r,ball_theta, M_radius)

def update_frame(frame):
    global ball_v,ball_a,ball_mass,dt,ball_pos,ball_r,ball_theta
    global M_mass,G, line, start_pos, M_x, t_count
    ball_v = update_v(ball_v,dt,ball_a)

    ball_pos = update_pos(ball_pos,dt,ball_v)

    ball_r = find_r(ball_pos)

    M_mass = update_rel_mass(ball_r,M_density)

    ball_theta = find_theta(ball_pos)
    ball_a = update_acceleration(G,M_mass,ball_mass,ball_r,ball_theta, M_radius)

    M_x = find_x(ball_pos, ball_r,start_pos)
    M_x_list.append(M_x)
    t_count += dt
    t.append(t_count)
    ball.set_center(ball_pos)
    x_line.set_data(t,M_x_list)
    if line == True:
        ball_x.append(ball_pos[0])
        ball_y.append(ball_pos[1])
        ball_line.set_data(ball_x,ball_y)
        return M, ball, ball_line, x_line
    else:
        return M, ball, x_line


def init_func():
    global line
    ax.grid()
    ax.set_title('Hole through Earth simulation')
    ax.set_xlabel('X axis /km')
    ax.set_ylabel('Y axis /km')
    ax1.grid()
    ax1.set_title('X Vs Time')
    ax1.set_xlabel('Time /s')
    ax1.set_ylabel('X (displacement of ball on plane of hole) axis /km')
    global ball, M
    ball = patches.Circle(ball_pos, radius = 400000 ,fc= 'b')

    M = patches.Circle(M_pos, radius= 6371000, fc= 'green')
    ax.add_patch(M)
    ax.add_patch(ball)

    ax.set_aspect('equal')

    global x_line
    x_line, = ax1.plot(t,M_x_list, color = 'blue', label = 'Ball')

    if line == True:
        global ball_line
        ball_line, = ax.plot(ball_x,ball_y, color = 'blue', label = 'Ball')
    return ball, M, x_line

fig, (ax, ax1) = plt.subplots(1,2, figsize=(12,6))
if line == True:
    ball_line, = ax.plot(ball_x,ball_y, color = 'blue', label = 'Ball')
x_line, = ax1.plot(t,M_x_list, color = 'blue', label = 'Ball')

ax1.legend()
ax.legend()
ax.axis([-7000000,7000000,-7000000,7000000])
ax1.axis([0,8000,-6500000,6500000])

ani = FuncAnimation(fig, update_frame, frames = 6000, interval =0.1, init_func=init_func, repeat = False, blit = True)

period_calc = math.sqrt((3*(math.pi))/(M_density*G))
fig.text(0.8,0.8, s = 'The period from calculation ' + str(period_calc), ha='center')
plt.show()
update_frame(ani.new_frame_seq()[0])


        