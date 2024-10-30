#CONTROLS
# WASD: Thrusters
# Up/Down arrows: Increase/Decrease Thrust
# +/-: Increase/Decrease time step
# C: change camera angle (shuttle or Sun)



import pygame
import math 

pygame.init()
pygame.font.init()

white = (255,255,255)
black = (0,0,0)

info_font = pygame.font.SysFont('comicsans', 30)
label_font = pygame.font.SysFont('comicsans',15)

sun_label = label_font.render('Sun', 1,white)
mercury_label = label_font.render('Mercury', 1, white)
venus_label = label_font.render('Venus', 1, white)
earth_label = label_font.render('Earth', 1, white)
mars_label = label_font.render('Mars', 1, white)
jupiter_label = label_font.render('Jupiter', 1, white)
saturn_label = label_font.render('Saturn', 1, white)
uranus_label = label_font.render('Uranus', 1, white)
neptune_label = label_font.render('Neptune', 1, white)
player_label = label_font.render('Your Ship', 1, white)

def au_to_pixel(au_position):
    global pixels_per_au
    return au_position * pixels_per_au

def find_theta(m_pos):
    theta = math.atan2(m_pos[1],m_pos[0])
    return theta

def find_r(m_pos):
    r = math.hypot(m_pos[0],m_pos[1])
    return r

sun_radius_true = 0.00465047

def update_acceleration(G,M,m,r,theta, forces = None, M_radius = sun_radius_true):
    conv = 1.496*(10**11)
    if r < M_radius:
        F = 0
    else:
        r = r * conv
        r_square = r**2
        F = (G*m*M)/r_square
    a = F/m
    a = a/conv
    if forces != None:
        a_x = -a*math.cos(theta) + (forces[0]/m)
        a_y = -a*math.sin(theta) + (forces[1]/m)
    else:
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

def update_pos_player(m_pos,dt,m_v):
    m_pos[0] = m_pos[0] + dt*m_v[0]
    m_pos[1] = m_pos[1] + dt*m_v[1]
    m_dposx = dt*m_v[0]
    m_dposy = dt*m_v[1]
    m_dpos = [m_dposx,m_dposy]
    return m_pos, m_dpos

def update_pos_rel_player(player_pos,m_pos):
    rel_playerx = m_pos[0]-player_pos[0]
    rel_playery = m_pos[1]-player_pos[1]
    rel_playerx = au_to_pixel(rel_playerx)+((screenWidth/2))
    rel_playery = au_to_pixel(rel_playery)+ (screenHeight/2)
    return rel_playerx, rel_playery

def update_pos_rel_planet(player_pos,m_pos):
    rel_planetx = player_pos[0]-m_pos[0]
    rel_planety = player_pos[1]-m_pos[1]
    rel_planet = [rel_planetx,rel_planety]
    return rel_planet

#Simulation
pixels_per_au = 1000
G = 6.67*(10**-11)
#dt = 500
dt = 31540
#dt = 100000

screenWidth = 1000
screenHeight = 800
FPS = 60
white = (255,255,255)
black = (0,0,0)

#Masses
M = 1.989 * (10**30)
earth_mass = 5.9722 * (10**24)
mercury_mass = 3.285 * (10**23)
venus_mass = 4.867 * (10**24)
mars_mass = 0.64169 * (10**24)
jupiter_mass = 1898.13 * (10**24)
saturn_mass = 568.32 * (10**24)
uranus_mass = 86.811 * (10**24)
neptune_mass = 102.409 * (10**24)
player_mass = 4 * (10**5)

