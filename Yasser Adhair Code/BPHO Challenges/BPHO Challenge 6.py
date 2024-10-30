#Importing libraries
import matplotlib as mpl #Matplotlib for graphing
import matplotlib.pyplot as plt #Function for actually plotting the graphs
import numpy as np #Useful for arrays
import math #For all the trigonometric calculations
from matplotlib.ticker import MultipleLocator #Useful for setting fixed axes scales
from matplotlib.animation import FuncAnimation #Used for animating the plot
from tkinter import * #Used for GUI

def find_distance(u, g, theta, R): #Finds the distance travelled using solved integral
    z = math.tan(theta)
    c1 = (0.5 * np.log(abs(math.sqrt(1+(z**2))+z))) + (0.5 * z * math.sqrt(1+(z**2))) #First part of the integral z = (tan(theta)), the base of np.log is e
    z = math.tan(theta) - (((g*R)/(u**2))*(1+(math.tan(theta)**2)))
    c2 = (0.5 * np.log(abs(math.sqrt(1+(z**2))+z))) + (0.5 * z * math.sqrt(1+(z**2))) #First part of the integral 
    s = ((u**2)/(g*(1+(math.tan(theta)**2)))) * (c1-c2)
    return s

def update_points(x_pos, y_pos, v_x, v_y, i): #Made a function to update points to make it easier to code the update_frame function with multiple lines
    #np.append is formatted like array = np.append(array, item you want to add to array) and it returns a new array with the item in it.
    #np arrays are used because it is a lot more compatable with matplotlib graphs
    x_pos = np.append(x_pos, x_pos[i] + (v_x * dt))  #Find next x coordinate and append it
    y_pos = np.append(y_pos, y_pos[i] + (v_y[i] * dt)) #Find next y coordinate and append it
    v_y = np.append(v_y, v_y[i] - (g * dt)) #Calculate new y velocity
    return x_pos, y_pos, v_y

def update_frame(frame):
    #Update_frame will be passed to the animation function because it needs a function that will return a new line for each frame
    #The way FuncAnimation handles the local variables in the update frame function is strange so I have to move most variables to global scope
    global v_x, v_y, x_pos, y_pos
    global y_pos_max, x_pos_max, v_x_max, v_y_max
    i = frame #Because frame starts at 1 we must use frame -1 to index, this also means we are referencing the last index when we append
    try: #Added try if i is out of range meaning we hit the ground
        if y_pos[i] < 0: #An end condition for the animation if y drops below zero/hits the ground
            pass
        else:
            x_pos, y_pos, v_y = update_points(x_pos, y_pos, v_x, v_y, i)
            line.set_data(x_pos,y_pos) #Update the data of the line
    except IndexError:
        pass
    try:
        if y_pos_max[i] < 0:
            pass
        else:
            x_pos_max, y_pos_max, v_y_max = update_points(x_pos_max, y_pos_max, v_x_max, v_y_max, i)
            line_max.set_data(x_pos_max, y_pos_max)
    except IndexError:
        pass
    return line, line_max


def init_func(): 
    #This function is passed to the Func Animation function to initialise the graph
    global line, ax, line_max
    ax.set_title('Projectile Simulation')
    ax.set_xlabel('x /m')
    ax.set_ylabel('y /m')
    ax.grid()
    ax.plot(x_ap, highest_y, '-bx', label = 'inputted apogee') #Plot the apogee
    ax.plot(x_ap_max, highest_y_max, '-rx', label = 'max range apogee') #Plot max range apogee
    ax.plot(highest_x, 0.0, '-b.', label = 'inputted range')
    ax.plot(highest_x_max, 0.0, '-r.', label = 'max range')
    line, = ax.plot(x_pos,y_pos, color = 'blue', label = 'inputted trajectory') 
    line_max, = ax.plot(x_pos_max, y_pos_max, color = 'red', label = 'max range trajectory')
    


