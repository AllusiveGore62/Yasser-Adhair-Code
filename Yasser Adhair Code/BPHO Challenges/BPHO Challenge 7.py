#Importing libraries
import matplotlib as mpl #Matplotlib for graphing
import matplotlib.pyplot as plt #Function for actually plotting the graphs
import numpy as np #Useful for arrays
import math #For all the trigonometric calculations
from matplotlib.ticker import MultipleLocator #Useful for setting fixed axses scales
from matplotlib.animation import FuncAnimation #Used for animating the plot
from tkinter import * #Used for GUI






def update_frame(frame):
    #Update_frame will be passed to the animation function because it needs a function that will return a new line for each frame
    #The way FuncAnimation handles the local variables in the update frame function is strange so I have to move most variables to global scope
    global ball_30, ball_45, ball_60, ball_70, ball_78, ball_85, time
    i = frame #Because frame starts at 1 we must use frame -1 to index, this also means we are referencing the last index when we append
    time = np.append(time, time[i]+dt) #Add new time

    #Update points for all balls
    ball_30.update_points(dt, i)
    ball_45.update_points(dt, i)
    ball_60.update_points(dt, i)
    ball_70.update_points(dt, i)
    ball_78.update_points(dt, i)
    ball_85.update_points(dt, i)

    #set new data for displacement lines
    line_30.set_data(ball_30.x_pos, ball_30.y_pos)
    line_45.set_data(ball_45.x_pos, ball_45.y_pos)
    line_60.set_data(ball_60.x_pos, ball_60.y_pos)
    line_70.set_data(ball_70.x_pos, ball_70.y_pos)
    line_78.set_data(ball_78.x_pos, ball_78.y_pos)
    line_85.set_data(ball_85.x_pos, ball_85.y_pos)

    #set new data for range lines
    rline_30.set_data(time, ball_30.range)
    rline_45.set_data(time, ball_45.range)
    rline_60.set_data(time, ball_60.range)
    rline_70.set_data(time, ball_70.range)
    rline_78.set_data(time, ball_78.range)
    rline_85.set_data(time, ball_85.range)
    #Returns all lines
    return line_30, line_45, line_60, line_70, line_78, line_85, rline_30, rline_45, rline_60, rline_70, rline_78, rline_85
    
#I decided to use a class structure since there are many different trajectories so it would be tedious to name them all seperately and repeat so much code
class ball:
    def __init__(self, u, theta):
        self.theta = math.radians(theta) #turns theta into radians for calculations
        self.u_x = u * math.cos(self.theta) # initial x velocity
        self.u_y = u * math.sin(self.theta) # initial y velocity

        self.v_x = self.u_x # since x velocity doesn't change this is not an array
        self.v_y = np.array([self.u_y]) # Velocity array

        self.x_pos = np.array([0.0]) # array of x positions relative to origin during flight /m
        self.y_pos = np.array([0.0]) # array of y positions relative to origin during flight /m

        self.range = np.array([0.0]) # array of range in m
    def find_range(self): #Finds and updates range
        x = self.x_pos[-1]
        y = self.y_pos[-1]
        self.range = np.append(self.range, math.sqrt((x**2)+(y**2)))
    def update_points(self, dt, i): #Made a function to update points to make it easier to code the update_frame function with multiple lines and class instances
        #np.append is formatted like array = np.append(array, item you want to add to array) and it returns a new array with the item in it.
        #np arrays are used because it is a lot more compatable with matplotlib graphs
        self.x_pos = np.append(self.x_pos, self.x_pos[i] + (self.v_x * dt))  #Find next x coordinate and append it
        self.y_pos = np.append(self.y_pos, self.y_pos[i] + (self.v_y[i] * dt)) #Find next y coordinate and append it
        self.v_y = np.append(self.v_y, self.v_y[i] - (g * dt)) #Calculate new y velocity
        self.find_range()   
    def find_max(self,u,g): #Finding the the range graph
        t = 1.5 * (u/g) * (math.sin(self.theta) + math.sqrt((math.sin(self.theta)**2)-(8/9))) #Calculating the time
        x = self.v_x * t #Multiplying the time by the x velocity to get the x-coordinate
        r = math.sqrt(((u**2)*(t**2))-(g*(t**3)*u*math.sin(self.theta)) + (0.25 * (g**2) * (t**4))) #Calculating the range at that point
        y = math.sqrt((r**2)-(x**2)) #Using the x coordinate and range to find the y coordinate
        self.x_max = x
        self.y_max = y
        self.t_max = t
        self.r_max = r
        return x, y, t, r
    def find_min(self,u,g): #Finding the minimum on the range graph
        t = 1.5 * (u/g) * (math.sin(self.theta) - math.sqrt((math.sin(self.theta)**2)-(8/9))) #Calculating the time
        x = self.v_x * t #Multiplying the time by the x velocity to get the x-coordinate
        r = math.sqrt(((u**2)*(t**2))-(g*(t**3)*u*math.sin(self.theta)) + (0.25 * (g**2) * (t**4))) #Calculating the range at that point
        y = math.sqrt((r**2)-(x**2)) #Using the x coordinate and range to find the y coordinate
        self.x_min = x
        self.y_min = y
        self.t_min = t
        self.r_min = r
        return x, y, t, r


