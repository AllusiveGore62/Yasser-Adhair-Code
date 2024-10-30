import pygame
#Controls 
#   WASD: Player 1 movement
#   Ctrl: Player 1 fire
#   Arrow keys: Player 2 movement
#   Space: Player 2 Fire


pygame.init()
pygame.font.init()

surface = True

def player1_movement(key, player1):
    if key[pygame.K_a] == True and player1.x > 0:
        player1.x += -vel
    elif key[pygame.K_d] == True and player1.x < (SCREEN_WIDTH//2)-5-player1.width:
        player1.x += vel
    if key[pygame.K_w] == True and player1.y > 0:
        player1.y += -vel
    elif key[pygame.K_s] == True and player1.y < SCREEN_HEIGHT-player1.height:
        player1.y += vel

def player2_movement(key, player2):
    if key[pygame.K_LEFT] == True and player2.x > (SCREEN_WIDTH//2)+5:
        player2.x += -vel
    elif key[pygame.K_RIGHT] == True and player2.x < SCREEN_WIDTH-player2.width:
        player2.x += vel
    if key[pygame.K_UP] == True and player2.y > 0:
        player2.y += -vel
    elif key[pygame.K_DOWN] == True and player2.y < SCREEN_HEIGHT-player2.height:
        player2.y += vel

def handle_bullets(player1_bullets, player2_bullets, player1, player2):
    for bullet in player1_bullets:
        bullet.x += bullet_vel
        if player2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(player2_hit))
            player1_bullets.remove(bullet)
        elif bullet.x > SCREEN_WIDTH - 10:
            player1_bullets.remove(bullet)
    for bullet in player2_bullets:
        bullet.x += -bullet_vel
        if player1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(player1_hit))
            player2_bullets.remove(bullet)
        elif bullet.x < 0:
            player2_bullets.remove(bullet)

def draw_winner(text):
    draw_text = winner_font.render(text,1,black)
    screen.blit(draw_text, ((SCREEN_WIDTH//2)-(draw_text.get_width()//2), SCREEN_HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

player1_hit = pygame.USEREVENT + 1
player2_hit = pygame.USEREVENT + 2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
player1 = pygame.Rect((75,275,50,50))
player2 = pygame.Rect((675,275,50,50))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
border = pygame.Rect((SCREEN_WIDTH//2)-5,0,10, SCREEN_HEIGHT)
player1_bullets = []
player2_bullets = []

player1_health = 10
player2_health = 10

health_font = pygame.font.SysFont('comicsans',40)
winner_font = pygame.font.SysFont('comicsans',100)

FPS = 60
vel = 5
bullet_vel = 7
max_bullets = 3
clock = pygame.time.Clock()
run = True
white = (255,255,255)
black = (0,0,0)

def draw_window():
    screen.fill(white)
    pygame.draw.rect(screen, black, border)
    player1_health_text = health_font.render('Health: ' + str(player1_health),1,black)
    player2_health_text = health_font.render('Health: ' + str(player2_health),1,black)
    screen.blit(player1_health_text, (10,10))
    screen.blit(player2_health_text, (SCREEN_WIDTH-player2_health_text.get_width()-10, 10))
    pygame.draw.rect(screen, (255,0,0), player1)
    pygame.draw.rect(screen, (0,255,0), player2)

    for bullet in player1_bullets:
        pygame.draw.rect(screen, (255,0,0), bullet)

    for bullet in player2_bullets:
        pygame.draw.rect(screen, (0,255,0), bullet)
    pygame.display.update()



while run:
    clock.tick(FPS)
    key = pygame.key.get_pressed()
    player1_movement(key, player1)
    player2_movement(key, player2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL and len(player1_bullets) < max_bullets:
                bullet = pygame.Rect(player1.x + player1.width, player1.y + (player1.height)//2-2, 10,4)
                player1_bullets.append(bullet)
            if event.key == pygame.K_RCTRL and len(player2_bullets) < max_bullets and surface == False:  
                bullet = pygame.Rect(player2.x, player2.y + (player2.height)//2-2, 10,4)
                player2_bullets.append(bullet)
            if event.key == pygame.K_SPACE and len(player2_bullets) < max_bullets and surface == True:  
                bullet = pygame.Rect(player2.x, player2.y + (player2.height)//2-2, 10,4)
                player2_bullets.append(bullet)
        if event.type == player1_hit:
            player1_health += -1
        if event.type == player2_hit:
            player2_health += -1

    winner_text = ''
    if player1_health <= 0:
        winner_text = 'Player 2 Wins!'
    
    if player2_health <= 0:
        winner_text = 'Player 1 Wins!'
        
    
    if winner_text != '':
        draw_winner(winner_text)
        player1_health = 10
        player2_health = 10
        player1_bullets = []
        player2_bullets = []

    handle_bullets(player1_bullets,player2_bullets,player1,player2)
    draw_window()
        

pygame.quit()