#Positions
M_pos = [0,0]
earth_pos = [1.0167257013,0]
player_pos = [1.13,0]
mercury_pos = [0.467 ,0]
venus_pos = [0.72821700963,0]
mars_pos = [1.66620687,0]
jupiter_pos = [5.4570496,0]
saturn_pos = [10.070511,0]
uranus_pos = [20.0630529,0]
neptune_pos = [30.4740768,0]
earth_x = au_to_pixel(earth_pos[0])+((screenWidth/2))
earth_y = au_to_pixel(earth_pos[1])+ (screenHeight/2)
player_x = au_to_pixel(player_pos[0])+((screenWidth/2))
player_y = au_to_pixel(player_pos[1])+ (screenHeight/2)
mercury_x = au_to_pixel(mercury_pos[0])+((screenWidth/2))
mercury_y = au_to_pixel(mercury_pos[1])+ (screenHeight/2)
venus_x = au_to_pixel(venus_pos[0])+((screenWidth/2))
venus_y = au_to_pixel(venus_pos[1])+ (screenHeight/2)
mars_x = au_to_pixel(mars_pos[0])+((screenWidth/2))
mars_y = au_to_pixel(mars_pos[1])+ (screenHeight/2)
jupiter_x = au_to_pixel(jupiter_pos[0])+((screenWidth/2))
jupiter_y = au_to_pixel(jupiter_pos[1])+ (screenHeight/2)
saturn_x = au_to_pixel(saturn_pos[0])+((screenWidth/2))
saturn_y = au_to_pixel(saturn_pos[1])+ (screenHeight/2)
uranus_x = au_to_pixel(uranus_pos[0])+((screenWidth/2))
uranus_y = au_to_pixel(uranus_pos[1])+ (screenHeight/2)
neptune_x = au_to_pixel(neptune_pos[0])+((screenWidth/2))
neptune_y = au_to_pixel(neptune_pos[1])+ (screenHeight/2)

#Velocities
earth_v = [0,-(1.95791561*(10**-7))]
player_v = [0,-(2.43*(10**-7))]
mercury_v = [0, -(3.07491*(10**-7))]
venus_v = [0,-(2.3248994*(10**-7))]
mars_v = [0,-(1.4686038*(10**-7))]
jupiter_v = [0,-(8.3156264*(10**-8))]
saturn_v = [0,-(6.109713*(10**-8))]
uranus_v = [0,-(4.338297*(10**-8))]
neptune_v = [0,-(3.589623*(10**-8))]

#Acceleration
earth_r = find_r(earth_pos)
earth_theta = find_theta(earth_pos)
earth_a = update_acceleration(G,M,earth_mass,earth_r,earth_theta)
player_r = find_r(player_pos)
player_theta = find_theta(player_pos)
player_a = update_acceleration(G,M,player_mass,player_r,player_theta)
mercury_r = find_r(mercury_pos)
mercury_theta = find_theta(mercury_pos)
mercury_a = update_acceleration(G,M,mercury_mass,mercury_r,mercury_theta)
venus_r = find_r(venus_pos)
venus_theta = find_theta(venus_pos)
venus_a = update_acceleration(G,M,venus_mass,venus_r,venus_theta)
mars_r = find_r(mars_pos)
mars_theta = find_theta(mars_pos)
mars_a = update_acceleration(G,M,mars_mass,mars_r,mars_theta)
jupiter_r = find_r(jupiter_pos)
jupiter_theta = find_theta(jupiter_pos)
jupiter_a = update_acceleration(G,M,jupiter_mass,jupiter_r,jupiter_theta)
saturn_r = find_r(saturn_pos)
saturn_theta = find_theta(saturn_pos)
saturn_a = update_acceleration(G,M,saturn_mass,saturn_r,saturn_theta)
uranus_r = find_r(uranus_pos)
uranus_theta = find_theta(uranus_pos)
uranus_a = update_acceleration(G,M,uranus_mass,uranus_r,uranus_theta)
neptune_r = find_r(neptune_pos)
neptune_theta = find_theta(neptune_pos)
neptune_a = update_acceleration(G,M,neptune_mass,neptune_r,neptune_theta)

#Radii
"""
mercury_radius_true = 0.0019
venus_radius_true = 0.0048
earth_radius_true = 0.005
mars_radius_true = 0.00265
jupiter_radius_true = 0.0056
saturn_radius_true = 0.024725
uranus_radius_true = 0.03
neptune_radius_true = 0.040194
sun_radius_true = 0.01
"""

