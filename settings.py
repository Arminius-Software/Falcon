import sys
import pygame
import pygame.gfxdraw
import random
import time
import os
import neat
import math
from multiprocessing.pool import ThreadPool as Pool
import re
import textwrap


# this file contains all the needed settings for main.py and classes.py, this allows for easy testing of important values since they are all in one place

# screen settings

WIDTH = 1400
HEIGHT = 800

MAIN_MENU_WIDTH = 800 # the window is smaller in main menu mode
GAME_WIDTH = 700 # half of the window is reserved for the game the other half for the neural net visualization

pygame.init()
window = pygame.display.set_mode((MAIN_MENU_WIDTH,HEIGHT))
pygame.display.set_caption("Falcon") 

# settings

click = False

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BUTTON_GREY = (220, 220, 220)

FONT = pygame.font.SysFont("arial", 24, True)  
FONT_MAIN_MENU = pygame.font.SysFont("arial", 40, True)  

# Calculate x-coordinate to center the buttons horizontally
BUTTON_WIDHT = 400
BUTTON_HEIGHT = 80
X_CENTER = (MAIN_MENU_WIDTH - BUTTON_WIDHT) // 2

MAIN_MENU_BUTTON_PLAY = pygame.Rect(X_CENTER, 200, BUTTON_WIDHT, BUTTON_HEIGHT)
MAIN_MENU_BUTTON_HELP = pygame.Rect(X_CENTER, 325, BUTTON_WIDHT, BUTTON_HEIGHT)
MAIN_MENU_BUTTON_STOP = pygame.Rect(X_CENTER, 450, BUTTON_WIDHT, BUTTON_HEIGHT)

HELP_BACK_BUTTON = pygame.Rect(X_CENTER, (HEIGHT - 200), BUTTON_WIDHT, BUTTON_HEIGHT)

# game variables 

clock = pygame.time.Clock()
generation = 0
score = 0
high_score = 0
MAX_ASTEROIDS = 4
CLOSESTS_ASTEROIDS = 2
FRAMES_PER_ASTEROID = 120

PLAYER_COLORS = [
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (255, 0, 255),   # Magenta
    (0, 255, 255),   # Cyan
    (128, 0, 0),     # Maroon
    (0, 128, 0),     # Dark Green
    (0, 0, 128),     # Navy
    (128, 128, 0),   # Olive
    (128, 0, 128),   # Purple
    (0, 128, 128),   # Teal
    (192, 192, 192), # Silver
    (128, 128, 128), # Grey
    (255, 165, 0),   # Orange
    (255, 192, 203), # Pink
    (165, 42, 42),   # Brown
    (255, 215, 0),   # Gold
    (0, 255, 127),   # Spring Green
    (0, 0, 0)        # Black
]


# Node settings

winner_weights = []
mode_winner = False
current_winner_selected = 0

NEURAL_NET_REC_TOP = (GAME_WIDTH + 35, 45, GAME_WIDTH - 50, 362)
NEURAL_NET_REC_BOTTOM = (GAME_WIDTH + 35, 427, GAME_WIDTH - 50, 362)

BUTTON_HEIGHT_NEURAL_NET = 60
BUTTON_WIDHT_NEURAL_NET = 150

PAUSE_BUTTON = pygame.Rect(GAME_WIDTH, 0, BUTTON_WIDHT_NEURAL_NET, BUTTON_HEIGHT_NEURAL_NET)

NEXT_NEGATIVE_BUTTON_TOP = pygame.Rect(GAME_WIDTH, (HEIGHT//2) - BUTTON_HEIGHT_NEURAL_NET, BUTTON_WIDHT_NEURAL_NET, BUTTON_HEIGHT_NEURAL_NET)
NEXT_POSITIVE_BUTTON_TOP = pygame.Rect(WIDTH - BUTTON_WIDHT_NEURAL_NET, (HEIGHT//2) - BUTTON_HEIGHT_NEURAL_NET, BUTTON_WIDHT_NEURAL_NET, BUTTON_HEIGHT_NEURAL_NET)

WINNER_CURRENT_SWITCH_BUTTON = pygame.Rect(GAME_WIDTH, ((HEIGHT//2) + 2), BUTTON_WIDHT_NEURAL_NET, BUTTON_HEIGHT_NEURAL_NET)

NEXT_NEGATIVE_BUTTON_BOTTOM = pygame.Rect(GAME_WIDTH, (HEIGHT) - BUTTON_HEIGHT_NEURAL_NET, BUTTON_WIDHT_NEURAL_NET, BUTTON_HEIGHT_NEURAL_NET)
NEXT_POSITIVE_BUTTON_BOTTOM = pygame.Rect(WIDTH - BUTTON_WIDHT_NEURAL_NET, (HEIGHT) - BUTTON_HEIGHT_NEURAL_NET, BUTTON_WIDHT_NEURAL_NET, BUTTON_HEIGHT_NEURAL_NET)

NODES_RADIUS = 18  # Size of the nodes

# Define positive and negative line colors

POSITIVE_LINE_COLOR = BLUE
NEGATIVE_LINE_COLOR = RED

LAYERS = [6, 4, 2]

# images

# converting increases performance, pngs with no background need convert_alpha() so that the background stays clear

PLAYER = pygame.image.load("images/player_small.png").convert_alpha() # image source https://www.nicepng.com/maxp/u2q8e6q8i1y3u2i1/
ASTEROID = pygame.image.load("images/asteroid_small.png").convert_alpha()
BACKGROUND = pygame.image.load("images/background.png").convert()