def init_func(): 
    #This function is passed to the Func Animation function to initialise the graph
    global line_30,line_45, line_60, line_70, line_78, line_85, axs, axr
    global rline_30, rline_45, rline_60, rline_70, rline_78, rline_85, g
    axs.set_title('Projectile Simulation, y vs x')
    axs.set_xlabel('x /m')
    axs.set_ylabel('y /m')
    axs.grid()
    axr.set_title('Projectile Simulation, r vs t')
    axr.set_xlabel('t /s')
    axr.set_ylabel('Range /m')
    axr.grid()
    line_30, = axs.plot(ball_30.x_pos, ball_30.y_pos, color='blue', label='30*')
    line_45, = axs.plot(ball_45.x_pos, ball_45.y_pos, color='green', label='45*')
    line_60, = axs.plot(ball_60.x_pos, ball_60.y_pos, color='red', label='60*')
    line_70, = axs.plot(ball_70.x_pos, ball_70.y_pos, color='cyan', label='70.5*')
    line_78, = axs.plot(ball_78.x_pos, ball_78.y_pos, color='purple', label='78*')
    line_85, = axs.plot(ball_85.x_pos, ball_85.y_pos, color='lime', label='85*')

    rline_30, = axr.plot(time, ball_30.range, color='blue', label='30*')
    rline_45, = axr.plot(time, ball_45.range, color='green', label='45*')
    rline_60, = axr.plot(time, ball_60.range, color='red', label='60*')
    rline_70, = axr.plot(time, ball_70.range, color='cyan', label='70.5*')
    rline_78, = axr.plot(time, ball_78.range, color='purple', label='78*')
    rline_85, = axr.plot(time, ball_85.range, color='lime', label='85*')

    x,y,t,r = ball_70.find_max(u_temp,g) #Plotting the maximum for 70.5*
    axs.plot(x, y, 'rx') #On displacement graph
    axr.plot(t, r, 'rx') #On range graph
    ball_70_label_max_x.config(text= '(X,Y) = (' + str(x) + ','+ str(y) +') m')
    ball_70_label_max_t.config(text= 'T = ' + str(t) + 's')
    ball_70_label_max_r.config(text= 'R = ' + str(r) + 'm')
    x,y,t,r = ball_78.find_max(u_temp,g) #Plotting the maximum for 78*
    axs.plot(x, y, 'rx')
    axr.plot(t, r, 'rx')
    ball_78_label_max_x.config(text= '(X,Y) = (' + str(x) + ','+ str(y) +') m')
    ball_78_label_max_t.config(text= 'T = ' + str(t) + 's')
    ball_78_label_max_r.config(text= 'R = ' + str(r) + 'm')
    x,y,t,r = ball_85.find_max(u_temp,g) #Plotting the maximum for 85*
    axs.plot(x, y, 'rx')
    axr.plot(t, r, 'rx')
    ball_85_label_max_x.config(text= '(X,Y) = (' + str(x) + ','+ str(y) +') m')
    ball_85_label_max_t.config(text= 'T = ' + str(t) + 's')
    ball_85_label_max_r.config(text= 'R = ' + str(r) + 'm')
    x,y,t,r = ball_70.find_min(u_temp,g) #Plotting the minimum for 70.5*
    axs.plot(x, y, 'bx') #On displacement graph
    axr.plot(t, r, 'bx') #On range graph
    ball_70_label_min_x.config(text= '(X,Y) = (' + str(x) + ','+ str(y) +') m')
    ball_70_label_min_t.config(text= 'T = ' + str(t) + 's')
    ball_70_label_min_r.config(text= 'R = ' + str(r) + 'm')
    x,y,t,r = ball_78.find_min(u_temp,g) #Plotting the minimum for 78*
    axs.plot(x, y, 'bx')
    axr.plot(t, r, 'bx')
    ball_78_label_min_x.config(text= '(X,Y) = (' + str(x) + ','+ str(y) +') m')
    ball_78_label_min_t.config(text= 'T = ' + str(t) + 's')
    ball_78_label_min_r.config(text= 'R = ' + str(r) + 'm')
    x,y,t,r = ball_85.find_min(u_temp,g) #Plotting the minimum for 85*
    axs.plot(x, y, 'bx')
    axr.plot(t, r, 'bx')
    ball_85_label_min_x.config(text= '(X,Y) = (' + str(x) + ','+ str(y) +') m')
    ball_85_label_min_t.config(text= 'T = ' + str(t) + 's')
    ball_85_label_min_r.config(text= 'R = ' + str(r) + 'm')
    



