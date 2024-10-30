import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
import numpy as np
from matplotlib.animation import FuncAnimation
import random

experiment = True
 
#Calculating the position to check for wall hit
def update_bounds(radius, position):
    left_bound = position[0] - radius
    right_bound = position[0] + radius
    down_bound = position[1] - radius
    up_bound = position[1] + radius
    bounds = [left_bound,right_bound,down_bound,up_bound]
    return bounds

def calculate_distance(pos1,pos2):
    x_distance = abs(pos1[0] - pos2[0])
    y_distance = abs(pos1[1] - pos2[1])
    distance_squared = (x_distance**2)+(y_distance**2)
    distance = distance_squared**(1/2)
    return distance

def check_ball_collision(min_distance, distance):
    if min_distance > distance:
        return True
    else:
        return False

def wall_collision(bounds, limits, v,c):
    if bounds[0] <= limits[0] and v[0] < 0:
        v[0] = v[0] * -c
        in_contact = True
    if bounds[1] >= limits[1] and v[0] > 0:
        v[0] = v[0] * -c
        in_contact = True
    if bounds[2] <= limits[2] and v[1] < 0:
        v[1] = v[1] * -c
        in_contact = True
    if bounds[3] >= limits[3] and v[1]> 0:
        v[1] = v[1] * -c
        in_contact = True
    else:
        in_contact = False
    return v, in_contact

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
    

#Masses
ball1_mass = 1
ball2_mass = 2
#Tennis and basketball
if experiment == True:
    ball1_mass = 600
    ball2_mass = 57


#Radii and minimum distance
ball1_radius = 1
ball2_radius = 1
#Tennis and basketball
if experiment == True:
    ball1_radius = 0.11938
    ball2_radius = 0.0335

min_distance = ball1_radius+ball2_radius

#Starting positions
ball1_pos = [0,0]
ball2_pos = [0,0]
#Tennis and basketball
if experiment == True:
    ball1_pos = [0.5,1.7]
    ball2_pos = [0.5,1.86]

distance = calculate_distance(ball1_pos, ball2_pos)
collision = check_ball_collision(min_distance, distance)
while collision == True:
    ball1_pos = [np.random.uniform(1,9),np.random.uniform(1,9)]
    ball2_pos = [np.random.uniform(1,9),np.random.uniform(1,9)]
    distance = calculate_distance(ball1_pos, ball2_pos)
    collision = check_ball_collision(min_distance, distance)




#Bounds
ball1_bound = update_bounds(ball1_radius, ball1_pos)
ball2_bound = update_bounds(ball2_radius, ball2_pos)

#Starting velocities
ball1_v = [0,0]
ball2_v = [0,0]
if experiment == False:
    ball1_v = [np.random.uniform(0,10),np.random.uniform(0,10)]
    ball2_v = [np.random.uniform(0,10),np.random.uniform(0,10)]

#Momentuum
ball1_mv = update_mv(ball1_mass, ball1_v)
ball2_mv = update_mv(ball2_mass, ball2_v)

#Walls and simulation things
ball1_contact = False
ball2_contact = False
limits = [0,10,0,10]
if experiment == True:
    limits = [0,1,0,8]

dt = 0.005
c = 0.9
t = 0
g = 9.81

def update_frame(frame):
    global ball1_bound, ball1_mass, ball1_mv, ball1_pos, ball1_v, ball1_radius, ball1_contact
    global ball2_bound, ball2_mass, ball2_mv, ball2_pos, ball2_v, ball2_radius, ball2_contact
    global t, limits
    ball1_v, ball1_contact = wall_collision(ball1_bound, limits, ball1_v,c)
    ball2_v, ball2_contact = wall_collision(ball2_bound, limits, ball2_v,c)
    if ball1_contact == False:
        ball1_v[1] += -g*dt
    if ball2_contact == False:
        ball2_v[1] += -g*dt
    ball1_mv = update_mv(ball1_mass, ball1_v)
    ball2_mv = update_mv(ball2_mass, ball2_v)
    distance = calculate_distance(ball1_pos, ball2_pos)
    collision = check_ball_collision(min_distance, distance)
    if collision == True:
        V = find_V(ball1_mv, ball2_mv, ball1_mass, ball2_mass)
        ball1_v, ball2_v = collide(V, c, ball1_v, ball2_v)
        ball1_mv = update_mv(ball1_mass, ball1_v)
        ball2_mv = update_mv(ball2_mass, ball2_v)
    ball1_pos[0] = ball1_pos[0] + (ball1_v[0]*dt)
    ball2_pos[0] = ball2_pos[0] + (ball2_v[0]*dt)
    ball1_pos[1] = (ball1_pos[1] + (ball1_v[1]*dt))
    ball2_pos[1] = (ball2_pos[1] + (ball2_v[1]*dt))
    ball1_bound = update_bounds(ball1_radius,ball1_pos)
    ball2_bound = update_bounds(ball2_radius,ball2_pos)
    t += dt
    circle1.set_center(ball1_pos)
    circle2.set_center(ball2_pos)
    return circle1,circle2,
    
def init_func():
    ax.grid()
    global circle1, circle2 
    circle1 = patches.Circle(ball1_pos, radius = ball1_radius, fc = 'r')
    circle2 = patches.Circle(ball2_pos, radius = ball2_radius, fc = 'b')
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.set_aspect('equal')
    return circle1,circle2,

fig, ax = plt.subplots()

ani = FuncAnimation(fig, update_frame,frames=5000,interval =5,init_func = init_func, repeat = False, blit = True)
plt.axis(limits)
plt.show()