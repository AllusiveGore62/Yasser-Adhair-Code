#CONTROLS
#   A/D: Move left and right
#   Scroll up/down: change weapon stances
#   W: Use thrusters
#   Shift: Hold to lock direction (i.e: keep aiming to one side regardless of movement)
#   Return: Press at scoreboard to restart game
#MECHANICS:
#   Lasers will appear after a certain score
#   Upgrades after a certain number of points
#   Boxes will begin to move after a certain number of points
#   Run blank scores to initialise and wipe the scoreboard


import pygame
import ctypes
import random
import math
import pickle
import sys

ctypes.windll.user32.SetProcessDPIAware()

pygame.init()
pygame.font.init()

info_font = pygame.font.SysFont('comicsans', 30)
winner_font = pygame.font.SysFont('comicsans', 70)
prompt_font = pygame.font.SysFont('comicsans',40)

def player_movement(key, player):
    global vel_y, in_air, player_offsetx_left, player_offsetx_right
    if key[pygame.K_a] == True and player.x > (0-player_offsetx_left):
        player.x += -vel_x
        if player.x -5 - gun_width >= 0 and lock_aim == False:
            switch_gun_offsetx_left()
            update_player_offsetx()
    elif key[pygame.K_d] == True and player.x < (SCREEN_WIDTH-player_offsetx_right):
        player.x += vel_x
        if player.x + player_width + 5 + gun_width <= SCREEN_WIDTH and lock_aim == False:
            switch_gun_offsetx_right()
            update_player_offsetx()
    if key[pygame.K_SPACE] == True and in_air == False:
        vel_y = vel_y_init
        player.y += vel_y
        in_air = True

def player_in_air(player):
    global in_air, vel_y, hover, hover_power
    if player.y < SCREEN_HEIGHT - player_height:
        if player.y <= 0:
            vel_y = 1
            player.y += vel_y
        elif hover == False:
            vel_y += g
            temp_vel_y = int(vel_y)
            player.y += temp_vel_y
        else:
            vel_y += g + hover_power
            temp_vel_y = int(vel_y)
            player.y += temp_vel_y
    else:
        player.y = SCREEN_HEIGHT - player_height
        in_air = False

def lower_gun():
    global gun_offsety
    if gun_offsety == gun_high:
        gun_offsety = gun_mid
    elif gun_offsety == gun_mid:
        gun_offsety = gun_low
    else:
        gun_offsety = gun_high

def raise_gun():
    global gun_offsety
    if gun_offsety == gun_low:
        gun_offsety = gun_mid
    elif gun_offsety == gun_mid:
        gun_offsety = gun_high
    else:
        gun_offsety = gun_low

def switch_gun_offsetx_left():
    global gun_offsetx, gun_offsetx_lim_left, gun_offsetx_lim_right, left_facing, pointer_offsetx
    if gun_offsetx_lim_left == 0:
        gun_offsetx_lim_left = -5 - gun_width
        gun_offsetx_lim_right = 0
        gun_offsetx = -5 - gun_width
        pointer_offsetx = -5 - gun_width - pointer.width
        left_facing = True

def switch_gun_offsetx_right():
    global gun_offsetx, gun_offsetx_lim_left, gun_offsetx_lim_right, left_facing, pointer_offsetx
    if gun_offsetx_lim_right == 0:
        gun_offsetx_lim_left = 0
        gun_offsetx_lim_right = 5 + gun_width
        gun_offsetx = 5 + player_width
        pointer_offsetx = 5 + player_width + gun_width
        left_facing = False

def update_player_offsetx():
    global player_offsetx_left, player_offsetx_right
    player_offsetx_left = 0 + gun_offsetx_lim_left
    player_offsetx_right = player_width + gun_offsetx_lim_right
    
