import pygame as pg

# Want to change this? Unleash the horrors within...
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1000
SCREEN_SIZE = [SCREEN_WIDTH, SCREEN_HEIGHT]

NUM_INJECTORS = 10

STATUS_BAR_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT / 10)

TOTAL_INJECTOR_HEIGHT = SCREEN_HEIGHT - STATUS_BAR_SIZE[1]

# How big can you take?
INJECTOR_SIZE = (
    SCREEN_WIDTH / 2,
    TOTAL_INJECTOR_HEIGHT / (NUM_INJECTORS / 2),
)

UPGRADE_BUTTON_SIZE = (INJECTOR_SIZE[0], INJECTOR_SIZE[1] / 8)
IMAGE_SIZE = (INJECTOR_SIZE[0], INJECTOR_SIZE[1] - UPGRADE_BUTTON_SIZE[1])

# KETAMINE_COUNTER_SIZE = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
KETAMINE_COUNTER_COLOR = BLACK
UPGRADE_BUTTON_TEXT_COLOR = BLACK
IMAGE_NAME_TEXT_COLOR = BLACK

FPS = 120  # Go big or go home

# TODO(bhollaway): parameterize based on screen size
KETAMINE_FONT = pg.font.Font("../assets/fonts/joystix_mono.ttf", 25)
KETAMINE_STATUS_FONT = pg.font.Font("../assets/fonts/joystix_mono.ttf", 20)
KETAMINE_VICTORY_FONT = pg.font.Font("../assets/fonts/joystix_mono.ttf", 30)
DEFAULT_FONT = pg.font.SysFont("arialblack", 25)