#Making a graph function so that it can be called easily with GUI
def graph(u):
    global g, dt, fig, axs, axs_lim, ball_30,ball_45, ball_60, ball_70, ball_78, ball_85, axr, time, u_temp
    #theta = launch angle from horizontal in degrees
    #g = strength of gravity in m/s^2  
    #u = launch speed in m/s
    #h = launch height in m
    u_temp = u
    dt = 0.01 #time step in s
    time = np.array([0.0]) #Array of time
    #Initialising all the balls
    turning_point = math.asin((2*math.sqrt(2))/3)
    turning_point = math.degrees(turning_point)
    ball_30 = ball(u, 30)
    ball_45 = ball(u, 45)
    ball_60 = ball(u, 60)
    ball_70 = ball(u, turning_point)
    ball_78 = ball(u, 78)
    ball_85 = ball(u, 85)


    #Finding the apogee using v**2 = u**2 - 2gs 
    # u**2/2g = s
    highest_y = (ball_85.u_y**2)/(2*g) #Finding the highest y so we can scale the axses


    #Before I start making the graph I must work out the time until the ball hits the ground, using the 85* ball since it will be in the air the longest
    #This is so that I can calculate how many frames I need with this time interval
    #I will do this using the concept that y = h + u_y*t - 0.5*g*(t**2) with y becoming 0
    
    a = -0.5 * g
    b = ball_85.u_y
    c = (highest_y//1)+1 #This is here because I want the animation to end when it hits the bottom of the scale
    #We will only focus on the - case of the quadratic equation because 2a will always be negative and so will -b
    T = (-b - (math.sqrt((b**2)-4*a*c)))/(2*a) #T is the time to hit ground
    last_frame = int((T//dt) + 1)*10#Calculates the number of frames needed, adding 1 to ensure it rounds up

    #Doing this again for the X_axis scale
    a = -0.5 * g
    b = ball_30.u_y #Using ball 30 because it will travel the furthest
    c = (highest_y//1)+1
    T = (-b - (math.sqrt((b**2)-4*a*c)))/(2*a)

    highest_x = T * ball_30.v_x #Calculating the highest x for accurate scale

    axs_lim = -highest_y//1
    fig, [axs,axr] = plt.subplots(1,2) #Initialises the axes and figure
    ani = FuncAnimation(fig, func= update_frame, frames = range(last_frame),init_func=init_func(),blit = True, interval = 3, repeat = False) #Makes the animation
    axs.axis([0,(highest_x//1)+1,(-highest_y//1),(highest_y//1)+1]) #Setting axis range
    axr.axis([0, (3*(u/g)), 0, (u/g) * 30])
    plt.legend()
    plt.subplots_adjust(wspace=0.4)
    plt.show() #Shows the graph and animation

root = Tk() #Intialising window


g_entry = Entry(root, width=50) #Input box for gravity
u_entry = Entry(root, width=50) #Input box for initial speed
error_label = Label(root, text = 'Ensure all data is correct')

def clicked(): #Function for if the enter_button is clicked
    global g, error_label #Makes g global for other variables
    #Gets the values from each text box
    g = g_entry.get()
    u = u_entry.get()
    if len(g) != 0 and len(u) != 0: #Ensures they are not empty
        try: #Tries to convert the values into floats
            g = float(g)
            u = float(u)
            if g > 0 and u >= 0: #Checks if data is valid
                graph(u) #Outputs the graph
            else: #Tells the user to make sure all data is valid
                error_label.config(text = 'Ensure g > 0, u >= 0')
                
        except IndexError: #If values can't be converted into floats, tell the user to make sure all data is numerical
            error_label.config(text = 'Ensure all data is numerical')
            

    else: #If the text box is empty is enters an error message
        error_label.config(text = 'Ensure all data is filled')
        

enter_button = Button(root,text = 'Finalise data', command= clicked) #Create the labels
g_label = Label(root, text= 'Enter the strength of gravity in m/s^2: ')
u_label = Label(root, text= 'Enter the launch speed in m/s: ')

ball_70_label = Label(root, text= 'Range stats for 70.5* ball: ')

ball_70_label_max = Label(root, text= 'Local maximum: ')

ball_70_label_max_x = Label(root, text= '(X,Y) = ')
ball_70_label_max_t = Label(root, text= 'T = ')
ball_70_label_max_r = Label(root, text= 'R = ')

ball_70_label_min = Label(root, text= 'Local minimum: ')

ball_70_label_min_x = Label(root, text= '(X,Y) = ')
ball_70_label_min_t = Label(root, text= 'T = ')
ball_70_label_min_r = Label(root, text= 'R = ')

ball_78_label = Label(root, text= 'Range stats for 78* ball: ')

ball_78_label_max = Label(root, text= 'Local maximum: ')

ball_78_label_max_x = Label(root, text= '(X,Y) = ')
ball_78_label_max_t = Label(root, text= 'T = ')
ball_78_label_max_r = Label(root, text= 'R = ')

ball_78_label_min = Label(root, text= 'Local minimum: ')

ball_78_label_min_x = Label(root, text= '(X,Y) = ')
ball_78_label_min_t = Label(root, text= 'T = ')
ball_78_label_min_r = Label(root, text= 'R = ')

ball_85_label = Label(root, text= 'Range stats for 85* ball: ')

ball_85_label_max = Label(root, text= 'Local maximum: ')

ball_85_label_max_x = Label(root, text= '(X,Y) = ')
ball_85_label_max_t = Label(root, text= 'T = ')
ball_85_label_max_r = Label(root, text= 'R = ')

ball_85_label_min = Label(root, text= 'Local minimum: ')

ball_85_label_min_x = Label(root, text= '(X,Y) = ')
ball_85_label_min_t = Label(root, text= 'T = ')
ball_85_label_min_r = Label(root, text= 'R = ')



#Add all the buttons and labels and entry boxes in the correct order
g_label.pack()
g_entry.pack()
u_label.pack()
u_entry.pack()
enter_button.pack()
error_label.pack()
ball_70_label.pack()
ball_70_label_max.pack()
ball_70_label_max_x.pack()
ball_70_label_max_t.pack()
ball_70_label_max_r.pack()
ball_70_label_min.pack()
ball_70_label_min_x.pack()
ball_70_label_min_t.pack()
ball_70_label_min_r.pack()
ball_78_label.pack()
ball_78_label_max.pack()
ball_78_label_max_x.pack()
ball_78_label_max_t.pack()
ball_78_label_max_r.pack()
ball_78_label_min.pack()
ball_78_label_min_x.pack()
ball_78_label_min_t.pack()
ball_78_label_min_r.pack()
ball_85_label.pack()
ball_85_label_max.pack()
ball_85_label_max_x.pack()
ball_85_label_max_t.pack()
ball_85_label_max_r.pack()
ball_85_label_min.pack()
ball_85_label_min_x.pack()
ball_85_label_min_t.pack()
ball_85_label_min_r.pack()

root.mainloop() #Display window and start mainloop