#Making a graph function so that it can be called easily with GUI
def graph(theta, u, h):
    global v_x, v_y, x_pos, y_pos, g, dt, fig, ax, T, highest_y, highest_x, x_ap
    global v_x_max, v_y_max, x_pos_max, y_pos_max, highest_y_max, highest_x_max, x_ap_max
    #theta = launch angle from horizontal in degrees
    #g = strength of gravity in m/s^2
    #u = launch speed in m/s
    #h = launch height in m

    dt = 0.005 #time step in s
    theta = math.radians(theta) #turns theta into radians for calculations

    theta_max = math.asin(1/(math.sqrt(2+((2*g*h)/(u**2))))) #Finds the angle for the maximum range

    u_x = u * math.cos(theta) # initial x velocity
    u_y = u * math.sin(theta) # initial y velocity

    u_x_max = u * math.cos(theta_max) # initial x velocity for max range
    u_y_max = u * math.sin(theta_max) # initial y velocity for max range

    v_x = u_x # since x velocity doesn't change this is not an array
    v_y = np.array([u_y]) # Velocity array

    v_x_max = u_x_max # X velocity for max range
    v_y_max = np.array([u_y_max]) #y velocity array for max range

    x_pos = np.array([0.0]) # array of x positions relative to origin during flight /m
    y_pos = np.array([float(h)]) # array of y positions relative to origin during flight /m
    
    x_pos_max = np.array([0.0]) # array of x positions relative to origin during flight /m - max range
    y_pos_max = np.array([float(h)]) # array of y positions relative to origin during flight /m - max range
    

    #Before I start making the graph I must work out the time until the ball hits the ground
    #This is so that I can calculate how many frames I need with this time interval
    #I will do this using the concept that y = h + u_y*t - 0.5*g*(t**2) with y becoming 0
    a = -0.5 * g
    b = u_y
    c = h
    #We will only focus on the - case of the quadratic equation because 2a will always be negative and so will -b
    T = (-b - (math.sqrt((b**2)-4*a*c)))/(2*a) #T is the time to hit ground
    #Doing the same for max range
    a = -0.5 * g
    b = u_y_max
    c = h

    T_max = (-b - (math.sqrt((b**2)-4*a*c)))/(2*a)

    if T_max > T: #Calculates the number of frames needed based on the ball with the longest flight time
        last_frame = int((T_max//dt) + 1)*10#Calculates the number of frames needed, adding 1 to ensure it rounds up
    else:
        last_frame = int((T//dt) + 1)*10#Calculates the number of frames needed, adding 1 to ensure it rounds up
    highest_x = T * v_x #Calculating the highest x for the normal ball
    highest_x_max = T_max * v_x_max #Calculates highest x for max range
    #Finding the apogee using v**2 = u**2 - 2gs 
    # u**2/2g = s
    highest_y = (u_y**2)/(2*g) + h 
    x_ap = (u_x*u_y)/g #x at the apogee since time at apogee is u_y/g

    highest_y_max = (u_y_max**2)/(2*g) + h #Same for max range ball
    x_ap_max = (u_x_max*u_y_max)/g

    s = find_distance(u,g,theta, highest_x) #Distance traveled by normal ball
    s_max = find_distance(u,g,theta_max, highest_x_max)   #Distance travelled at max range

    T_label.config(text = 'Inputted ball T = '+ str(T) + 's')
    T_max_label.config(text = 'Max range ball T = '+ str(T_max) + 's')
    theta_max_label.config(text = 'Max range ball angle = ' + str(math.degrees(theta_max)) + '/degrees')
    highest_x_label.config(text = 'Inputted ball range R = ' + str(highest_x) + 'm')
    highest_x_max_label.config(text = 'Max range R = ' + str(highest_x_max) + 'm')
    s_label.config(text = 'Inputted ball distance traveled S = '+ str(s) + 'm')
    s_label_max.config(text = 'Max range ball distance traveled S = '+ str(s_max) + 'm')


    fig, ax = plt.subplots() #Initialises the axes and figure
    ani = FuncAnimation(fig, func= update_frame, frames = range(last_frame),init_func=init_func(),blit = True, interval = 3, repeat = False) #Makes the animation
    if highest_y_max < highest_y: #Finds which apogee is highest and uses it for scale
        plt.axis([0,(highest_x_max//1)+1,0,(highest_y//1)+1]) #Setting axis range - using range of max range ball for x scale
    else:
        plt.axis([0,(highest_x_max//1)+1,0,(highest_y_max//1)+1]) #Setting axis range - using range of max range ball for x scale

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
                error_label.config(text = 'Ensure g > 0, u >= 0, h >= 0 and -90 <= theta <= 90')
                error_label.pack() #Puts the label in the window
        except ValueError: #If values can't be converted into floats, tell the user to make sure all data is numerical
            error_label.config(text = 'Ensure all data is numerical')
            error_label.pack() #Puts the label in the window

    else: #If the text box is empty is enters an error message
        error_label.config(text = 'Ensure all data is filled')
        error_label.pack() #Puts the label in the window

enter_button = Button(root,text = 'Finalise data', command= clicked) #Create the labels
theta_label = Label(root, text= 'Enter the launch angle from the horizontal in degrees: ') 
g_label = Label(root, text= 'Enter the strength of gravity in m/s^2: ')
u_label = Label(root, text= 'Enter the launch speed in m/s: ')
h_label = Label(root, text='Enter the launch height in m: ')
error_label = Label(root, text = 'Ensure all data is entered correctly')
T_label = Label(root, text = 'Inputted ball T = ')
T_max_label = Label(root, text = 'Max Range ball T = ')
theta_max_label = Label(root, text = 'Max range ball angle = ')
highest_x_label = Label(root, text = 'Inputted ball range R = ')
highest_x_max_label = Label(root, text = 'Max range R = ')
s_label = Label(root, text = 'Inputted ball distance traveled S = ')
s_label_max = Label(root, text = 'Max range ball distance traveled S = ')
theta_label.pack() #Add all the buttons and labels and entry boxes in the correct order
theta_entry.pack()
g_label.pack()
g_entry.pack()
u_label.pack()
u_entry.pack()
h_label.pack()
h_entry.pack()
enter_button.pack()
error_label.pack()
T_label.pack()
T_max_label.pack()
theta_max_label.pack()
highest_x_label.pack()
highest_x_max_label.pack()
s_label.pack()
s_label_max.pack()

root.mainloop() #Display window and start mainloop