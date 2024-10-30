#Importing libraries
import matplotlib as mpl #Matplotlib for graphing
import matplotlib.pyplot as plt #Function for actually plotting the graphs
import numpy as np #Useful for arrays
import math #For all the trigonometric calculations
from matplotlib.ticker import MultipleLocator #Useful for setting fixed axes scales
from matplotlib.animation import FuncAnimation #Used for animating the plot
from tkinter import * #Used for GUI


def update_frame(frame):
    #Update_frame will be passed to the animation function because it needs a function that will return a new line for each frame
    #The way FuncAnimation handles the local variables in the update frame function is strange so I have to move most variables to global scope
    i = frame
    global x_pos, y_pos, ax, fig, ball, line, x_pos_n, y_pos_n, ball_n, line_n
    if i <= len(x_pos):
        line.set_data(x_pos[:i],y_pos[:i])
        ball.set_data([x_pos[i-1]], [y_pos[i-1]])
    if i <= len(x_pos_n):
        line_n.set_data(x_pos_n[:i],y_pos_n[:i])
        ball_n.set_data([x_pos_n[i-1]], [y_pos_n[i-1]])
    return line, ball, line_n, ball_n


def init_func(): 
    #This function is passed to the Func Animation function to initialise the graph
    global ax, fig, line, ball, line_n, ball_n, max_pos_x, max_pos_y, max_pos_x_n, max_pos_y_n
    ax.set_title('Projectile Simulation')
    ax.set_xlabel('x /m')
    ax.set_ylabel('y /m')
    ax.grid()
    line, = ax.plot(x_pos[:1],y_pos[:1], color = 'red', label = 'Air resistance')
    ball, = ax.plot([x_pos[0]], [y_pos[0]], color = 'red', marker = 'o', markersize = 5)
    line_n, = ax.plot(x_pos_n[:1],y_pos_n[:1], color = 'blue', label = 'No air resistance')
    ball_n, = ax.plot([x_pos_n[0]], [y_pos_n[0]], color = 'blue', marker = 'o', markersize = 5)
    ax.plot([max_pos_x], [max_pos_y], 'rx', markersize = 5)
    ax.plot([max_pos_x_n], [max_pos_y_n], 'bx', markersize = 5)    


