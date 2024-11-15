"""Functions and variables for gameGraphics.py"""

import pygame
pygame.init()

class MyAdventure():
    """Contains adventure game variables representing pyGame text font, screen,
    screen dimensions, and initial user position.
    """
    def __init__(self):
        self.font_path = pygame.font.match_font('Consolas')
        self.font = pygame.font.Font(self.font_path, 16)
        self.screen_w = 384
        self.screen_h = 384
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
    # Initial user position on screen
        self.user_pos = {'x_pos': 32, 'y_pos': 128}

def drawStats(screen, font, stats, x, y):
    """Renders image of user's stats and blits them to the pyGame screen.

    Parameters:
        screen: the pygame screen to blit the image on to
        font: the pygame font to use when rendering text
        stats (str): It's recommended this comes from gamefunctions.getUserStats()
        so that the text is cleanly formatted. 
        x (int): x coordinate to blit image to
        y (int): y coordinate to blit image to
    
    Returns: None
    """
    i = 0
    # To render newlines, each line must be rendered as a separate image
    lines = stats.split("\n")
    for line in lines:
        text_image = font.render(line, True, (240,240,240))
        if line == 0:
            screen.blit(text_image, (x,y))
            i += 1
        else:
            screen.blit(text_image, (x,y+(16*i)))
            i += 1

def drawOptions(screen, font, text, x, y, highlight=1):
    """Renders text on the initial startup screen and highlights a selectable
    option.

    Parameters:
        screen: the pyGame screen to blit the image(s) on to
        font: the pyGame font to use when rendering text
        text (list): The text to render (each list value is a line)
        x (int): x coordinate to blit image to
        y (int): y coordinate to blit image to
        highlight (int): Option to highlight. Default is 1 (which is the first
        selectable option in the instance that save files exist)
    
    Returns: None
    """
    i = 0
    for line in text:
        if line == 0:
            text_image = font.render(line, True, (240,240,240))
            screen.blit(text_image, (x,y))
            i += 1
        else:
            if highlight == i:
                text_image = font.render(line, True, (50,50,50), (255,255,255))
                screen.blit(text_image, (x,y+(16*i)))
            else: 
                text_image = font.render(line, True, (240,240,240))
                screen.blit(text_image, (x,y+(16*i)))
            i += 1

def moveUser(user_pos, x=0, y=0):
    """Changes user's position values. The current areas available for the user
    to be positioned are (0-384, 128-384).
    
    Parameters:
        user_pos (dict):
            x_pos: user's position on x axis
            y_pos: user's position on y axis
        x (int): represents number of pixels to move user on x axis
        y (int): represents number of pixels to move user on y axis
    
    Returns: None
    """
    if x != 0:
        if (user_pos['x_pos'] + x) in range(0, 384):
            user_pos['x_pos'] += x
    elif y != 0:
        if (user_pos['y_pos'] + y) in range(128, 384):
            user_pos['y_pos'] += y

def drawUser(screen, user_pos):
    """Render's the user (currently drawn as a rectangle)

    Parameters: 
        screen: the pyGame window to draw the user on
        user_pos (dict): dictionary containing values regarding user's current
        position on screen
    
    Returns: None
    """
    pygame.draw.rect(
        screen, color = (255,255,255),
        rect = (user_pos['x_pos'], user_pos['y_pos'], 32, 32)
    )

def drawShop(screen):
    """Draws a cute little green circle representing the shop.
    
    Parameters:
        screen: the pyGame window to draw the shop on

    Returns: None
    """
    pygame.draw.circle(
        screen, color = (34, 139, 34),
        center = ((272, 176)),
        radius = (16)
    )

def saveGame(screen, font):
    """Renders text to the screen giving the option to save game progress.

    Parameters: 
        screen: the pyGame screen to blit the image(s) on to
        font: the pyGame font to use when rendering text

    Returns:
        highlight (int): represents the option selected by the user. If user 
        closes the window by pressing the red X, 2 is returned and nothing
        is saved.
    """
    save_options = ["Save stats? (press enter)", "1) Yes", "2) No"]
    highlight = 1
    save_text = True
    while save_text:
        screen.fill((50,50,50))
        drawOptions(screen, font, save_options, 0, 160, highlight)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_text = False
                highlight = 2
                return highlight
            elif event.type == pygame.KEYDOWN:
                # highlight is used to select between options
                if event.key == pygame.K_DOWN:
                    highlight = 2
                elif event.key == pygame.K_UP:
                    highlight = 1
                elif event.key == pygame.K_RETURN:
                    save_text = False
                    return highlight
        pygame.display.flip()