# Game options / settings
TITLE = "Shauna's Sky Search"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'comic sans'
HS_FILE = "highscore.txt"
SPRITESHEET = "Shauna2.png" 

# Player properties
PLAYER_ACC = 0.5 # How quickly you accelerate
PLAYER_FRICTION = -0.12 # Max speed / How quickly you stop
PLAYER_GRAV = 0.8 # How fast you fall / Gravity
PLAYER_JUMP = 23 # How high you jump

# Game properties
BOOST_POWER = 60
POW_SPAWN_PCT = 25

# Starting platform
PLATFORM_LIST = [(0, HEIGHT - 9,),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4), 
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 108, 22)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (214, 1, 255)
SKYBLUE = (0, 225, 225)