#Making a graph function so that it can be called easily with GUI
def graph(theta, u, h, drag, m, area, density, dt):
    global  x_pos, y_pos, fig, ax, highest_y, max_pos_x ,max_pos_y, max_pos_x_n, max_pos_y_n , x_pos_n, y_pos_n
    #theta = launch angle from horizontal in degrees
    #g = strength of gravity in m/s^2
    #u = launch speed in m/s
    #h = launch height in m
    # drag = drag coefficient
    # m  = mass in kg
    # area = cross sectional area in m^2
    # density = air density /kgm^-3
    # dt = time step in s
    theta = math.radians(theta) #turns theta into radians for calculations
    k = (0.5*drag*density*area)/m

    t = np.array([0])

    u_x = u * math.cos(theta) # initial x velocity
    u_y = u * math.sin(theta) # initial y velocity

    v_x = np.array([u_x]) # since x velocity doesn't change this is not an array
    v_y = np.array([u_y]) # Velocity array

    # Normal (n) velocities i.e: if no air resistance
    v_x_n = np.array([u_x]) 
    v_y_n = np.array([u_y])

    x_pos = np.array([0.0]) # array of x positions relative to origin during flight /m
    y_pos = np.array([float(h)]) # array of y positions relative to origin during flight /m

    #Positions for ball with no air resistance
    x_pos_n = np.array([0.0])
    y_pos_n = np.array([float(h)])

    v = np.array([u]) # array of speeds /m/s
    v_n = np.array([u]) # array of speeds with no air resistance /m/s

    # Added force for graphing purposes and future simulations even though it could just be done with acceleration
    f_x = np.array([-(u_x/u)*m*k*(u**2)]) # Force in the x direction /N
    f_y = np.array([-m*g-(u_y/u)*m*k*(u**2)]) # Force in the y direction /N

    #Forces with no air resistance
    f_x_n = np.array([0]) 
    f_y_n = np.array([-m*g])

    a_x = np.array([f_x[0]/m]) # Acceleration in the x direction /m/s^2
    a_y = np.array([f_y[0]/m]) # Acceleration in the y direction /m/s^2

    #Acceleration with no air resistance
    a_x_n = np.array([f_x_n[0]/m])
    a_y_n= np.array([f_y_n[0]/m])
    

    #Finding the apogee using v**2 = u**2 - 2gs 
    # u**2/2g = s
    highest_y = (u_y**2)/(2*g) + h 

    #Added bit at the start to account for balling going upwards.
    #Added bit at the end because the time equation seems to stop at the last apogee.

    i = 0
    apogee_flag = False #Marks whether the apogee has been reached yet
    apogee_flag_n = False
    while y_pos_n[-1] >= 0 or y_pos[-1] >= 0: #The simulation calculations will end when both balls hit the ground.
        
        #np.append is formatted like array = np.append(array, item you want to add to array) and it returns a new array with the item in it.
        #np arrays are used because it is a lot more compatable with matplotlib graphs
        if y_pos[-1] >= 0: #If statement to ensure simulation continues after 1 ball hits the ground (-1 prevents index error)
            x_pos = np.append(x_pos, x_pos[i] + (v_x[i] * dt))  #Find next x coordinate and append it
            y_pos = np.append(y_pos, y_pos[i] + (v_y[i] * dt)) #Find next y coordinate and append it
            if v_y[i] <= 0 and apogee_flag == False:
                max_pos_x = x_pos[i]
                max_pos_y = y_pos[i]
                apogee_flag = True
            v_x = np.append(v_x, v_x[i] + (a_x[i]*dt)) #Calculate new x velocity
            v_y = np.append(v_y, v_y[i] + (a_y[i]*dt)) #Calculate new y velocity

            v = np.append(v, math.hypot(v_x[i], v_y[i])) #Calculate new speed

            f_x = np.append(f_x,-(v_x[i]/v[i])*m*k*(v[i]**2)) #Calculate new force in x direction on ball
            f_y = np.append(f_y,-m*g-(v_y[i]/v[i])*m*k*(v[i]**2)) #Calculate new force in y direction on ball

            a_x = np.append(a_x, f_x[i]/m) #Calculate new acceleration on ball in x direction
            a_y = np.append(a_y, f_y[i]/m) #Calculate new acceleration on ball in y direction

        if y_pos_n[-1] >= 0:                
            x_pos_n = np.append(x_pos_n, x_pos_n[i] + (v_x_n[i] * dt))  #Find next x coordinate and append it for ball with no air resistance
            y_pos_n = np.append(y_pos_n, y_pos_n[i] + (v_y_n[i] * dt)) #Find next y coordinate and append it for ball with no air resistance      
            if v_y_n[i] <= 0 and apogee_flag_n == False:
                max_pos_x_n = x_pos_n[i]
                max_pos_y_n = y_pos_n[i]
                apogee_flag_n = True
            v_x_n = np.append(v_x_n, v_x_n[i] + (a_x_n[i]*dt)) #Calculate new x velocity on ball with no air resistance
            v_y_n = np.append(v_y_n, v_y_n[i] + (a_y_n[i]*dt)) #Calculate new y velocity on ball with no air resistance

            v_n = np.append(v_n, math.hypot(v_x_n[i], v_y_n[i])) #Calculate new speed with no air resistance

            f_x_n = np.append(f_x_n,0) #Calculate new force in x direction on ball with no air resistance
            f_y_n = np.append(f_y_n,-m*g) #Calculate new force in y direction on ball with no air resistance

            a_x_n = np.append(a_x_n, f_x_n[i]/m) #Calculate new acceleration on ball with no air resistance in x direction
            a_y_n = np.append(a_y_n, f_y_n[i]/m) #Calculate new acceleration on ball with no air resistance in y direction
        t = np.append(t, t[i] + dt)
        i += 1 #Next i


    y_pos[-1] = 0

    y_pos_n[-2] = 0

    Tstop_label_n.config(text= 'T no air resistance = ' + str(t[len(x_pos_n)-1]) + 's') #Finds the time that the ball with no air resistance hit the ground
    Tstop_label.config(text= 'T w/ air resistance = ' + str(t[len(x_pos)-1]) + 's') #Finds the time that the ball with air resistance hit the ground
    fig, ax = plt.subplots() #Initialises the axes and figure
    ani = FuncAnimation(fig, func= update_frame, frames = len(x_pos_n),init_func=init_func(),blit = True, interval = dt*1000, repeat = False) #Makes the animation
    plt.axis([0,(x_pos_n[-1]//1)+1,0,(highest_y//1)+1]) #Setting axis range
    plt.legend()
    plt.show() #Shows the graph and animation

root = Tk() #Intialising window

theta_entry = Entry(root, width = 50) #Input box for angle
g_entry = Entry(root, width=50) #Input box for gravity
u_entry = Entry(root, width=50) #Input box for initial speed
h_entry = Entry(root, width=50) #Input box for height
drag_entry = Entry(root, width=50) #Input box for drag coefficient
m_entry = Entry(root, width=50) #Input box for mass
area_entry = Entry(root, width=50) #Input box for cross sectional area
density_entry = Entry(root, width=50) #Input box for air density
dt_entry = Entry(root, width=50)

def clicked(): #Function for if the enter_button is clicked
    global g, C, N #Makes g global for other variables
    theta = theta_entry.get() #Gets the values from each text box
    g = g_entry.get()
    u = u_entry.get()
    h = h_entry.get()
    drag = drag_entry.get()
    m = m_entry.get()
    area = area_entry.get()
    density = density_entry.get()
    dt = dt_entry.get()
    if len(theta) != 0 and len(g) != 0 and len(u) != 0 and len(h) != 0 and len(drag) != 0 and len(m) != 0 and len(area) != 0 and len(density) != 0 and len(dt) != 0: #Ensures they are not empty
        try: #Tries to convert the values into floats
            theta = float(theta)
            g = float(g)
            u = float(u)
            h = float(h)
            drag = float(drag)
            m = float(m)
            area = float(area)
            density = float(density)
            dt = float(dt)
            if g > 0 and u >= 0 and h >= 0 and theta >= -90 and theta <= 90 and drag >= 0 and m > 0 and area > 0 and density > 0 and dt > 0: #Checks if data is valid
                graph(theta,u,h, drag,m,area,density, dt) #Outputs the graph
            else: #Tells the user to make sure all data is valid
                error_label.config(text = 'Ensure g > 0, u >= 0, h >= 0, -90 <= theta <= 90, drag >= 0, m > 0, area > 0, density > 0, and dt > 0')
        
        except KeyError: #If values can't be converted into floats, tell the user to make sure all data is numerical
            error_label.config(text = 'Ensure all data is numerical')
    
    else: #If the text box is empty is enters an error message
        error_label.config(text = 'Ensure all data is filled')


enter_button = Button(root,text = 'Finalise data', command= clicked) #Create the labels
theta_label = Label(root, text= 'Enter the launch angle from the horizontal in degrees: ') 
g_label = Label(root, text= 'Enter the strength of gravity in m/s^2: ')
u_label = Label(root, text= 'Enter the launch speed in m/s: ')
h_label = Label(root, text='Enter the launch height in m: ')
drag_label = Label(root, text='Enter the drag coefficient: ')
m_label = Label(root, text='Enter the mass in kg: ')
area_label = Label(root, text='Enter the cross-sectional area in m^2: ')
density_label = Label(root, text='Enter the air density in kg/m^3: ')
dt_label = Label(root, text= 'Enter the time step in s: ')
error_label = Label(root, text= 'Ensure all data is correct')
Tstop_label_n = Label(root, text= 'T no air resistance =')
Tstop_label = Label(root, text= 'T w/ air resistance = ')


theta_label.pack() #Add all the buttons and labels and entry boxes in the correct order
theta_entry.pack()
g_label.pack()
g_entry.pack()
u_label.pack()
u_entry.pack()
h_label.pack()
h_entry.pack()
drag_label.pack()
drag_entry.pack()
m_label.pack()
m_entry.pack()
area_label.pack()
area_entry.pack()
density_label.pack()
density_entry.pack()
dt_label.pack()
dt_entry.pack()
enter_button.pack()
Tstop_label_n.pack()
Tstop_label.pack()
root.mainloop() #Display window and start mainloop

#g = 10
#graph(45,10,1,0.1,10,0.01,100,0.01)