def handle_bullets(bullets):
    global ammo, score, targets, local_score
    for index,bullet in enumerate(bullets):
        if bullet.x < player.x:
            bullet.x += - bullet_vel
            if bullet.x < 0:
                bullets.remove(bullet)

        if bullet.x > player.x:
            bullet.x += bullet_vel
            if bullet.x > SCREEN_WIDTH - bullet_width:
                bullets.remove(bullet)
        for target in targets:
            if target.colliderect(bullet):
                targets.remove(target)
                bullets.remove(bullet)
                if moving_targetx == True:
                    target_vx.remove(target_vx[index])
                if moving_targety == True:
                    target_vy.remove(target_vy[index])
                ammo += 1
                score += 1
                local_score += 1
                pygame.event.post(pygame.event.Event(generate_target))

def handle_lasersx():
    global lasersx, laser_size, player, laserx_osc
    change = 2
    for laserx in lasersx:
        if laserx.colliderect(player) and player_invincible == False:
            pygame.event.post(pygame.event.Event(player_lose_health))
        if laserx_osc*change + 5 >= laser_size:
            laserx.height += -change
            laserx.y += 0.5*change
        else:
            laserx.height += change
            laserx.y += -0.5*change
    if laserx_osc >= ((laser_size-5)/change)*2:
        lasersx = []
        laserx_osc = 1
    if len(lasersx) != 0:
            laserx_osc += 1

def handle_lasersy():
    global lasersy, laser_size, player, lasery_osc
    change = 2
    for lasery in lasersy:
        if lasery.colliderect(player) and player_invincible == False:
            pygame.event.post(pygame.event.Event(player_lose_health))
        if lasery_osc*change + 5 >= laser_size:
            lasery.width += -change
            lasery.x += 0.5*change
        else:
            lasery.width += change
            lasery.x += -0.5*change
    if lasery_osc >= ((laser_size-5)/change)*2:
        lasersy = []
        lasery_osc = 1
    if len(lasersy) != 0:
            lasery_osc += 1

def handle_pointer():
    global targets, pointer, pointer_offsetx, left_facing
    closest = SCREEN_WIDTH
    collision = False
    for target in targets:
        if target.colliderect(pointer):
            collision = True
            if left_facing == False:
                distance = abs(target.x-pointer.x)
                if distance < closest:
                    closest = distance+10
            if left_facing == True:
                distance = abs((target.x+target_size)-(pointer.x+pointer.width))
                if distance < closest:
                    closest = distance+10           
    pointer.width = closest+10
    if left_facing == True:
        pointer_offsetx = -5 - gun_width - pointer.width

def handle_targets():
    global moving_targetx, moving_targety,targets
    if moving_targetx == True:
        for index,target in enumerate(targets):
            target.x += int(target_vx[index])
            if target.x <= 0:
                target_vx[index] = abs(target_vx[index])
            if target.x >= SCREEN_WIDTH-target_size:
                target_vx[index] = -(target_vx[index])
                target.x += int(target_vx[index])

    if moving_targety == True:
        for index,target in enumerate(targets):
            target.y += int(target_vy[index])
            if target.y <= target_size:
                target_vy[index] = abs(target_vy[index])
                target.y += int(target_vy[index])
            if target.y >= SCREEN_HEIGHT-target_size:
                target_vy[index] = -(target_vy[index])

