#Importing libraries
import matplotlib as mpl #Matplotlib for graphing
import matplotlib.pyplot as plt #Function for actually plotting the graphs
import numpy as np #Useful for arrays
import math #For all the trigonometric calculations
from matplotlib.ticker import MultipleLocator #Useful for setting fixed axes scales
from matplotlib.animation import FuncAnimation #Used for animating the plot
from tkinter import * #Used for GUI

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

    global v_x_min, v_x_low, v_x_high, v_y_min, v_y_low, v_y_high, x_pos_min, x_pos_low, x_pos_high, y_pos_min, y_pos_low, y_pos_high
    global y_pos_max, x_pos_max, v_x_max, v_y_max
    i = frame #Because frame starts at 1 we must use frame -1 to index, this also means we are referencing the last index when we append
    try:
        if y_pos_max[i] < 0:
            pass
        else:
            x_pos_max, y_pos_max, v_y_max = update_points(x_pos_max, y_pos_max, v_x_max, v_y_max, i)
            line_max.set_data(x_pos_max, y_pos_max)
    except IndexError:
        pass
    try: #Added try if i is out of range meaning at least one of the balls hit the desired point

        #Various if statements will check if the ball is within range and will check index went out of range using the try statement 
        #These checks are ordered: high then min then low because the low ball will always hit first follow by min then high 
        #This means that if the low ball hits then it will keep the same line while the other two can still keep moving.
        if  y_pos_high[i] >= 0: #high ball check
            x_pos_high, y_pos_high, v_y_high = update_points(x_pos_high, y_pos_high, v_x_high,v_y_high, i) 
            line_high.set_data(x_pos_high,y_pos_high) #Update the data of the line
        

        if y_pos_min[i] >= 0: #min ball check
            x_pos_min, y_pos_min, v_y_min = update_points(x_pos_min, y_pos_min, v_x_min,v_y_min, i)
            line_min.set_data(x_pos_min,y_pos_min) #Update the data of the line


        if y_pos_low[i] >= 0: #low ball check
            x_pos_low, y_pos_low, v_y_low = update_points(x_pos_low, y_pos_low, v_x_low,v_y_low, i)
            line_low.set_data(x_pos_low,y_pos_low) #Update the data of the line

    except IndexError:
        pass
    return line_min, line_low, line_high, line_max, #returns the lines to the animation function
        


def init_func(): 
    #This function is passed to the Func Animation function to initialise the graph
    global line_min, line_low, line_high, ax, root, line_max
    ax.set_title('Projectile Simulation, stats in other tab')
    ax.set_xlabel('x /m')
    ax.set_ylabel('y /m')
    ax.grid()
    ax.plot(x_ap_min,highest_y_min, color = 'grey', marker = 'x', linestyle = '-', label = 'minimum u apogee')
    ax.plot(x_ap_low,highest_y_low, color = 'orange', marker = 'x', linestyle = '-', label = 'low ball apogee')
    ax.plot(x_ap_high,highest_y_high, '-bx', label = 'high ball apogee')
    ax.plot(x_ap_max, highest_y_max, '-rx', label = 'max range apogee') #Plot max range apogee
    ax.plot(highest_x,target_Y, '-go', label = 'target')
    ax.plot(highest_x_max, 0.0, '-r.', label = 'max range')
    
    ax.plot(bounding_x,bounding_y, linestyle = 'dashed',color = 'pink', label = 'Bounding parabola')

    line_min, = ax.plot(x_pos_min,y_pos_min, color = 'grey', label = 'min u')
    line_low, = ax.plot(x_pos_low,y_pos_low, color = 'orange', label = 'low ball')
    line_high, = ax.plot(x_pos_high,y_pos_high, color = 'blue', label = 'high ball')
    line_max, = ax.plot(x_pos_max, y_pos_max, color = 'red', label = 'max range trajectory')


