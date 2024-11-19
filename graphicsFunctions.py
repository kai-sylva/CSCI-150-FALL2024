"""Classes and functions for gameGraphics.py"""

import pygame
import random
import gamefunctions
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

class User():
    """Contains variables and functions relating to the user in gameGraphics.py"""
    def __init__(self, stats=dict, inventory=dict) -> None:
        self.pos = {'x_pos': 32, 'y_pos': 128}
        self.stats = stats
        self.inventory = inventory
    
    def __eq__(self, other):
        # If user moves over a monster or the shop
        if self.pos == other.pos:
            return True
        else:
            return False
    
    def move(self, x=0, y=0):
        """Changes user's position values. The current areas available for the user
        to be positioned are (0-384, 128-384).
        
        Parameters:
            x (int): represents number of pixels to move user on x axis
            y (int): represents number of pixels to move user on y axis
        
        Returns: None
        """
        if x != 0:
            if (self.pos['x_pos'] + x) in range(0, 384):
                self.pos['x_pos'] += x
        elif y != 0:
            if (self.pos['y_pos'] + y) in range(128, 384):
                self.pos['y_pos'] += y

class Monster():
    """Contains variables and functions relating to a monster in gameGraphics.py"""
    def __init__(self, enderman=False) -> None:
        self.pos = {'x_pos': 192, 'y_pos': 288}
        # Right now, monster in gameGraphics is always an enderman
        if enderman:
            self.image = pygame.image.load('Enderman_icon.png')
            self.stats = gamefunctions.new_random_monster(enderman=True)
        else:
            # FIXME -- change self.image here when introducing new monsters
            self.image = pygame.image.load('Enderman_icon.png')
            self.stats = gamefunctions.new_random_monster()
        
    
    def move(self):
        """Moves monster within pyGame window, with the small chance of the 
        monster teleporting (moving 96px instead of 32px)
        
        Parameters: 
            self
        
        Returns: None
        
        """
        # Generate random direction
        direction = random.randint(1, 4)
        random_teleport = random.randint(1, 100)
        # Distance to move monster
        distance = 32
        if 10 <= random_teleport <= 20:
            distance *= 3
        # If direction == 1, move up 32px
        if direction == 1:
            if self.pos['y_pos'] - distance in range(128, 384):
                self.pos['y_pos'] -= distance
        elif direction == 2:
            if self.pos['y_pos'] + distance in range(128, 384):
                self.pos['y_pos'] += distance
        elif direction == 3:
            if self.pos['x_pos'] - distance in range(0, 384):
                self.pos['x_pos'] -= distance
        elif direction == 4: 
            if self.pos['x_pos'] + distance in range(0, 384):
                self.pos['x_pos'] += distance
    
    def draw(self, screen):
        """Draws (blits) monster image to the screen
        
        Parameters:
            self
            screen (pygame display): pygame window to blit image on to
        
        """
        screen.blit(self.image, (self.pos['x_pos'], self.pos['y_pos']))
    
class Shop():
    """Contains variables and functions relating to a shop with items available
    to purchase"""
    def __init__(self, pos, items) -> None:
        self.pos = pos
        self.items = items
        self.image = pygame.image.load('shop.png')
    
    def draw(self, screen):
        """Draws (blits) shop image onto the screen
        
        Parameters:
            self
            screen (pygame display): pygame window to blit image on to
        
        Returns: None
        
        """
        screen.blit(self.image, (self.pos['x_pos'], self.pos['y_pos']))
    
    def interact(self, user_stats, user_inventory):
        """Starts a shop interaction
        
        Parameters: 
            Self
            user_stats (dict): dictionary containing user stats (gold, etc.)
            user_inventory (dict): dictionary containing user inventory
        
        Returns: boolean indicating interaction is finished
        
        """
        return gamefunctions.buyShopItems(user_stats, self.items, user_inventory)
    

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

def drawOverlay(screen, user_pos, image):
    """Renders an image on top of user's image/rect

    Parameters:
        screen: the screen/pygame window to blit the image on to
        user_pos (dict): 2-value dict containning x and y pos on screen
        image: the image to overlay on top of user
    
    Returns: None
    
    """
    s = pygame.Surface((32, 32))
    s.set_alpha(64)
    s.blit(image, (0,0))
    screen.blit(s, (user_pos['x_pos'], user_pos['y_pos']))

def drawShop(screen, pos):
    """Draws a cute little green circle representing the shop.
    
    Parameters:
        screen: the pyGame window to draw the shop on

    Returns: None
    """
    pygame.draw.circle(
        screen, color = (34, 139, 34),
        center = (pos),
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