mercury_radius_vis = 0.019
venus_radius_vis = 0.048
earth_radius_vis = 0.05
mars_radius_vis = 0.0265
jupiter_radius_vis = 0.056
saturn_radius_vis = 0.24725
uranus_radius_vis = 0.3
neptune_radius_vis = 0.40194
sun_radius_vis = 0.1 

mercury_radius = au_to_pixel(mercury_radius_vis)
venus_radius = au_to_pixel(venus_radius_vis)
earth_radius = au_to_pixel(earth_radius_vis)
mars_radius = au_to_pixel(mars_radius_vis)
jupiter_radius = au_to_pixel(jupiter_radius_vis)
saturn_radius = au_to_pixel(saturn_radius_vis)
uranus_radius = au_to_pixel(uranus_radius_vis)
neptune_radius = au_to_pixel(neptune_radius_vis)
sun_radius = au_to_pixel(sun_radius_vis)

mercury_radius_true = 1.63083872 * (10**-5) 
venus_radius_true = 4.04537843 * (10**-5)
earth_radius_true = 4.26352 * (10**-5)
mars_radius_true = 2.26574081 * (10**-5)
jupiter_radius_true = 0.000477895
saturn_radius_true = 0.000389256877 
uranus_radius_true = 0.000169534499 
neptune_radius_true = 0.000164587904 
sun_radius_true = 0.00465047 

#spaceship_size_vis = 0.0005
spaceship_size_vis = 0.001
spaceship_size = au_to_pixel(spaceship_size_vis)
#spaceship_thrust = 1 * (10**-6)
spaceship_thrust = 1 * (10**-7)
player_forces = [0,0]
player_x += -spaceship_size/2
player_y += -spaceship_size/2


screen = pygame.display.set_mode((screenWidth,screenHeight))
orbit = False
player = pygame.Rect((player_x,player_y,spaceship_size,spaceship_size))


def draw_screen():
    global mercury_radius, venus_radius, earth_radius, mars_radius, jupiter_radius, saturn_radius, uranus_radius, neptune_radius, sun_radius, spaceship_size, player, update_zoom

    if update_zoom == True:
        update_zoom = False

        mercury_radius = au_to_pixel(mercury_radius_vis)
        venus_radius = au_to_pixel(venus_radius_vis)
        earth_radius = au_to_pixel(earth_radius_vis)
        mars_radius = au_to_pixel(mars_radius_vis)
        jupiter_radius = au_to_pixel(jupiter_radius_vis)
        saturn_radius = au_to_pixel(saturn_radius_vis)
        uranus_radius = au_to_pixel(uranus_radius_vis)
        neptune_radius = au_to_pixel(neptune_radius_vis)
        sun_radius = au_to_pixel(sun_radius_vis)
        spaceship_size = au_to_pixel(spaceship_size_vis)

        player.width = spaceship_size
        player.height = spaceship_size

    screen.fill(black)

    pygame.draw.circle(screen, (191, 191, 191), (mercury_x, mercury_y), mercury_radius)
    pygame.draw.circle(screen, (255, 191, 128), (venus_x, venus_y), venus_radius)
    pygame.draw.circle(screen, (0, 191, 255), (earth_x, earth_y), earth_radius)
    pygame.draw.circle(screen, (255, 128, 128), (mars_x, mars_y), mars_radius)
    pygame.draw.circle(screen, (255, 255, 128), (jupiter_x, jupiter_y), jupiter_radius)
    pygame.draw.circle(screen, (255, 255, 191), (saturn_x, saturn_y), saturn_radius)
    pygame.draw.circle(screen, (128, 255, 255), (uranus_x, uranus_y), uranus_radius)
    pygame.draw.circle(screen, (128, 191, 255), (neptune_x, neptune_y), neptune_radius)
    pygame.draw.rect(screen,(255,0,0), player)

    thrust_text = info_font.render('Thrust in N: ' + str(spaceship_thrust),1,white)
    dt_text = info_font.render('dt in seconds : ' + str(dt),1,white)
    screen.blit(thrust_text, (10,10))
    screen.blit(dt_text, (screenWidth-dt_text.get_width()-10, 10))

    if camera_on_player == True:
        sun_x = au_to_pixel(-player_pos[0])+((screenWidth/2))
        sun_y = au_to_pixel(-player_pos[1])+ (screenHeight/2)
        pygame.draw.circle(screen, (255, 255, 0), (sun_x, sun_y), sun_radius)        
    else:
        sun_x = screenWidth/2
        sun_y = screenHeight/2
        pygame.draw.circle(screen, (255, 255, 0), (screenWidth/2, screenHeight/2), sun_radius)
    
    if labels == True:
        screen.blit(sun_label,(sun_x,sun_y))
        screen.blit(mercury_label, (mercury_x, mercury_y))
        screen.blit(venus_label, (venus_x, venus_y))   
        screen.blit(earth_label, (earth_x, earth_y))
        screen.blit(mars_label, (mars_x, mars_y))
        screen.blit(jupiter_label, (jupiter_x, jupiter_y))
        screen.blit(saturn_label, (saturn_x, saturn_y))
        screen.blit(uranus_label, (uranus_x, uranus_y))
        screen.blit(neptune_label, (neptune_x, neptune_y))
        screen.blit(player_label, (player.x,player.y))
    pygame.display.update()
        



