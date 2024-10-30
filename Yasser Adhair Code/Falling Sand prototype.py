#Controls:
#   1-5: selecting particles (can also click boxes)
#   p: place mode
#   t: temperature mode
#   +: increase brush size
#   -: decrease brush size
#   up arrow: increase temperature change
#   down arrow: lower temperature change
#   Temperature change displayed in terminal
#   Change SCREEN_WIDTH and SCREEN_HEIGHT to change window size
#   Change grid_width to change resolution of particles (increase for more pixels)


import pygame
import ctypes
import numpy as np
import random
import cProfile #optimisation

ctypes.windll.user32.SetProcessDPIAware() #Makes resolution standard

pygame.init()

#Setting screen sizes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

#Possible positions for pixel 
grid_width = 50
pixel_size = int((SCREEN_WIDTH/grid_width)//1)
grid_height = int((SCREEN_HEIGHT/pixel_size)//1)

#Rate at which heat transfers
transfer_rate = 0.005

#Colours for the game
black = (0,0,0)
sand_color = (194, 178, 128)
water_color = (28,163,236)
air_color = (50,50,50)
iron_color = (161, 157, 148)
oil_color = (219,207,92)
ice_color = (214, 255, 250)
steam_color = (60,60,70)
frozen_oil_color = (255,247,164)
frozen_air_color = (255,255,255)
molten_sand_color = (229,101,32)
pig_iron_color = (255,37,0)
liquid_air_color = (255,255,255)
oil_vapour_color = (116,118,60)
sand_vapour_color = (152,41,0)
iron_vapour_color = (159,89,89)
UI_air_color = (255,255,255)
UI_select_color = (255,0,0)

#Events
NULL_EVENT = pygame.USEREVENT + 1 #Place holder event
class events(): 
    WATER_ICE = pygame.USEREVENT + 2 #Water to ice
    WATER_STEAM = pygame.USEREVENT + 3 #Water to steam
    ICE_WATER = pygame.USEREVENT + 4 #ETC
    STEAM_WATER = pygame.USEREVENT + 5
    OIL_FROZEN_OIL = pygame.USEREVENT + 6
    OIL_OIL_VAPOUR = pygame.USEREVENT + 7
    FROZEN_OIL_OIL = pygame.USEREVENT + 8
    OIL_VAPOUR_OIL = pygame.USEREVENT + 9
    SAND_MOLTEN_SAND = pygame.USEREVENT + 10
    MOLTEN_SAND_SAND_VAPOUR = pygame.USEREVENT + 11
    SAND_VAPOUR_MOLTEN_SAND = pygame.USEREVENT + 12
    MOLTEN_SAND_SAND = pygame.USEREVENT + 13
    IRON_PIG_IRON = pygame.USEREVENT + 14
    PIG_IRON_IRON_VAPOUR = pygame.USEREVENT + 15
    PIG_IRON_IRON = pygame.USEREVENT + 16
    IRON_VAPOUR_PIG_IRON = pygame.USEREVENT + 17
    AIR_LIQUID_AIR = pygame.USEREVENT + 18
    LIQUID_AIR_FROZEN_AIR = pygame.USEREVENT + 19
    LIQUID_AIR_AIR = pygame.USEREVENT + 20
    FROZEN_AIR_LIQUID_AIR = pygame.USEREVENT + 21
class particle(): #Base particle class, all other particle classes will inherit this class
    def __init__(self, x_pos, y_pos,array_pos,temp=None) -> None:
        self.name = ''
        self.array_pos = array_pos #Position in particle array
        if temp == None: #Sets base temperature at 20*C if being placed by player
            self.temp = 293.0
        else: #This case is for when particles are changing state
            self.temp = temp
        self.state_down = 0 #The temperature at which it will go to lower state (gas -> liquid -> solid)
        self.state_up = 100000 #Temperature at which it will go to higher state (solid -> liquid -> gas)
        #Actual position
        self.x_pos = x_pos 
        self.y_pos = y_pos
        #Position in grid
        self.grid_x_pos = int(x_pos//pixel_size)
        self.grid_y_pos = int(y_pos//pixel_size)
        #Positions on screen
        self.screen_x_pos = (x_pos//pixel_size) * pixel_size
        self.screen_y_pos = (y_pos//pixel_size) * pixel_size
        #Visualisation shape
        self.rect = pygame.Rect(self.screen_x_pos, self.screen_y_pos, pixel_size, pixel_size)
        self.event_up = NULL_EVENT #Event that is triggered when it goes up in state
        self.event_down = NULL_EVENT #Event triggered when it goes down in state
    def new_y_pos(self, grid_y_pos): #Function for updating the y position when the particle is swapped because of density or temperature
        self.grid_y_pos = grid_y_pos
        self.y_pos = grid_y_pos * pixel_size
        self.screen_y_pos = (self.y_pos//pixel_size) * pixel_size
        self.rect.y = self.screen_y_pos
    def update_pos_y(self,change, swapped): #For when a particle falls or sinks below something less dense or hotter
        #Actual position + change
        self.y_pos = self.y_pos + change 
        #Position in grid before change
        previous_grid = self.grid_y_pos
        self.grid_y_pos = (self.y_pos//pixel_size) #Position in grid after change
        if self.grid_y_pos != previous_grid: #Checks if grid position has changed
            if swapped == True: #If it has displaced a particle
                grid[int(self.grid_x_pos)][int(self.grid_y_pos)].new_y_pos(previous_grid) #updates all values of a particle if it has been swapped due to density difference
                
            grid[int(self.grid_x_pos)][int(previous_grid)], grid[int(self.grid_x_pos)][int(self.grid_y_pos)] = grid[int(self.grid_x_pos)][int(self.grid_y_pos)], grid[int(self.grid_x_pos)][int(previous_grid)] #Swaps position in the grid
            
        #Positions on screen
        self.screen_y_pos = (self.y_pos//pixel_size) * pixel_size #updates position on screen
        #Visualisation shape
        self.rect.y = self.screen_y_pos #updates position of rectangle on screen
    def update_x_pos(self,x_pos, swapped): #Sand as update_pos_y but for x
        self.x_pos = x_pos
        #Position in grid
        previous_grid = self.grid_x_pos
        self.grid_x_pos = (self.x_pos//pixel_size)
        if self.grid_x_pos != previous_grid:
            if swapped == True:
                grid[int(self.grid_x_pos)][int(self.grid_y_pos)].new_x_pos(previous_grid) #updates all values of a particle if it has been swapped due to density difference
            grid[int(previous_grid)][int(self.grid_y_pos)], grid[int(self.grid_x_pos)][int(self.grid_y_pos)] = grid[int(self.grid_x_pos)][int(self.grid_y_pos)], grid[int(previous_grid)][int(self.grid_y_pos)]
            
        #Positions on screen
        self.screen_x_pos = (self.x_pos//pixel_size) * pixel_size
        #Visualisation shape
        self.rect.x = self.screen_x_pos
    def new_x_pos(self,grid_x_pos): #changes the x_pos of a particle
        self.grid_x_pos = grid_x_pos
        self.x_pos = grid_x_pos * pixel_size
        self.screen_x_pos = (self.x_pos//pixel_size) * pixel_size
        self.rect.x = self.screen_x_pos 
    def transfer_heat_x(self): #Transfers heat in x direction
        if self.grid_x_pos == grid_width-1:
            return
        temp2 = grid[int(self.grid_x_pos)+1][int(self.grid_y_pos)]
        if temp2 != None:
            change = self.temp * transfer_rate
            change2 = temp2.temp * transfer_rate
            self.temp += change2 - change
            temp2.temp += change - change2
    def check_state(self):#Triggers events for state changes
        if self.temp > self.state_up: 
            #Passes parameters to event to update corret pixel
            pygame.event.post(pygame.event.Event(self.event_up,x_pos=self.x_pos, y_pos = self.y_pos, grid_x_pos = self.grid_x_pos,grid_y_pos = self.grid_y_pos,array_pos = self.array_pos,temp=self.temp))
            return
        elif self.temp < self.state_down:
            pygame.event.post(pygame.event.Event(self.event_down,x_pos=self.x_pos, y_pos = self.y_pos, grid_x_pos = self.grid_x_pos,grid_y_pos = self.grid_y_pos,array_pos = self.array_pos,temp=self.temp))
            return
        else:
            return

class solid(particle): #Parent class for all solids
    def __init__(self, x_pos, y_pos, array_pos,temp=None) -> None:
        particle.__init__(self,x_pos,y_pos,array_pos,temp) #Inherits most attributes and function from partile
        self.is_solid = True #Simple solid condition
        self.density = 0 #Its density
        self.strength = 1 #How high it can stack before toppling
        self.topple_speed = 0.5 * (pixel_size/FPS)*FPS #How fast it topples
    def check_below_empty(self): #Function to check if there is a particle below, is different for liquids and gasses
        if self.grid_y_pos == grid_height-1: #If it is on the border of the screen
            return False, False
        temp = grid[int(self.grid_x_pos)][int(self.grid_y_pos+1)] #stores the grid space below it
        if temp == None: #if it is empty below
            return True, False
        elif temp.density < self.density and temp.is_solid == False: #A denser solid can only displace a less dense non-solid
            #They exchange heat
            change = self.temp * transfer_rate
            change2 = temp.temp * transfer_rate
            self.temp += change2 - change
            temp.temp += change - change2
            return True, True
        else: #If it is not empty below
            change = self.temp * transfer_rate
            change2 = temp.temp * transfer_rate
            self.temp += change2 - change
            temp.temp += change - change2
            return False, False
    def check_topple(self): #For checking if the particle needs to topple
        temp_right = False
        temp_left = False
        if self.grid_y_pos >= grid_height - self.strength:
            return False, None
        else: #Decides possible flow direction for particle, for topple here must be a non solid or empty space there
            if self.grid_x_pos != grid_width-1 and self.grid_x_pos != 0:
                if grid[int(self.grid_x_pos)+1][int(self.grid_y_pos)+self.strength] == None:
                    temp_right = True
                elif grid[int(self.grid_x_pos)+1][int(self.grid_y_pos)+self.strength].is_solid == False:
                    temp_right = True
                if grid[int(self.grid_x_pos)-1][int(self.grid_y_pos)+self.strength] == None:
                    temp_left = True
                elif grid[int(self.grid_x_pos)-1][int(self.grid_y_pos)+self.strength].is_solid == False:
                    temp_left = True
            elif self.grid_x_pos == grid_width-1:
                if grid[int(self.grid_x_pos)-1][int(self.grid_y_pos)+self.strength] == None:
                    temp_left = True
                elif grid[int(self.grid_x_pos)-1][int(self.grid_y_pos)+self.strength].is_solid == False:
                    temp_left = True
            elif self.grid_x_pos == 0:
                if grid[int(self.grid_x_pos)+1][int(self.grid_y_pos)+self.strength] == None:
                    temp_right = True
                elif grid[int(self.grid_x_pos)+1][int(self.grid_y_pos)+self.strength].is_solid == False:
                    temp_right = True
            if temp_left == True: #Returning which directions it can topple
                if temp_right == True:
                    return True, None
                else:
                    return True, False
            elif temp_right == True:
                return True, True
            else:
                return False, False
                
    def topple(self,right_flowing): #Topples solid
        self.right_flowing = right_flowing 
        if self.right_flowing == None:
            self.right_flowing = bool(random.getrandbits(1)) #Randomly decides flow direction
        if self.right_flowing == True:
            if grid[int(self.grid_x_pos+1)][int(self.grid_y_pos)] == None: #Checks if it needs to displace a particle
                swapped = False 
                x_pos = self.x_pos + self.topple_speed
                self.update_x_pos(x_pos, swapped)
            elif grid[int(self.grid_x_pos+1)][int(self.grid_y_pos)].density < self.density and grid[int(self.grid_x_pos+1)][int(self.grid_y_pos)].is_solid == False: 
                swapped = True
                x_pos = self.x_pos + self.topple_speed
                self.update_x_pos(x_pos, swapped)

        elif self.right_flowing == False:
            if grid[int(self.grid_x_pos-1)][int(self.grid_y_pos)] == None:
                swapped = False
                x_pos = self.x_pos - self.topple_speed
                self.update_x_pos(x_pos, swapped)
            elif grid[int(self.grid_x_pos-1)][int(self.grid_y_pos)].density < self.density and grid[int(self.grid_x_pos-1)][int(self.grid_y_pos)].is_solid == False:
                swapped = True
                x_pos = self.x_pos - self.topple_speed
                self.update_x_pos(x_pos, swapped)

class liquid(particle): #Parent class for liquids
    def __init__(self, x_pos, y_pos, array_pos,temp=None) -> None:
        particle.__init__(self,x_pos,y_pos, array_pos,temp) #Inherits particle
        self.density = 0 #Density in kg/m^3
        self.is_solid = False
        self.flow_speed = 0
        self.right_flowing = bool(random.getrandbits(1)) #Randomly decides flow direction
    def check_below_empty(self): #Function to check if there is a particle below, same as before but ignores whether or not it is solid
        if self.grid_y_pos == grid_height-1:
            return False, False
        temp = grid[int(self.grid_x_pos)][int(self.grid_y_pos+1)]
        if temp == None:
            return True, False
        elif temp.density < self.density or (temp.density == self.density and temp.temp > self.temp):
            change = self.temp * transfer_rate
            change2 = temp.temp * transfer_rate
            self.temp += change2 - change
            temp.temp += change - change2
            return True, True
        else:
            change = self.temp * transfer_rate
            change2 = temp.temp * transfer_rate
            self.temp += change2 - change
            temp.temp += change - change2
            return False, False
    def flow(self): #Handles flowing
        if self.grid_x_pos == grid_width-1:
            self.right_flowing = False
        elif self.grid_x_pos == 0:
            self.right_flowing = True
        if self.right_flowing == True:
            if grid[int(self.grid_x_pos+1)][int(self.grid_y_pos)] == None:
                swapped = False
                x_pos = self.x_pos + self.flow_speed
                self.update_x_pos(x_pos, swapped)
            elif grid[int(self.grid_x_pos+1)][int(self.grid_y_pos)].density < self.density:
                swapped = True
                x_pos = self.x_pos + self.flow_speed
                self.update_x_pos(x_pos, swapped)
            else:
                self.right_flowing = False
        elif self.right_flowing == False:
            if grid[int(self.grid_x_pos-1)][int(self.grid_y_pos)] == None:
                swapped = False
                x_pos = self.x_pos - self.flow_speed
                self.update_x_pos(x_pos, swapped)
            elif grid[int(self.grid_x_pos-1)][int(self.grid_y_pos)].density < self.density:
                swapped = True
                x_pos = self.x_pos - self.flow_speed
                self.update_x_pos(x_pos, swapped)
            else:
                self.right_flowing = True

class gas(liquid): #Parent class for gasses
    def __init__(self, x_pos, y_pos,array_pos,temp=None) -> None:
        super().__init__(x_pos, y_pos,array_pos,temp)
        self.bounce_chance = 60 #chance of gas bouncing when space above is empty
        self.small_bounce = (0.1 * pixel_size)//1
        self.big_bounce = 1*pixel_size - (self.small_bounce)
    def check_above_empty(self): #Function to check if there is a particle below, will be expanded to use a set to increase efficiency
        if self.grid_y_pos == 0:
            return False, False
        temp = grid[int(self.grid_x_pos)][int(self.grid_y_pos-1)]
        if temp == None:
            return True, False
        elif temp.density < self.density:
            return True, True
        else:
            return False, False
    def flow(self): #Handles flowing but adds bouncing up
        global bounce_random_i
        liquid.flow(self)
        bounce_random_i = (bounce_random_i + 1)%10000
        if bounce_random[bounce_random_i] < self.bounce_chance:
            empty_above, swapping = self.check_above_empty()
            if empty_above == True:
                change = self.small_bounce + ((bounce_random[-bounce_random_i]/100) * self.big_bounce)
                self.update_pos_y(-change,swapping)

#Lists all current particles
class sand(solid):
    def __init__(self, x_pos, y_pos,array_pos,temp=None) -> None:
        solid.__init__(self,x_pos,y_pos,array_pos,temp)
        self.density = 1602.0 #Density in kg/m^3
        self.state_up = 1973.0
        self.name = 'sand'
        self.strength = 1
        self.topple_speed = 0.9*(pixel_size/FPS)*FPS
        self.event_up = events.SAND_MOLTEN_SAND

class iron(solid):
    def __init__(self, x_pos, y_pos,array_pos,temp=None) -> None:
        super().__init__(x_pos, y_pos,array_pos,temp)
        self.density = 7800.0
        self.state_up = 1538.0
        self.name = 'iron'
        self.strength = 30
        self.topple_speed = 0.5* (pixel_size/FPS)*FPS
        self.event_up = events.IRON_PIG_IRON
    def check_topple(self):
        return False, False

class ice(solid):
    def __init__(self, x_pos, y_pos,array_pos,temp=None) -> None:
        super().__init__(x_pos, y_pos,array_pos,temp)
        self.density = 917.0
        self.temp = 273.0
        self.state_up = 273.0
        self.name = 'ice'
        self.strength = 30
        self.topple_speed = 0.5* (pixel_size/FPS)*FPS
        self.event_up = events.ICE_WATER
    def check_topple(self):
        return False, False

class frozen_oil(solid):
    def __init__(self, x_pos, y_pos, array_pos,temp=None):
        super().__init__(x_pos, y_pos, array_pos,temp)
        self.density = 980.0
        self.temp = 263.0
        self.state_up = 263.0
        self.name = 'frozen_oil'
        self.strength = 3
        self.event_up = events.FROZEN_OIL_OIL

class frozen_air(solid):
    def __init__(self, x_pos, y_pos, array_pos,temp=None):
        super().__init__(x_pos, y_pos, array_pos,temp)
        self.density = 1026.0
        self.temp = 50.0
        self.state_up = 50.0
        self.name = 'frozen_air'
        self.strength = 30
        self.event_up = events.FROZEN_AIR_LIQUID_AIR
    def check_topple(self):
        return False, False


class water(liquid):
    def __init__(self, x_pos, y_pos,array_pos,temp=None) -> None:
        liquid.__init__(self,x_pos,y_pos,array_pos,temp)
        self.name = 'water'
        self.state_down = 273.0
        self.state_up = 373.0
        self.density = 977.0 #Density in kg/m^3
        self.flow_speed = 0.5*(pixel_size/FPS)*FPS #Gets a flow speed
        self.event_up = events.WATER_STEAM
        self.event_down = events.WATER_ICE

class oil(liquid):
    def __init__(self, x_pos, y_pos,array_pos,temp=None) -> None:
        super().__init__(x_pos, y_pos,array_pos,temp)
        self.name = 'oil'
        self.state_down = 263.0
        self.state_up = 673.0
        self.density = 750.0
        self.flow_speed = 0.6*(pixel_size/FPS)*FPS
        self.event_up = events.OIL_OIL_VAPOUR
        self.event_down = events.OIL_FROZEN_OIL

class molten_sand(liquid):
    def __init__(self, x_pos, y_pos, array_pos,temp=None):
        super().__init__(x_pos, y_pos, array_pos,temp)
        self.name = 'molten_sand'
        self.temp = 1973.0
        self.state_down = 1973.0
        self.state_up = 2230.0
        self.density = 2080.0
        self.flow_speed = 0.2*(pixel_size/FPS)*FPS
        self.event_up = events.MOLTEN_SAND_SAND_VAPOUR
        self.event_down = events.MOLTEN_SAND_SAND

class pig_iron(liquid):
    def __init__(self, x_pos, y_pos, array_pos,temp=None):
        super().__init__(x_pos, y_pos, array_pos,temp)
        self.name = 'pig_iron'
        self.temp = 1538.0
        self.state_down = 1538.0
        self.state_up = 2861.0
        self.density = 6980.0
        self.flow_speed = 0.2*(pixel_size/FPS)*FPS
        self.event_up = events.PIG_IRON_IRON_VAPOUR
        self.event_down = events.PIG_IRON_IRON

class liquid_air(liquid):
    def __init__(self, x_pos, y_pos, array_pos,temp=None):
        super().__init__(x_pos, y_pos, array_pos,temp)
        self.name = 'liquid_air'
        self.temp = 77.0
        self.state_down = 50.0
        self.state_up = 77.0
        self.density = 870.0
        self.flow_speed = 0.5*(pixel_size/FPS)*FPS
        self.event_up = events.LIQUID_AIR_AIR
        self.event_down = events.LIQUID_AIR_FROZEN_AIR
    

class air(gas):
    def __init__(self, x_pos, y_pos,array_pos,temp=None) -> None:
        super().__init__(x_pos, y_pos,array_pos,temp)
        self.name = 'air'
        self.state_down = 77.0
        self.density = 1.3
        self.flow_speed = 0.5*(pixel_size/FPS)*FPS #Gets a flow speed
        self.bounce_chance = 60 #chance of gas bouncing when space above is empty
        self.small_bounce = (0.1 * pixel_size)//1
        self.big_bounce = 1*pixel_size - (self.small_bounce)
        self.event_down = events.AIR_LIQUID_AIR

class steam(gas):
    def __init__(self, x_pos, y_pos,array_pos,temp=None) -> None:
        super().__init__(x_pos, y_pos,array_pos,temp)
        self.name = 'steam'
        self.temp = 373.0
        self.state_down = 373.0
        self.density = 0.5974
        self.flow_speed = 0.5*(pixel_size/FPS)*FPS #Gets a flow speed
        self.bounce_chance = 60 #chance of gas bouncing when space above is empty
        self.small_bounce = (0.1 * pixel_size)//1
        self.big_bounce = 1*pixel_size - (self.small_bounce)
        self.event_down = events.STEAM_WATER

class oil_vapour(gas):
    def __init__(self, x_pos, y_pos,array_pos,temp=None) -> None:
        super().__init__(x_pos, y_pos,array_pos,temp)
        self.name = 'oil_vapour'
        self.temp = 673.0
        self.state_down = 673.0
        self.density = 0.7
        self.flow_speed = 0.5*(pixel_size/FPS)*FPS #Gets a flow speed
        self.bounce_chance = 60 #chance of gas bouncing when space above is empty
        self.small_bounce = (0.1 * pixel_size)//1
        self.big_bounce = 1*pixel_size - (self.small_bounce)
        self.event_down = events.OIL_VAPOUR_OIL

class sand_vapour(gas):
    def __init__(self, x_pos, y_pos,array_pos,temp=None) -> None:
        super().__init__(x_pos, y_pos,array_pos,temp)
        self.name = 'sand_vapour'
        self.temp = 2230.0
        self.state_down = 2230.0
        self.density = 1.0
        self.flow_speed = 0.4*(pixel_size/FPS)*FPS #Gets a flow speed
        self.bounce_chance = 60 #chance of gas bouncing when space above is empty
        self.small_bounce = (0.1 * pixel_size)//1
        self.big_bounce = 1*pixel_size - (self.small_bounce)
        self.event_down = events.SAND_VAPOUR_MOLTEN_SAND

class iron_vapour(gas):
    def __init__(self, x_pos, y_pos,array_pos,temp=None) -> None:
        super().__init__(x_pos, y_pos,array_pos,temp)
        self.name = 'iron_vapour'
        self.temp = 2861.0
        self.state_down = 2861.0
        self.density = 1.5
        self.flow_speed = 0.3*(pixel_size/FPS)*FPS #Gets a flow speed
        self.bounce_chance = 60 #chance of gas bouncing when space above is empty
        self.small_bounce = (0.1 * pixel_size)//1
        self.big_bounce = 1*pixel_size - (self.small_bounce)
        self.event_down = events.IRON_VAPOUR_PIG_IRON


#Initising grid of pixels
temp_array = np.full(grid_height, None)
grid = np.full((grid_width, grid_height), None)
#Initialising random values
bounce_random = []
for i in range(0,10000):
    bounce_random.append(random.randrange(100))
bounce_random = np.array(bounce_random)
bounce_random_i = 0

#Initialise screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pixel_array = []
#UI values
UI_select_start_x = 10
UI_select_start_y = 10
UI_select_spacing = 15
UI_select_particle_size = 50
UI_sand = pygame.Rect(UI_select_start_x+((UI_select_spacing+UI_select_particle_size)*0),UI_select_start_y,UI_select_particle_size,UI_select_particle_size)
UI_water = pygame.Rect(UI_select_start_x+((UI_select_spacing+UI_select_particle_size)*1),UI_select_start_y,UI_select_particle_size,UI_select_particle_size)
UI_air = pygame.Rect(UI_select_start_x+((UI_select_spacing+UI_select_particle_size)*2),UI_select_start_y,UI_select_particle_size,UI_select_particle_size)
UI_iron = pygame.Rect(UI_select_start_x+((UI_select_spacing+UI_select_particle_size)*3),UI_select_start_y,UI_select_particle_size,UI_select_particle_size)
UI_oil = pygame.Rect(UI_select_start_x+((UI_select_spacing+UI_select_particle_size)*4),UI_select_start_y,UI_select_particle_size,UI_select_particle_size)
UI_select_rect = pygame.Rect(UI_select_start_x+((UI_select_spacing+UI_select_particle_size)*0),UI_select_start_y,UI_select_particle_size+10,UI_select_particle_size+10)
UI_select_sand_pos_x = UI_sand.x -5
UI_select_sand_pos_y = UI_sand.y -5
UI_select_water_pos_x = UI_water.x -5
UI_select_water_pos_y = UI_water.y -5
UI_select_air_pos_x = UI_air.x -5
UI_select_air_pos_y = UI_air.y -5
UI_select_iron_pos_x = UI_iron.x -5
UI_select_iron_pos_y = UI_iron.y -5
UI_select_oil_pos_x = UI_oil.x -5
UI_select_oil_pos_y = UI_oil.y -5

#Set FPS and clock
FPS = 120
falling_velocity = 0.9*pixel_size #Falls by x pixel per frame, gravity system with forces not present for prototype. can't be above 1 pixel per frame


def main_game_loop(): #added a main game loop function for testing
    clock = pygame.time.Clock()
    run = True
    mouse_down = False
    element_selected = 'sand'
    placing = True
    place_square = 1
    mode = 'place'
    temp_change = 10
    def draw_screen(): #Update screen function
        screen.fill(black)
        for pixel in pixel_array:
            match pixel.name:
                case 'sand':
                    pygame.draw.rect(screen, sand_color, pixel.rect)  # Draws sand pixel on screen
                case 'water':
                    pygame.draw.rect(screen, water_color, pixel.rect)  # Draws water pixel on screen
                case 'air':
                    pygame.draw.rect(screen, air_color, pixel.rect)  # Draws air pixel on screen
                case 'iron':
                    pygame.draw.rect(screen, iron_color, pixel.rect)  # Draws iron pixel on screen
                case 'oil':
                    pygame.draw.rect(screen, oil_color, pixel.rect)  # Draws oil pixel on screen
                case 'ice':
                    pygame.draw.rect(screen, ice_color, pixel.rect)  # Draws ice pixel on screen
                case 'steam':
                    pygame.draw.rect(screen, steam_color, pixel.rect)  # Draws steam pixel on screen
                case 'frozen_oil':
                    pygame.draw.rect(screen, frozen_oil_color, pixel.rect)  # Draws frozen oil pixel on screen
                case 'frozen_air':
                    pygame.draw.rect(screen, frozen_air_color, pixel.rect)  # Draws frozen air pixel on screen
                case 'molten_sand':
                    pygame.draw.rect(screen, molten_sand_color, pixel.rect)  # Draws molten sand pixel on screen
                case 'pig_iron':
                    pygame.draw.rect(screen, pig_iron_color, pixel.rect)  # Draws pig iron pixel on screen
                case 'liquid_air':
                    pygame.draw.rect(screen, liquid_air_color, pixel.rect)  # Draws liquid air pixel on screen
                case 'oil_vapour':
                    pygame.draw.rect(screen, oil_vapour_color, pixel.rect)  # Draws oil vapour pixel on screen
                case 'sand_vapour':
                    pygame.draw.rect(screen, sand_vapour_color, pixel.rect)  # Draws sand vapour pixel on screen
                case 'iron_vapour':
                    pygame.draw.rect(screen, iron_vapour_color, pixel.rect)  # Draws iron vapour pixel on screen

        match element_selected:
            case 'sand':
                UI_select_rect.x = UI_select_sand_pos_x
                UI_select_rect.y = UI_select_sand_pos_y
            case 'water':
                UI_select_rect.x = UI_select_water_pos_x
                UI_select_rect.y = UI_select_water_pos_y
            case 'air':
                UI_select_rect.x = UI_select_air_pos_x
                UI_select_rect.y = UI_select_air_pos_y
            case 'iron':
                UI_select_rect.x = UI_select_iron_pos_x
                UI_select_rect.y = UI_select_iron_pos_y
            case 'oil':
                UI_select_rect.x = UI_select_oil_pos_x
                UI_select_rect.y = UI_select_oil_pos_y
        pygame.draw.rect(screen,UI_select_color, UI_select_rect)
        pygame.draw.rect(screen, sand_color,UI_sand)
        pygame.draw.rect(screen, water_color,UI_water)
        pygame.draw.rect(screen, UI_air_color,UI_air)
        pygame.draw.rect(screen, iron_color,UI_iron)
        pygame.draw.rect(screen, oil_color,UI_oil)
        pygame.display.update()

    while run == True: #Main game loop continues while run is true
        clock.tick(FPS) #Starts next frame
        #print(clock.get_fps())
        print(temp_change)
        for event in pygame.event.get(): #Handles all events
            if event.type == pygame.QUIT:
                run = False #Lets the player quit
            elif event.type == pygame.MOUSEBUTTONDOWN: #Places sand if mouse button is down
                mouse_down = True #Allows the user to hold down the mouse button to create sand
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    element_selected = 'sand'
                elif event.key == pygame.K_2:
                    element_selected = 'water'
                elif event.key == pygame.K_3:
                    element_selected = 'air'
                elif event.key == pygame.K_4:
                    element_selected = 'iron'
                elif event.key == pygame.K_5:
                    element_selected = 'oil'
                elif event.key == pygame.K_t:
                    mode = 'temp'
                elif event.key == pygame.K_p:
                    mode = 'place'
                elif event.key == pygame.K_EQUALS: #Increases the size of the placement square
                    place_square += 1
                elif event.key == pygame.K_MINUS: #Decreases the size of the placement square
                    if place_square > 1:
                        place_square += -1
                elif event.key == pygame.K_UP:
                    temp_change += 10
                elif event.key == pygame.K_DOWN:
                    temp_change += -10
            else:
                match event.type:
                    case events.WATER_ICE:
                        pixel_array[event.array_pos] = ice(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.WATER_STEAM:
                        pixel_array[event.array_pos] = steam(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.ICE_WATER:
                        pixel_array[event.array_pos] = water(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.STEAM_WATER:
                        pixel_array[event.array_pos] = water(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.OIL_FROZEN_OIL:
                        pixel_array[event.array_pos] = frozen_oil(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.OIL_OIL_VAPOUR:
                        pixel_array[event.array_pos] = oil_vapour(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.FROZEN_OIL_OIL:
                        pixel_array[event.array_pos] = oil(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.OIL_VAPOUR_OIL:
                        pixel_array[event.array_pos] = oil(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.SAND_MOLTEN_SAND:
                        pixel_array[event.array_pos] = molten_sand(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.MOLTEN_SAND_SAND_VAPOUR:
                        pixel_array[event.array_pos] = sand_vapour(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.SAND_VAPOUR_MOLTEN_SAND:
                        pixel_array[event.array_pos] = molten_sand(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.MOLTEN_SAND_SAND:
                        pixel_array[event.array_pos] = sand(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.IRON_PIG_IRON:
                        pixel_array[event.array_pos] = pig_iron(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.PIG_IRON_IRON_VAPOUR:
                        pixel_array[event.array_pos] = iron_vapour(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.PIG_IRON_IRON:
                        pixel_array[event.array_pos] = iron(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.IRON_VAPOUR_PIG_IRON:
                        pixel_array[event.array_pos] = pig_iron(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.AIR_LIQUID_AIR:
                        pixel_array[event.array_pos] = liquid_air(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.LIQUID_AIR_FROZEN_AIR:
                        pixel_array[event.array_pos] = frozen_air(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.LIQUID_AIR_AIR:
                        pixel_array[event.array_pos] = air(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]

                    case events.FROZEN_AIR_LIQUID_AIR:
                        pixel_array[event.array_pos] = liquid_air(event.x_pos, event.y_pos, event.array_pos,event.temp)
                        grid[int(event.grid_x_pos)][int(event.grid_y_pos)] = pixel_array[event.array_pos]
                    case _:
                        continue


        if mouse_down == True:
            placing = True
            xy_list = pygame.mouse.get_pos()
            mouse_x = int(xy_list[0]) #Gets the actual physical position of the mouse when the sand is place
            mouse_y = int(xy_list[1])
            if mouse_y > UI_sand.y and mouse_y < UI_sand.y + UI_select_particle_size:
                if mouse_x > UI_sand.x and mouse_x < UI_sand.x + UI_select_particle_size:
                    element_selected = 'sand'
                    placing = False
                elif mouse_x > UI_water.x and mouse_x < UI_water.x + UI_select_particle_size:
                    element_selected = 'water'
                    placing = False
                elif mouse_x > UI_air.x and mouse_x < UI_air.x + UI_select_particle_size:
                    element_selected = 'air'
                    placing = False
                elif mouse_x > UI_iron.x and mouse_x < UI_iron.x + UI_select_particle_size:
                    element_selected = 'iron'
                    placing = False
                elif mouse_x > UI_oil.x and mouse_x < UI_oil.x + UI_select_particle_size:
                    element_selected = 'oil'
                    placing = False
            if placing == True:
                grid_mouse_x_pos = int(mouse_x//pixel_size) #Finds the position in the grid
                grid_mouse_y_pos = int(mouse_y//pixel_size)
                for place_x in range(0,place_square): #finds the x offset of a position in the place square
                    place_x = grid_mouse_x_pos + place_x - (place_square//2) #offsets further so that mouse is roughly in centre of square
                    for place_y in range(0,place_square): #finds the y offset of a position in the place square
                        place_y = grid_mouse_y_pos + place_y - (place_square//2)
                        if place_x > grid_width-1 or place_x < 0 or place_y > grid_height-1 or place_y < 0:
                            continue
                        else:
                            if grid[place_x][place_y] == None:
                                if mode == 'place':
                                    temp_pos = len(pixel_array)
                                    if element_selected == 'sand': #Checks if that grid position is empty
                                        pixel_array.append(sand(place_x * pixel_size, place_y * pixel_size,temp_pos)) #Appends a pixel to the rendering array
                                        grid[place_x][place_y] = pixel_array[-1] #Replaces empty grid with sand
                                    elif element_selected == 'water':
                                        pixel_array.append(water(place_x * pixel_size, place_y * pixel_size,temp_pos)) #Appends a pixel to the rendering array
                                        grid[place_x][place_y] = pixel_array[-1] #Replaces empty grid with water
                                    elif element_selected == 'air':
                                        pixel_array.append(air(place_x * pixel_size, place_y * pixel_size,temp_pos)) #Appends a pixel to the rendering array
                                        grid[place_x][place_y] = pixel_array[-1] #Replaces empty grid with water
                                    elif element_selected == 'iron':
                                        pixel_array.append(iron(place_x * pixel_size, place_y * pixel_size,temp_pos)) #Appends a pixel to the rendering array
                                        grid[place_x][place_y] = pixel_array[-1] #Replaces empty grid with water
                                    elif element_selected == 'oil':
                                        pixel_array.append(oil(place_x * pixel_size, place_y * pixel_size,temp_pos)) #Appends a pixel to the rendering array
                                        grid[place_x][place_y] = pixel_array[-1] #Replaces empty grid with water
                            else:
                                if mode == 'temp':
                                    grid[place_x][place_y].temp += temp_change
        for pixel in pixel_array: #Iterate through every particle
            empty_below, swapping = pixel.check_below_empty() #Check if the pixel can fall
            pixel.transfer_heat_x()
            if empty_below == True: #If it is empty then the pixel falls
                pixel.update_pos_y(falling_velocity, swapping)
            else:
                if pixel.is_solid == False:
                    pixel.flow()
                else:
                    toppling, right_flowing = pixel.check_topple()
                    if toppling == True:
                        pixel.topple(right_flowing)
        for pixel in pixel_array: #added secondary loop for changing states to prevent positional clashes
            pixel.check_state()


                
        draw_screen() #Renders everything

if __name__ == '__main__':
    cProfile.run('main_game_loop()')