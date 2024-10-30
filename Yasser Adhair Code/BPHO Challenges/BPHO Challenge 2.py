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
    global v_x, v_y, x_pos, y_pos, ax
    i = frame
    try: #Added try if i is out of range meaning we hit the ground
        if x_pos[i] >= R: #An end condition for the animation if x goes above the range
            return line,
        #np.append is formatted like array = np.append(array, item you want to add to array) and it returns a new array with the item in it.
        #np arrays are used because it is a lot more compatable with matplotlib graphs
        x_pos = np.append(x_pos, x_pos[i] + dx)  #Creates an equally spaced array of x coordinates (as requested in the question)
        y_pos = np.append(y_pos, y_pos[i] + (v_y[i] * dt)) #Find next y coordinate and append it
        v_y = np.append(v_y, v_y[i] - (g * dt)) #Calculate new y velocity
        line.set_data(x_pos,y_pos) #Update the data of the line
        return line, #Return the line to the FuncAnimation function
    except IndexError:
        return line,


def init_func(): 
    #This function is passed to the Func Animation function to initialise the graph
    global line, ax
    ax.set_title('Projectile Simulation, T = '+ str(T) + 's, R = ' + str(R) +'m')
    ax.set_xlabel('x /m')
    ax.set_ylabel('y /m')
    ax.grid()
    ax.plot(x_ap,highest_y, '-rx', label = 'apogee')
    line, = ax.plot(x_pos,y_pos, color = 'blue', label = 'y vs x')


#Making a graph function so that it can be called easily with GUI
def graph(theta, u, h):
    global v_x, v_y, x_pos, y_pos, g, fig, ax, T, highest_y, R, dt, dx, x_ap
    #theta = launch angle from horizontal in degrees
    #g = strength of gravity in m/s^2
    #u = launch speed in m/s
    #h = launch height in m

    theta = math.radians(theta) #turns theta into radians for calculations

    u_x = u * math.cos(theta) # initial x velocity
    u_y = u * math.sin(theta) # initial y velocity

    v_x = u_x # since x velocity doesn't change this is not an array
    v_y = np.array([u_y]) # Velocity array

    x_pos = np.array([0.0]) # array of x positions relative to origin during flight /m
    y_pos = np.array([float(h)]) # array of y positions relative to origin during flight /m
    
    #Previously used to find the last frame in the timestep, the flight time will now simply be displayed
    #I will do this using the concept that y = h + u_y*t - 0.5*g*(t**2) with y becoming 0
    a = -0.5 * g
    b = u_y
    c = h
    #We will only focus on the - case of the quadratic equation because 2a will always be negative and so will -b
    T = (-b - (math.sqrt((b**2)-4*a*c)))/(2*a) #T is the time to hit ground
    last_frame = 4000 #Since the we are plotting 1000 x points we only need 1000 animation frames
    R = T * v_x #Previously used to calculate the range x for accurate scale, can now be used as range for challenge No. 2
    dx = R/500 #Distance step of x, graph will always plot 1000 points now
    dt = dx/u_x #Finds the equivalent time step created by this analytical model, this means we don't have to make many changes to our update frame function
    #Finding the apogee using v**2 = u**2 - 2gs 
    # u**2/2g = s
    highest_y = (u_y**2)/(2*g) + h 
    x_ap = (u_x*u_y)/g #x at the apogee since time at apogee is u_y/g
    fig, ax = plt.subplots() #Initialises the axes and figure
    ani = FuncAnimation(fig, func= update_frame, frames = range(last_frame),init_func=init_func(),blit = True, interval = 3, repeat = False) #Makes the animation
    plt.axis([0,(R//1)+1,0,(highest_y//1)+1]) #Setting axis range
    plt.legend()
    plt.show() #Shows the graph and animation

root = Tk() #Intialising window

theta_entry = Entry(root, width = 50) #Input box for angle
g_entry = Entry(root, width=50) #Input box for gravity
u_entry = Entry(root, width=50) #Input box for initial speed
h_entry = Entry(root, width=50) #Input box for height

def clicked(): #Function for if the enter_button is clicked
    global g #Makes g global for other variables
    theta = theta_entry.get() #Gets the values from each text box
    g = g_entry.get()
    u = u_entry.get()
    h = h_entry.get()
    if len(theta) != 0 and len(g) != 0 and len(u) != 0 and len(h) != 0: #Ensures they are not empty
        try: #Tries to convert the values into floats
            theta = float(theta)
            g = float(g)
            u = float(u)
            h = float(h)
            if g > 0 and u >= 0 and h >= 0 and theta >= -90 and theta <= 90: #Checks if data is valid
                graph(theta,u,h) #Outputs the graph
            else: #Tells the user to make sure all data is valid
                error_label = Label(root, text = 'Ensure g > 0, u >= 0, h >= 0 and -90 <= theta <= 90')
                error_label.pack() #Puts the label in the window
        except TypeError: #If values can't be converted into floats, tell the user to make sure all data is numerical
            error_label = Label(root, text = 'Ensure all data is numerical')
            error_label.pack() #Puts the label in the window

    else: #If the text box is empty is enters an error message
        error_label = Label(root, text = 'Ensure all data is filled')
        error_label.pack() #Puts the label in the window

enter_button = Button(root,text = 'Finalise data', command= clicked) #Create the labels
theta_label = Label(root, text= 'Enter the launch angle from the horizontal in degrees: ') 
g_label = Label(root, text= 'Enter the strength of gravity in m/s^2: ')
u_label = Label(root, text= 'Enter the launch speed in m/s: ')
h_label = Label(root, text='Enter the launch height in m: ')

theta_label.pack() #Add all the buttons and labels and entry boxes in the correct order
theta_entry.pack()
g_label.pack()
g_entry.pack()
u_label.pack()
u_entry.pack()
h_label.pack()
h_entry.pack()
enter_button.pack()

root.mainloop() #Display window and start mainloop