clock = pygame.time.Clock()
run = True
update_zoom = False
camera_on_player = True
labels = False
while run:
    clock.tick(FPS)
    earth_v = update_v(earth_v,dt,earth_a)
    earth_pos = update_pos(earth_pos,dt,earth_v)
    earth_x = au_to_pixel(earth_pos[0])+((screenWidth/2))
    earth_y = au_to_pixel(earth_pos[1])+ (screenHeight/2)
    earth_r = find_r(earth_pos)
    earth_theta = find_theta(earth_pos)
    earth_a = update_acceleration(G,M,earth_mass,earth_r,earth_theta)

    # Mercury
    mercury_v = update_v(mercury_v, dt, mercury_a)
    mercury_pos = update_pos(mercury_pos, dt, mercury_v)
    mercury_x = au_to_pixel(mercury_pos[0])+((screenWidth/2))
    mercury_y = au_to_pixel(mercury_pos[1])+ (screenHeight/2)
    mercury_r = find_r(mercury_pos)
    mercury_theta = find_theta(mercury_pos)
    mercury_a = update_acceleration(G, M, mercury_mass, mercury_r, mercury_theta)

    # Venus
    venus_v = update_v(venus_v, dt, venus_a)
    venus_pos = update_pos(venus_pos, dt, venus_v)
    venus_x = au_to_pixel(venus_pos[0])+((screenWidth/2))
    venus_y = au_to_pixel(venus_pos[1])+ (screenHeight/2)
    venus_r = find_r(venus_pos)
    venus_theta = find_theta(venus_pos)
    venus_a = update_acceleration(G, M, venus_mass, venus_r, venus_theta)

    # Mars
    mars_v = update_v(mars_v, dt, mars_a)
    mars_pos = update_pos(mars_pos, dt, mars_v)
    mars_x = au_to_pixel(mars_pos[0])+((screenWidth/2))
    mars_y = au_to_pixel(mars_pos[1])+ (screenHeight/2)
    mars_r = find_r(mars_pos)
    mars_theta = find_theta(mars_pos)
    mars_a = update_acceleration(G, M, mars_mass, mars_r, mars_theta)

    # Jupiter
    jupiter_v = update_v(jupiter_v, dt, jupiter_a)
    jupiter_pos = update_pos(jupiter_pos, dt, jupiter_v)
    jupiter_x = au_to_pixel(jupiter_pos[0])+((screenWidth/2))
    jupiter_y = au_to_pixel(jupiter_pos[1])+ (screenHeight/2)
    jupiter_r = find_r(jupiter_pos)
    jupiter_theta = find_theta(jupiter_pos)
    jupiter_a = update_acceleration(G, M, jupiter_mass, jupiter_r, jupiter_theta)

    # Saturn
    saturn_v = update_v(saturn_v, dt, saturn_a)
    saturn_pos = update_pos(saturn_pos, dt, saturn_v)
    saturn_x = au_to_pixel(saturn_pos[0])+((screenWidth/2))
    saturn_y = au_to_pixel(saturn_pos[1])+ (screenHeight/2)
    saturn_r = find_r(saturn_pos)
    saturn_theta = find_theta(saturn_pos)
    saturn_a = update_acceleration(G, M, saturn_mass, saturn_r, saturn_theta)

    # Uranus
    uranus_v = update_v(uranus_v, dt, uranus_a)
    uranus_pos = update_pos(uranus_pos, dt, uranus_v)
    uranus_x = au_to_pixel(uranus_pos[0])+((screenWidth/2))
    uranus_y = au_to_pixel(uranus_pos[1])+ (screenHeight/2)
    uranus_r = find_r(uranus_pos)
    uranus_theta = find_theta(uranus_pos)
    uranus_a = update_acceleration(G, M, uranus_mass, uranus_r, uranus_theta)

    # Neptune
    neptune_v = update_v(neptune_v, dt, neptune_a)
    neptune_pos = update_pos(neptune_pos, dt, neptune_v)
    neptune_x = au_to_pixel(neptune_pos[0])+((screenWidth/2))
    neptune_y = au_to_pixel(neptune_pos[1])+ (screenHeight/2)
    neptune_r = find_r(neptune_pos)
    neptune_theta = find_theta(neptune_pos)
    neptune_a = update_acceleration(G, M, neptune_mass, neptune_r, neptune_theta)

    player_v = update_v(player_v, dt, player_a)
    player_pos= update_pos(player_pos, dt, player_v)
    player_x = au_to_pixel(player_pos[0])+((screenWidth/2))
    player_y = au_to_pixel(player_pos[1])+ (screenHeight/2)
    player_x += -spaceship_size/2
    player_y += -spaceship_size/2
    player.x = player_x
    player.y = player_y
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player_forces[0] = -spaceship_thrust
    elif key[pygame.K_d] == True:
        player_forces[0] = spaceship_thrust
    else:
        player_forces[0] = 0
    if key[pygame.K_s] == True:
        player_forces[1] = spaceship_thrust
    elif key[pygame.K_w] == True:
        player_forces[1] = -spaceship_thrust
    else:
        player_forces[1] = 0
    
    #Sun
    player_r = find_r(player_pos)
    player_theta = find_theta(player_pos)
    player_a = update_acceleration(G, M, player_mass, player_r, player_theta, forces = player_forces)
    if orbit == True:
        #Mercury
        player_pos_rel_mercury = update_pos_rel_planet(player_pos, mercury_pos)
        player_r_mercury = find_r(player_pos_rel_mercury)
        player_theta_mercury = find_theta(player_pos_rel_mercury)
        player_a_mercury = update_acceleration(G, mercury_mass,player_mass,player_r_mercury,player_theta_mercury,M_radius = mercury_radius_true)
        player_a[0] += player_a_mercury[0]
        player_a[1] += player_a_mercury[1]

        #Venus
        player_pos_rel_venus = update_pos_rel_planet(player_pos, venus_pos)
        player_r_venus = find_r(player_pos_rel_venus)
        player_theta_venus = find_theta(player_pos_rel_venus)
        player_a_venus = update_acceleration(G, M, player_mass, player_r_venus, player_theta_venus, M_radius=venus_radius_true)
        player_a[0] += player_a_venus[0]
        player_a[1] += player_a_venus[1]

        # Earth
        player_pos_rel_earth = update_pos_rel_planet(player_pos, earth_pos)
        player_r_earth = find_r(player_pos_rel_earth)
        player_theta_earth = find_theta(player_pos_rel_earth)
        player_a_earth = update_acceleration(G, M, player_mass, player_r_earth, player_theta_earth, M_radius=earth_radius_true)
        player_a[0] += player_a_earth[0]
        player_a[1] += player_a_earth[1]

        # Mars
        player_pos_rel_mars = update_pos_rel_planet(player_pos, mars_pos)
        player_r_mars = find_r(player_pos_rel_mars)
        player_theta_mars = find_theta(player_pos_rel_mars)
        player_a_mars = update_acceleration(G, M, player_mass, player_r_mars, player_theta_mars, M_radius=mars_radius_true)
        player_a[0] += player_a_mars[0]
        player_a[1] += player_a_mars[1]

        # Jupiter
        player_pos_rel_jupiter = update_pos_rel_planet(player_pos, jupiter_pos)
        player_r_jupiter = find_r(player_pos_rel_jupiter)
        player_theta_jupiter = find_theta(player_pos_rel_jupiter)
        player_a_jupiter = update_acceleration(G, M, player_mass, player_r_jupiter, player_theta_jupiter, M_radius=jupiter_radius_true)
        player_a[0] += player_a_jupiter[0]
        player_a[1] += player_a_jupiter[1]

        # Saturn
        player_pos_rel_saturn = update_pos_rel_planet(player_pos, saturn_pos)
        player_r_saturn = find_r(player_pos_rel_saturn)
        player_theta_saturn = find_theta(player_pos_rel_saturn)
        player_a_saturn = update_acceleration(G, M, player_mass, player_r_saturn, player_theta_saturn, M_radius=saturn_radius_true)
        player_a[0] += player_a_saturn[0]
        player_a[1] += player_a_saturn[1]

        # Uranus
        player_pos_rel_uranus = update_pos_rel_planet(player_pos, uranus_pos)
        player_r_uranus = find_r(player_pos_rel_uranus)
        player_theta_uranus = find_theta(player_pos_rel_uranus)
        player_a_uranus = update_acceleration(G, M, player_mass, player_r_uranus, player_theta_uranus, M_radius=uranus_radius_true)
        player_a[0] += player_a_uranus[0]
        player_a[1] += player_a_uranus[1]

        # Neptune
        player_pos_rel_neptune = update_pos_rel_planet(player_pos, neptune_pos)
        player_r_neptune = find_r(player_pos_rel_neptune)
        player_theta_neptune = find_theta(player_pos_rel_neptune)
        player_a_neptune = update_acceleration(G, M, player_mass, player_r_neptune, player_theta_neptune, M_radius=neptune_radius_true)
        player_a[0] += player_a_neptune[0]
        player_a[1] += player_a_neptune[1]
    if camera_on_player == True:
        player_x = screenWidth/2
        player_y = screenHeight/2
        player_x += -spaceship_size/2
        player_y += -spaceship_size/2
        player.x = player_x
        player.y = player_y
        mercury_x, mercury_y = update_pos_rel_player(player_pos, mercury_pos)
        venus_x, venus_y = update_pos_rel_player(player_pos, venus_pos)
        earth_x, earth_y = update_pos_rel_player(player_pos, earth_pos)
        mars_x, mars_y = update_pos_rel_player(player_pos, mars_pos)
        jupiter_x, jupiter_y = update_pos_rel_player(player_pos, jupiter_pos)
        saturn_x, saturn_y = update_pos_rel_player(player_pos, saturn_pos)
        uranus_x, uranus_y = update_pos_rel_player(player_pos, uranus_pos)
        neptune_x, neptune_y = update_pos_rel_player(player_pos, neptune_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            update_zoom = True
            if event.button == 4:
                pixels_per_au = pixels_per_au * 1.1
            elif event.button == 5:
                pixels_per_au = pixels_per_au / 1.1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                camera_on_player = not camera_on_player
            if event.key == pygame.K_o:
                orbit = not orbit
            if event.key == pygame.K_EQUALS:
                dt = dt * 1.25
            elif event.key == pygame.K_MINUS:
                dt = dt / 1.25
            if event.key == pygame.K_UP:
                spaceship_thrust = spaceship_thrust * 1.5
            elif event.key == pygame.K_DOWN:
                spaceship_thrust = spaceship_thrust / 1.5
            if event.key == pygame.K_l:
                labels = not labels
                
    draw_screen()

pygame.quit()
