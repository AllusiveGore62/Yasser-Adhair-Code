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
    global x_pos, y_pos, ax, fig, ball, line
    line.set_data(x_pos[:i],y_pos[:i])
    ball.set_data([x_pos[i]], [y_pos[i]])
    return line, ball,


def init_func(): 
    #This function is passed to the Func Animation function to initialise the graph
    global ax, fig, line, ball
    ax.set_title('Projectile Simulation')
    ax.set_xlabel('x /m')
    ax.set_ylabel('y /m')
    ax.grid()
    line, = ax.plot(x_pos[:1],y_pos[:1], color = 'blue', label = 'No air resistance')
    ball, = ax.plot([x_pos[0]], [y_pos[0]], color = 'blue', marker = 'o', markersize = 5)
    for i,x in enumerate(max_posx):
        ax.plot([x], [max_posy[i]], 'bx', markersize = 5)


#Making a graph function so that it can be called easily with GUI
def graph(theta, u, h):
    global  x_pos, y_pos, fig, ax, highest_x, highest_y, max_posx,max_posy
    #theta = launch angle from horizontal in degrees
    #g = strength of gravity in m/s^2
    #u = launch speed in m/s
    #h = launch height in m
    N_bounce = 0 #Number of bounces
    dt = 0.005 #time step in s
    theta = math.radians(theta) #turns theta into radians for calculations

    u_x = u * math.cos(theta) # initial x velocity
    u_y = u * math.sin(theta) # initial y velocity

    v_x = u_x # since x velocity doesn't change this is not an array
    v_y = np.array([u_y]) # Velocity array

    x_pos = np.array([0.0]) # array of x positions relative to origin during flight /m
    y_pos = np.array([float(h)]) # array of y positions relative to origin during flight /m

    max_posx = np.array([]) #A log of all the apogee x coordinates
    max_posy = np.array([]) #A log of all the apogee y coordinates
    #Finding the apogee using v**2 = u**2 - 2gs 
    # u**2/2g = s
    highest_y = (u_y**2)/(2*g) + h 
    if C != 1:
        T = (u_y/g)+ 2*((2*highest_y/g)**(1/2))*((1/(1-C))-0.5) #Finding out how long until the ball stops bouncing
    else:
        T = (u_y/g)+ 2*((2*highest_y/g)**(1/2))*((1/(1-0.9))-0.5)
    T_bounces = abs((u_y/g) + 2*((2*highest_y/g)**(1/2))*(((1-(C**N))/(1-C))-0.5) + (C**(N-1)*(((2*h)/g)**0.5)))#Time taken to complete the desired number of bounces
    #Added bit at the start to account for balling going upwards.
    #Added bit at the end because the time equation seems to stop at the last apogee.



    last_frame = int((T_bounces//dt) + 1) #Calculates the number of frames needed, adding 1 to ensure it rounds up
    highest_x = T_bounces * v_x #Calculating the highest x for accurate scale
    bounce_flag = True #This is used to tell the program it has bounced once
    for i in range(last_frame):
        if N_bounce >= N: #End condition for number of bounces
            break
        else:
            #np.append is formatted like array = np.append(array, item you want to add to array) and it returns a new array with the item in it.
            #np arrays are used because it is a lot more compatable with matplotlib graphs
            x_pos = np.append(x_pos, x_pos[i] + (v_x * dt))  #Find next x coordinate and append it
            y_pos = np.append(y_pos, y_pos[i] + (v_y[i] * dt)) #Find next y coordinate and append it
            v_y = np.append(v_y, v_y[i] - (g * dt)) #Calculate new y velocity
            if y_pos[i+1] < 0 and v_y[i+1] < 0 and bounce_flag == False: #A bounce condition for the animation if y drops below zero/hits the ground
                y_pos[i+1] = 0 #Puts ball at ground level instead of below
                v_y[i+1] = -v_y[i+1] * C #Reverses y velocity
                N_bounce += 1
                bounce_flag = True #This will make sure the ball only bounces once when it hits the ground
                
            if v_y[i+1] < 0 and bounce_flag == True:
                max_posx = np.append(max_posx, x_pos[i])
                max_posy = np.append(max_posy, y_pos[i])
                bounce_flag = False #Resets bounce flag as it will only bounce when velocity is negative

    Tmax_label.config(text= 'Tmax = ' + str(T_bounces) + 's')
    Tstop_label.config(text= 'T to stop bouncing = ' + str(T) + 's')
    fig, ax = plt.subplots() #Initialises the axes and figure
    ani = FuncAnimation(fig, func= update_frame, frames = len(x_pos),init_func=init_func(),blit = True, interval = 5, repeat = False) #Makes the animation
    plt.axis([0,(highest_x//1)+1,0,(highest_y//1)+1]) #Setting axis range
    plt.legend()
    plt.show() #Shows the graph and animation

root = Tk() #Intialising window

theta_entry = Entry(root, width = 50) #Input box for angle
g_entry = Entry(root, width=50) #Input box for gravity
u_entry = Entry(root, width=50) #Input box for initial speed
h_entry = Entry(root, width=50) #Input box for height
N_entry = Entry(root, width=50) #Input box for number of bounces
C_entry = Entry(root, width=50) #Input box for C

def clicked(): #Function for if the enter_button is clicked
    global g, C, N #Makes g global for other variables
    theta = theta_entry.get() #Gets the values from each text box
    g = g_entry.get()
    u = u_entry.get()
    h = h_entry.get()
    N = N_entry.get()
    C = C_entry.get()
    if len(theta) != 0 and len(g) != 0 and len(u) != 0 and len(h) != 0 and len(N) != 0 and len(C) != 0: #Ensures they are not empty
        try: #Tries to convert the values into floats
            theta = float(theta)
            g = float(g)
            u = float(u)
            h = float(h)
            N = int(N) + 1
            C = float(C)
            if g > 0 and u >= 0 and h >= 0 and theta >= -90 and theta <= 90 and N >= 0 and C <= 1 and C >= 0: #Checks if data is valid
                graph(theta,u,h) #Outputs the graph
            else: #Tells the user to make sure all data is valid
                error_label.config(text = 'Ensure g > 0, u >= 0, h >= 0, -90 <= theta <= 90, N >= 0, and 0 <= C <= 1')
        
        except KeyError: #If values can't be converted into floats, tell the user to make sure all data is numerical
            error_label.config(text = 'Ensure all data is numerical')
    
    else: #If the text box is empty is enters an error message
        error_label.config(text = 'Ensure all data is filled')


enter_button = Button(root,text = 'Finalise data', command= clicked) #Create the labels
theta_label = Label(root, text= 'Enter the launch angle from the horizontal in degrees: ') 
g_label = Label(root, text= 'Enter the strength of gravity in m/s^2: ')
u_label = Label(root, text= 'Enter the launch speed in m/s: ')
h_label = Label(root, text='Enter the launch height in m: ')
N_label = Label(root, text='Enter the number of bounces: ')
C_label = Label(root, text='Enter the coefficient of restitution: ')
error_label = Label(root, text= 'Ensure all data is correct')
Tmax_label = Label(root, text= 'Tmax = ')
Tstop_label = Label(root, text= 'T to stop bouncing = ')


theta_label.pack() #Add all the buttons and labels and entry boxes in the correct order
theta_entry.pack()
g_label.pack()
g_entry.pack()
u_label.pack()
u_entry.pack()
h_label.pack()
h_entry.pack()
N_label.pack()
N_entry.pack()
C_label.pack()
C_entry.pack()
enter_button.pack()
Tmax_label.pack()
Tstop_label.pack()
root.mainloop() #Display window and start mainloop