def draw_winner(text):
    draw_text = winner_font.render(text,1,black)
    screen.blit(draw_text, ((SCREEN_WIDTH//2)-(draw_text.get_width()//2), SCREEN_HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)

#Screen resolution
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Button images

#easy_img = pygame.image.load(r'C:\Users\y_adhair\OneDrive - Winchester College\Documents\easy_img.png').convert_alpha()
#medium_img = pygame.image.load(r'C:\Users\y_adhair\OneDrive - Winchester College\Documents\medium_img.png').convert_alpha()
#hard_img = pygame.image.load(r'C:\Users\y_adhair\OneDrive - Winchester College\Documents\hard_img.png').convert_alpha()
#laser_pointer_upgrade_img = pygame.image.load(r'C:\Users\y_adhair\OneDrive - Winchester College\Documents\pointer_upgrade_img.png').convert_alpha()
#faster_bullets_upgrade_img = pygame.image.load(r'C:\Users\y_adhair\OneDrive - Winchester College\Documents\faster_bullets_upgrade_img.png').convert_alpha()

easy_img = pygame.image.load(r'C:\Users\yasse\Documents\easy_img.png').convert_alpha()
medium_img = pygame.image.load(r'C:\Users\yasse\Documents\medium_img.png').convert_alpha()
hard_img = pygame.image.load(r'C:\Users\yasse\Documents\hard_img.png').convert_alpha()
laser_pointer_upgrade_img = pygame.image.load(r'C:\Users\yasse\Documents\pointer_upgrade_img.png').convert_alpha()
faster_bullets_upgrade_img = pygame.image.load(r'C:\Users\yasse\Documents\faster_bullets_upgrade_img.png').convert_alpha()

black = (0,0,0)
white = (255,255,255)
green = (85,107,47)
red = (255,0,0)
blue = (0,0,255)

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def draw(self):

        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            

        screen.blit(self.image, (self.rect.x,self.rect.y))

easy_button = Button((SCREEN_WIDTH//2)-(easy_img.get_width()//2),(SCREEN_HEIGHT*(2/5))//1,easy_img)
medium_button = Button((SCREEN_WIDTH//2)-(medium_img.get_width()//2),(SCREEN_HEIGHT*(3/5))//1, medium_img)
hard_button = Button((SCREEN_WIDTH//2)-(hard_img.get_width()//2),(SCREEN_HEIGHT*(4/5))//1, hard_img)
laser_pointer_button = Button((SCREEN_WIDTH//2)-(hard_img.get_width()//2),(SCREEN_HEIGHT*(2/5))//1, laser_pointer_upgrade_img)
faster_bullets_button = Button((SCREEN_WIDTH//2)-(hard_img.get_width()//2),(SCREEN_HEIGHT*(3/5))//1, faster_bullets_upgrade_img)
#Player, gun, and bullet dimensions
player_height =70
player_width = 20
gun_height = 8
gun_width = 16
bullet_height = 4
bullet_width = 8
target_size = 50
pointer_height = 2
pointer_width = SCREEN_WIDTH

#Player and bullet velocities
vel_x = 8
vel_y_init = -10
vel_y_launch = -1
vel_y = vel_y_init
starting_bullet_vel = 30
bullet_vel = 30
#Laserx settings
incoming_lasersx = []
lasersx = []
laser_count = 0
laser_col = [red,white]
laser_size = 30
flash_delay = 500
laserx_osc = 1
incoming_lasersy = []
lasersy = []
lasery_osc = 1


#Initialise bullets, targets, ammo, and score
bullets = []
starting_ammo = 5
ammo = starting_ammo
targets = []
score = 0
target_vx = []
target_vy = []
ammo_lost = 3

#Target X velocities
min_target_vx = 10
max_target_vx = 20

#Target Y velocities
min_target_vy = 5
max_target_vy = 10

def set_easy():
    global min_target_vx,min_target_vy, max_target_vx, max_target_vy, starting_ammo, ammo, ammo_lost, laser_size
    min_target_vx = 2
    max_target_vx = 5
    min_target_vy = 1
    max_target_vy = 3
    starting_ammo = 10
    ammo_lost = 1
    laser_size = 30
    ammo = starting_ammo

def set_medium():
    global min_target_vx,min_target_vy, max_target_vx, max_target_vy, starting_ammo, ammo, ammo_lost, laser_size
    min_target_vx = 5
    max_target_vx = 10
    min_target_vy = 2
    max_target_vy = 6
    starting_ammo = 5
    ammo_lost = 2
    laser_size = 40
    ammo = starting_ammo

def set_hard():
    global min_target_vx,min_target_vy, max_target_vx, max_target_vy, starting_ammo, ammo, ammo_lost, laser_size
    min_target_vx = 8
    max_target_vx = 16
    min_target_vy = 5
    max_target_vy = 10
    starting_ammo = 3
    ammo_lost = 3
    laser_size = 50
    ammo = starting_ammo

g = (vel_y ** 2)/((SCREEN_HEIGHT-player_height))
hover_power = -g -0.1

left_facing = False
gun_offsetx_lim_left = 0
gun_offsetx_lim_right = 5 + gun_width
gun_offsetx = 5 + player_width
pointer_offsetx = 5 + player_width + gun_width
player_offsetx_left = 0
player_offsetx_right = 0
update_player_offsetx()

gun_high = 5
gun_mid = (player_height/2) - (gun_height/2)
gun_low = (player_height) - gun_height - 5
gun_offsety = gun_mid

#  EVENTS
generate_target = pygame.USEREVENT + 1
generate_incoming_laserx = pygame.USEREVENT + 2
laser_blink1 = pygame.USEREVENT + 3
laser_blink2 = pygame.USEREVENT + 4
laser_blink3 = pygame.USEREVENT + 5
laser_blink4 = pygame.USEREVENT + 6
laser_blink5 = pygame.USEREVENT + 7
generate_laserx = pygame.USEREVENT + 8
player_lose_health = pygame.USEREVENT + 9
player_make_vulnerable = pygame.USEREVENT + 10
generate_incoming_lasery = pygame.USEREVENT + 11
generate_lasery = pygame.USEREVENT + 12

player = pygame.Rect((100,SCREEN_HEIGHT-player_height,player_width,player_height))
gun = pygame.Rect((player.x + gun_offsetx, player.y + gun_offsety, gun_width, gun_height))
pointer = pygame.Rect((player.x + pointer_offsetx, player.y + gun_offsety+1, pointer_width, pointer_height))
player_color = green


def draw_screen():
    screen.fill(white)
    for temp_laserx in incoming_lasersx:
        pygame.draw.rect(screen, laser_col[laser_count%2], temp_laserx)
    for temp_lasery in incoming_lasersy:
        pygame.draw.rect(screen, laser_col[laser_count%2], temp_lasery)
    pygame.draw.rect(screen, player_color, player)
    gun.x = player.x + gun_offsetx
    gun.y = player.y + gun_offsety
    pygame.draw.rect(screen, black, gun)
    for temp_laserx in lasersx:
        pygame.draw.rect(screen, red,temp_laserx)
    for temp_lasery in lasersy:
        pygame.draw.rect(screen, red,temp_lasery)
    for bullet in bullets:
        pygame.draw.rect(screen, red, bullet)
    if pointer_check == True:
        pointer.x = player.x + pointer_offsetx
        pointer.y = player.y + gun_offsety + 2
        pygame.draw.rect(screen, blue,pointer)
    for target in targets:
        pygame.draw.rect(screen, black, target)
    score_text = info_font.render('Score: ' + str(score),1,black)
    ammo_text = info_font.render('Ammo: ' + str(ammo),1,black)
    screen.blit(ammo_text, (10,10))
    screen.blit(score_text, (SCREEN_WIDTH-score_text.get_width()-10, 10))
    pygame.display.update()

def draw_menu():
    screen.fill(white)
    prompt = prompt_font.render('Please choose a difficulty', 1, black)
    screen.blit(prompt, ((SCREEN_WIDTH//2)-(prompt.get_width()//2), SCREEN_HEIGHT//5))
    easy_button.draw()
    medium_button.draw()
    hard_button.draw()
    pygame.display.update()

def draw_upgrade_menu():
    screen.fill(white)
    prompt = prompt_font.render('Please choose an upgrade', 1, black)
    screen.blit(prompt, ((SCREEN_WIDTH//2)-(prompt.get_width()//2), SCREEN_HEIGHT//5))
    if pointer_check == False:
        laser_pointer_button.draw()
    faster_bullets_button.draw()
    pygame.display.update()

def upgrade_menu():
    local_run = True
    global run, clock, pointer_check, bullet_vel, laser_count, laserx_osc, incoming_lasersx, incoming_lasersy, laser_count
    while local_run == True:
        clock.tick(FPS)
        draw_upgrade_menu()
        if laser_pointer_button.clicked == True:
            laser_pointer_button.clicked = False
            pointer_check = True
            local_run = False
            break
        if faster_bullets_button.clicked == True:
            faster_bullets_button.clicked = False
            bullet_vel += 3
            local_run = False
            break
        for event in pygame.event.get():
            if event.type == generate_incoming_laserx:
                pygame.time.set_timer(generate_incoming_laserx,flash_delay, loops=1)
            if event.type == pygame.QUIT:
                run = False
                local_run = False
            if event.type == generate_incoming_lasery:
                pygame.time.set_timer(generate_incoming_lasery,flash_delay, loops=1)
            if event.type == laser_blink1:
                pygame.time.set_timer(laser_blink1,flash_delay, loops=1)
            if event.type == laser_blink2:
                pygame.time.set_timer(laser_blink2,flash_delay, loops=1)
            if event.type == laser_blink3:
                pygame.time.set_timer(laser_blink3,flash_delay, loops=1)
            if event.type == laser_blink4:
                pygame.time.set_timer(laser_blink4,flash_delay, loops=1)
            if event.type == laser_blink5:
                pygame.time.set_timer(laser_blink5,flash_delay, loops=1)
            if event.type == generate_laserx:
                pygame.time.set_timer(generate_laserx,flash_delay, loops=1)
            if event.type == generate_lasery:
                pygame.time.set_timer(generate_lasery,flash_delay, loops=1)

def scoreboard():
    global FPS, run, prompt_text, input_rect, user_text, too_big, too_big_text, title_text, swap_index, names,scores
    stage1 = False
    stage2 = True
    scores = []
    names = []
    user_text = ''
    prompt_text = info_font.render('You have achieved a place on the leaderboard. Enter your name:',1,black)
    too_big_text = info_font.render('Name too big, please reduce size',1,red)
    title_text = info_font.render('Leaderboard',1,red)
    input_rect_height = 57
    input_rect_width = 600
    input_rect = pygame.Rect(((SCREEN_WIDTH//2)-(input_rect_width//2)), SCREEN_HEIGHT//2, input_rect_width, input_rect_height)
    with open('high_scores.pkl', 'rb') as file:
        high_scores = pickle.load(file)
    for entry in high_scores:
        scores.append(int(entry[1]))
        names.append(entry[0])
    if score > scores[9]:
        stage1 = True
        for index, temp_score in enumerate(scores):
            if score > temp_score:
                scores.insert(index,score)
                swap_index = index
                scores = scores[:-1]
                break
            
    while stage1 == True:
        clock.tick(FPS)
        too_big = False
        draw_name()
        if user_text_drawn.get_width() > input_rect.width:
            too_big = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stage1 = False
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if too_big == False and len(user_text) != 0:
                        stage1 = False
                        names.insert(swap_index, user_text)
                        names = names[:-1]
                        new_board = []
                        for i in range(0,10):
                            new_board.append([names[i], scores[i]])
                        with open('high_scores.pkl','wb') as file:
                            pickle.dump(new_board, file)
                        pygame.event.clear()
                        press = 0
                        break
                else:
                    user_text += event.unicode

    while stage2 == True:
        clock.tick(FPS)
        draw_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stage2 = False
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    press += 1
                    if press == 2:
                        stage2 = False
                        break
        

        
        

def draw_name():
    global user_text_drawn, too_big
    screen.fill(white)
    screen.blit(prompt_text, (((SCREEN_WIDTH//2)-(prompt_text.get_width()//2)), SCREEN_HEIGHT//5))
    pygame.draw.rect(screen, blue, input_rect)
    user_text_drawn = info_font.render(user_text, 1, black)
    screen.blit(user_text_drawn, (input_rect.x+5,input_rect.y+5))
    if too_big == True:
        screen.blit(too_big_text, ((SCREEN_WIDTH//2)-(prompt_text.get_width()//2),4* (SCREEN_HEIGHT//5)))
    pygame.display.update()

def draw_board():
    screen.fill(white)
    screen.blit(title_text, (((SCREEN_WIDTH//2)-(title_text.get_width()//2)), SCREEN_HEIGHT//6))
    offset = SCREEN_HEIGHT//6 + title_text.get_height() + 5
    for i in range(0,10):
        temp_name_text = info_font.render(names[i],1,black)
        screen.blit(temp_name_text,(5,offset+(50*i)))
        temp_score_text = info_font.render(str(scores[i]),1,black)
        screen.blit(temp_score_text,(SCREEN_WIDTH-temp_score_text.get_width()-5,offset+(50*i)))
    pygame.display.update()
    



FPS = 60
clock = pygame.time.Clock()
run = True
setting_chosen = False
in_air = False
hover = False
lock_aim = False
moving_targetx = False
moving_targety = False
player_invincible = False
pointer_check = False
local_score = 0
laser_movingy = False
laser_movingx = False
while setting_chosen == False:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            setting_chosen = True
    draw_menu()
    if easy_button.clicked == True:
        set_easy()
        setting_chosen = True
        break
    if medium_button.clicked == True:
        set_medium()
        setting_chosen = True
        break
    if hard_button.clicked == True:
        set_hard()
        setting_chosen = True
        break




while run:
    clock.tick(FPS)
    key = pygame.key.get_pressed()
    player_movement(key,player)
    if in_air == True:
        player_in_air(player)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                hover = True
                if player.y == SCREEN_HEIGHT - player_height:
                    vel_y = vel_y_launch
                    player.y += vel_y
                    in_air = True
            if event.key == pygame.K_LSHIFT:
                lock_aim = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                hover = False
            if event.key == pygame.K_LSHIFT:
                lock_aim = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and left_facing == True and ammo > 0:
                bullet = pygame.Rect(gun.x, gun.y+(gun_height/2)-(bullet_height/2), bullet_width, bullet_height)
                bullets.append(bullet)
                ammo += -1
            if event.button == 1 and left_facing == False and ammo > 0:
                bullet = pygame.Rect(gun.x+gun_width, gun.y+(gun_height/2)-(bullet_height/2), bullet_width, bullet_height)
                bullets.append(bullet)
                ammo += -1
            if event.button == 4:
                raise_gun()
            if event.button == 5:
                lower_gun()
        if event.type == generate_target:
            target = pygame.Rect(random.randint(0,SCREEN_WIDTH-target_size), random.randint(0,SCREEN_HEIGHT-target_size), target_size, target_size)
            targets.append(target)
            if moving_targetx == True:
                target_vx.append(random.randint(min_target_vx,max_target_vx))
            if moving_targety == True:
                target_vy.append(random.randint(min_target_vy,max_target_vy))
        if event.type == generate_incoming_laserx:
            laserx = pygame.Rect(0, random.randint(0,SCREEN_HEIGHT-laser_size), SCREEN_WIDTH, laser_size)
            incoming_lasersx.append(laserx)
            laser_count = 0
            if len(incoming_lasersx) == 1:
                pygame.time.set_timer(laser_blink1,flash_delay, loops=1)
                pygame.time.set_timer(laser_blink2,flash_delay*2, loops=1)
                pygame.time.set_timer(laser_blink3,flash_delay*3, loops=1)
                pygame.time.set_timer(laser_blink4,flash_delay*4, loops=1)
                pygame.time.set_timer(laser_blink5,flash_delay*5, loops=1)
        if event.type == generate_incoming_lasery:
            lasery = pygame.Rect(random.randint(0,SCREEN_WIDTH-laser_size), 0, laser_size, SCREEN_HEIGHT)
            incoming_lasersy.append(lasery)
        if event.type == laser_blink1:
            laser_count += 1
        if event.type == laser_blink2:
            laser_count += 1
        if event.type == laser_blink3:
            laser_count += 1
        if event.type == laser_blink4:
            laser_count += 1
        if event.type == laser_blink5:
            laser_count += 1
            pygame.time.set_timer(generate_laserx,flash_delay, loops = 1)
            pygame.time.set_timer(generate_lasery,flash_delay, loops = 1)
        if event.type == generate_laserx:
            for temp_laserx in incoming_lasersx:
                temp_laserx.height = 5
                temp_laserx.y += ((1/2) * laser_size)-3
                lasersx.append(temp_laserx)
            laserx_osc = 1
            incoming_lasersx = []
        if event.type == generate_lasery:
            for temp_lasery in incoming_lasersy:
                temp_lasery.width = 5
                temp_lasery.x += ((1/2) * laser_size)-3
                lasersy.append(temp_lasery)
            laserx_osc = 1
            incoming_lasersy = []
        if event.type == player_lose_health:
            ammo += -ammo_lost
            player_invincible = True
            player_color = blue            
            pygame.time.set_timer(player_make_vulnerable, 2000, loops=1)
        if event.type == player_make_vulnerable:
            player_invincible = False
            player_color = green
            
    if local_score == 3:
        upgrade_menu()
        local_score = 0    
    if len(targets) < 1:
        pygame.event.post(pygame.event.Event(generate_target))
        first = False
    if score >= 5 and len(targets) < 2:
        pygame.event.post(pygame.event.Event(generate_target))
    if score >= 10 and len(targets) < 3:
        pygame.event.post(pygame.event.Event(generate_target))
    if moving_targetx == False and score >= 10:
        moving_targetx = True
        for target in targets:
            v = random.randint(min_target_vx,max_target_vx)
            target_vx.append(v)
    if moving_targety == False and score >= 15:
        moving_targety = True
        for target in targets:
            v = random.randint(min_target_vy,max_target_vy)
            target_vy.append(v)
    if score >= 5 and len(incoming_lasersx) == 0 and len(lasersx) == 0:
        pygame.event.post(pygame.event.Event(generate_incoming_laserx))
    if score >= 10 and len(incoming_lasersx) == 1 and len(lasersx) == 0:
        pygame.event.post(pygame.event.Event(generate_incoming_laserx))
    if score >= 15 and len(incoming_lasersy) == 0 and len(lasersy) == 0:
        pygame.event.post(pygame.event.Event(generate_incoming_lasery))
    if score >= 20 and len(incoming_lasersy) == 1 and len(lasersy) == 0:
        pygame.event.post(pygame.event.Event(generate_incoming_lasery))
    if score >= 20 and laser_movingx == False:
        laser_movingx = True
    handle_targets()
            

    if ammo == 0 and len(bullets) == 0:
        winner_text = 'You ran out of ammo! Your score was ' + str(score)
        bullet_vel = starting_bullet_vel
        ammo = starting_ammo
        local_score = 0
        moving_targety = False
        moving_targetx = False
        pointer_check = False
        targets = []
        bullets = []
        target_vx = []
        target_vy = []
        lasersx =[]
        lasersy =[]
        incoming_lasersx = []
        incoming_lasersy = []
        pygame.event.clear()
        draw_winner(winner_text)
        scoreboard()
        score = 0

    handle_lasersx()
    handle_lasersy()
    handle_bullets(bullets)
    if pointer_check == True:
        handle_pointer()
    draw_screen()


pygame.quit()