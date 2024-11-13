import gamefunctions
import pygame

pygame.init()

screen_width = 384
screen_height = 384

screen = pygame.display.set_mode((screen_width, screen_height))
user_pos = {'x_pos': 32, 'y_pos': 64}
text_font = pygame.font.SysFont('Consolas', 16)
clock = pygame.time.Clock()

def drawText(screen, text, x, y):
    text_image = text_font.render(text, True, (240,240,240))
    screen.blit(text_image, (x,y))

def moveUser(user_pos, x=0, y=0):
    if x != 0:
        if (user_pos['x_pos'] + x) in range(0, 384):
            user_pos['x_pos'] += x
    elif y != 0:
        if (user_pos['y_pos'] + y) in range(64, 384):
            user_pos['y_pos'] += y

def drawUser(screen, user_pos):
    pygame.draw.rect(
        screen, color = (255,255,255),
        rect = (user_pos['x_pos'], user_pos['y_pos'], 32, 32)
    )

def drawShop(screen):
    pygame.draw.circle(
        screen, color = (34, 139, 34),
        center = ((272, 80)),
        radius = (16)
    )

loadOrNew = """Start from save or new game?
1)Start from save
2)New Game"""
started = False
while started == False:
    screen.fill((50,50,50))
    drawText(screen, loadOrNew, 0, 192)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            started = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                user_stats, inventory = gamefunctions.loadFromSave()
                started = True
            elif event.type == pygame.K_2:
                user_stats, inventory = gamefunctions.newGame()
                started = True
    
    clock.tick(60)
    pygame.display.flip()

running = True
while running:
    screen.fill((50, 50, 50))
    current_text = "Hello!"
    drawUser(screen, user_pos)
    drawShop(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                moveUser(user_pos, y=32)
            elif event.key == pygame.K_w:
                moveUser(user_pos, y=-32)
            elif event.key == pygame.K_d:
                moveUser(user_pos, x=32)
            elif event.key == pygame.K_a:
                moveUser(user_pos, x=-32)
            
    
    clock.tick(60)
    pygame.display.flip()

pygame.quit()