#Making a graph function so that it can be called easily with GUI
def graph(X, Y_real, u, h):
    global v_x_min, v_x_low, v_x_high, v_y_min, v_y_low, v_y_high, x_pos_min, x_pos_low, x_pos_high, y_pos_min, y_pos_low, y_pos_high, g, dt, fig, ax, T_min, T_low, T_high, highest_x
    global x_ap_min,x_ap_low, x_ap_high, highest_y_min, highest_y_low, highest_y_high,T_min_label, T_low_label, T_high_label, min_u_label
    global v_x_max, v_y_max, x_pos_max, y_pos_max, highest_y_max, highest_x_max, x_ap_max
    global bounding_x, bounding_y
    #X = Desired x-coordinate
    #Y = Desired y-coordinate  
    #g = strength of gravity in m/s^2
    #u = launch speed in m/s
    #h = launch height in m
    Y = Y_real - h
    dt = 0.01 #time step in s
    min_u_theta = math.atan((Y+math.sqrt((X**2)+(Y**2)))/(X)) #Calculates theta for mininimum u scenario
    min_u = math.sqrt(g)*math.sqrt(Y+math.sqrt((X**2)+(Y**2))) #Calculates mininimum u
    theta_max = math.asin(1/(math.sqrt(2+((2*g*h)/(u**2))))) #Finds the angle for the maximum range


    u_x_min = min_u * math.cos(min_u_theta) # initial x velocity for minimum u
    u_y_min = min_u * math.sin(min_u_theta) # initial y velocity for minimum u
    #Using quadratic equation to find minimum and maximum theta (low and high ball)
    a = (g/(2*(u**2)))*(X**2)
    b = -X
    c = Y + (g*(X**2))/(2*(u**2))

    theta_low = math.atan((-b-math.sqrt((b**2)-4*a*c))/(2*a)) #Theta if it's a low ball
    theta_high = math.atan((-b+math.sqrt((b**2)-4*a*c))/(2*a)) #Theta if it's a high ball

    u_x_low = u * math.cos(theta_low) # initial x velocity for low ball
    u_y_low = u * math.sin(theta_low) # initial y velocity for low ball

    u_x_high = u * math.cos(theta_high) # initial x velocity for high ball
    u_y_high = u * math.sin(theta_high) # initial y velocity for high ball

    u_x_max = u * math.cos(theta_max) # initial x velocity for max range
    u_y_max = u * math.sin(theta_max) # initial y velocity for max range

    v_x_min = u_x_min # since x velocity doesn't change this is not an array - This is for minimum u
    v_y_min = np.array([u_y_min]) # y-velocity array for minimum u

    v_x_low = u_x_low # x-velocity for low ball
    v_y_low = np.array([u_y_low]) # y-velocity array for low ball

    v_x_high = u_x_high # x-velocity for high ball
    v_y_high = np.array([u_y_high]) # y-velocity array for high ball

    v_x_max = u_x_max # X velocity for max range
    v_y_max = np.array([u_y_max]) #y velocity array for max range

    # arrays of x positions relative to origin during flight /m
    # arrays of y positions relative to origin during flight /m
    x_pos_min = np.array([0.0]) #x for minimum u
    y_pos_min = np.array([float(h)]) #y for minimum u

    x_pos_low = np.array([0.0]) #x for low ball
    y_pos_low = np.array([float(h)]) #y for low ball
    
    x_pos_high = np.array([0.0]) #x for high ball
    y_pos_high = np.array([float(h)]) #y for high ball

    x_pos_max = np.array([0.0]) # array of x positions relative to origin during flight /m - max range
    y_pos_max = np.array([float(h)]) # array of y positions relative to origin during flight /m - max range

    #Before I start making the graph I must work out the time until the ball hits the ground
    #This is so that I can calculate how many frames I need with this time interval
    #I will do this using the concept that y = h + u_y*t - 0.5*g*(t**2) with y becoming the value Y
    a = -0.5 * g
    b = u_y_min
    c = h - Y_real #We will use the unadjusted value of Y rather than the Y from a relative frame.
    #We will only focus on the - case of the quadratic equation because 2a will always be negative and so will -b
    T_min = (-b - (math.sqrt((b**2)-4*a*c)))/(2*a) #T_min is the time to hit ground for minimum u

    #We will repeat this for each trajectory
    a = -0.5 * g
    b = u_y_low
    c = h - Y_real
    T_low = (-b - (math.sqrt((b**2)-4*a*c)))/(2*a) #T_low is the time to hit ground

    a = -0.5 * g
    b = u_y_high
    c = h - Y_real
    T_high = (-b - (math.sqrt((b**2)-4*a*c)))/(2*a) #T_low is the time to hit ground

    a = -0.5 * g
    b = u_y_max
    c = h

    T_max = (-b - (math.sqrt((b**2)-4*a*c)))/(2*a)

    last_frame = int((T_high//dt) + 1)*10#Calculates the number of frames needed, adding 1 to ensure it rounds up. We use high-ball's time because it will be in the air the longest

    highest_x = X 
    highest_x_max = T_max * v_x_max
    #Finding the apogee using v**2 = u**2 - 2gs 
    # u**2/2g = s
    #We will find the apogee for all trajectories (using the same method as the analytical model)
    highest_y_min = (u_y_min**2)/(2*g) + h 
    highest_y_low = (u_y_low**2)/(2*g) + h     
    highest_y_high = (u_y_high**2)/(2*g) + h 
    highest_y_max = (u_y_max**2)/(2*g) + h #Same for max range ball

    x_ap_min = (u_x_min*u_y_min)/g #x at the apogee since time at apogee is u_y/g - min ball
    x_ap_low = (u_x_low*u_y_low)/g # low ball
    x_ap_high = (u_x_high*u_y_high)/g # high ball
    x_ap_max = (u_x_max*u_y_max)/g # Max rangle ball

    #Updating information on GUI
    T_min_label.config(text= 'Minimum velocity T = '+ str(T_min) + 's')
    T_low_label.config(text = 'Low ball T = '+ str(T_low) + 's')
    T_high_label.config(text = 'High ball T = '+ str(T_high) + 's')
    T_max_label.config(text = 'Max range ball T = '+ str(T_max) + 's')
    min_u_label.config(text = 'Min u = ' + str(min_u) + 'm/s')
    min_u_theta_label.config(text = 'Min speed angle = ' + str(math.degrees(min_u_theta)) + '/degrees')
    theta_low_label.config(text = 'Low ball angle = ' + str(math.degrees(theta_low)) + '/degrees')
    theta_high_label.config(text = 'High ball angle = ' + str(math.degrees(theta_high)) + '/degrees')
    theta_max_label.config(text = 'Max range ball angle = ' + str(math.degrees(theta_max)) + '/degrees')    
    highest_x_max_label.config(text = 'Max range = ' + str(highest_x_max) + 'm')

    #Calculating points for bounding parabola
    dx = highest_x_max/500 #The step between each point
    bounding_x = np.arange(0,highest_x_max,dx) #Equally spaced array of x coordinates
    bounding_y = np.array([])
    for x in bounding_x: #Iterating through x coordinates
        y = ((u**2)/(2*g))-((g/(2*(u**2)))*(x**2)) + h #Finding corresponding y coordinate
        bounding_y = np.append(bounding_y, y)
    

    fig, ax = plt.subplots() #Initialises the axes and figure

    ani = FuncAnimation(fig, func= update_frame, frames = range(last_frame),init_func=init_func(),blit = True, interval = 3, repeat = False) #Makes the animation

    plt.axis([0,((1.2*highest_x_max)//1)+1,0,((1.1*highest_y_high)//1)+1]) #Setting axis range, using high ball for y limit
    plt.legend(loc = 'upper right') 
    plt.show() #Shows the graph and animation

root = Tk() #Intialising window

X_entry = Entry(root, width = 50) #Input box for X
g_entry = Entry(root, width=50) #Input box for gravity
Y_entry = Entry(root, width = 50) #Input box for Y
u_entry = Entry(root, width=50) #Input box for initial speed
h_entry = Entry(root, width=50) #Input box for height
T_min_label = Label(root, text= 'Minimum speed T = ')
T_low_label = Label(root, text = 'Low ball T = ')
T_high_label = Label(root, text = 'High ball T = ')
T_max_label = Label(root, text = 'Max Range ball T = ')
min_u_label = Label(root, text = 'Min u = ')
min_u_theta_label = Label(root, text = 'Min speed angle = ')
theta_low_label = Label(root, text = 'Low ball angle = ')
theta_high_label = Label(root, text = 'High ball angle = ')
theta_max_label = Label(root, text = 'Max range ball angle = ')
highest_x_max_label = Label(root, text = 'Max range = ')
def clicked(): #Function for if the enter_button is clicked
    global g, target_Y, min_u #Makes g global for other variables
    X = X_entry.get() #Gets the values from each text box
    g = g_entry.get()
    Y = Y_entry.get()
    u = u_entry.get()
    h = h_entry.get()
    if len(X) != 0 and len(g) != 0 and len(Y) != 0 and len(u) != 0 and len(h) != 0: #Ensures they are not empty
        try: #Tries to convert the values into floats
            X = float(X)
            g = float(g)
            Y = float(Y)
            u = float(u)
            h = float(h)
            if g > 0 and u >= 0 and h >= 0 and X > 0 and Y > 0: #Checks if data is valid
                temp_Y = Y - h
                target_Y = Y #added this because there was a name clash within a function
                min_u = math.sqrt(g)*math.sqrt(temp_Y+math.sqrt((X**2)+(temp_Y**2))) #Calculates minimum u
                if min_u > u: #Checks if u is too small
                    error_label.config(text = 'u must be greater than or equal to minimum u (minimum u = ' + str(min_u) + 'm/s)') #Prompts user to put in new u and tells them min u
        
                else:
                    graph(X,Y,u,h) #Outputs the graph
            else: #Tells the user to make sure all data is valid
                error_label.config(text = 'Ensure g > 0, u >= 0, h >= 0 and X > 0 and Y > 0')
    
        except ValueError: #If values can't be converted into floats, tell the user to make sure all data is numerical
            error_label.config(text = 'Ensure all data is numerical')


    else: #If the text box is empty is enters an error message
        error_label.config(text = 'Ensure all data is filled')

enter_button = Button(root,text = 'Finalise data', command= clicked) #Create the labels
X_label = Label(root, text= 'Enter the X coordinate in m: ') 
Y_label = Label(root, text = 'Enter the Y coordinate in m: ')
g_label = Label(root, text= 'Enter the strength of gravity in m/s^2: ')
u_label = Label(root, text= 'Enter the launch speed in m/s: ')
h_label = Label(root, text='Enter the launch height in m: ')
error_label = Label(root, text = 'Ensure all data is entered correctly')

X_label.pack() #Add all the buttons and labels and entry boxes in the correct order
X_entry.pack()
Y_label.pack()
Y_entry.pack()
g_label.pack()
g_entry.pack()
u_label.pack()
u_entry.pack()
h_label.pack()
h_entry.pack()
enter_button.pack()
error_label.pack()
T_min_label.pack()
T_low_label.pack()
T_high_label.pack()
T_max_label.pack()
min_u_label.pack()
min_u_theta_label.pack()
theta_low_label.pack()
theta_high_label.pack()
theta_max_label.pack()
highest_x_max_label.pack()

root.mainloop() #Display window and start mainloop