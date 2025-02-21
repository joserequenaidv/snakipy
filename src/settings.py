# Define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHTBROWN = (175, 126, 47)

# Game settings
WIDTH = 480
HEIGHT = 480 
FPS = 30
TITLE = "Tilemap Demo"
BGCOLOR = LIGHTBROWN

TILESIZE = 16
GRIDWIDTH = WIDTH // TILESIZE
GRIDHEIGHT = HEIGHT // TILESIZE

FRUIT_TYPES = {
    "Apple": {
        "points": 1,
        "image": "fruits/apple.png",
        "sound": "apple.mp3"
    },
    "Banana": {
        "points": 2,
        "image": "fruits/banana.png",
        "sound": "banana_cherry.mp3"
    },
    "Cherry": {
        "points": 3,
        "image": "fruits/cherry.png",
        "sound": "banana_cherry.mp3"
    }
}

# SOUNDS
# Sound settings
SOUND_FOLDER = "assets/sounds/"

# Sound files
SOUND_DEATH = "death.wav"
SOUND_MOVE = "move.wav"
SOUND_MENU = "menu.wav"
SOUND_BACKGROUND = "background.mp3"

# Sound volumes (0.0 to 1.0)
SOUND_EFFECTS_VOLUME = 0.2
MUSIC_VOLUME = 0.1

# MAIN-MENU Settings
MENU_OPTIONS = ["PLAY", "OPTIONS", "RANKING"]
SELECTED_COLOR_MENU = YELLOW
UNSELECTED_COLOR_MENU = WHITE
MAIN_MENU_BG = LIGHTBROWN
OPTION_TEXT_FONT_SIZE = 60
OPTION_TEXT_FONT_TYPE = "chicken_pie"

# RANKING Settings
RANKING_TITLE_FONT_SIZE = 48
RANKING_TITLE_FONT_TYPE = "chicken_pie"
RANKING_SCORE_FONT_SIZE = 36
RANKING_SCORE_FONT_TYPE = "chicken_pie"
RANKING_FILE_PATH = "../data/ranking.txt"
RANKING_TITLE_COLOR = WHITE

# Sprite folder
SPRITE_FOLDER = "assets/images/sprites"

# Sprite files and paths
PLAYER_HEADIMAGE = {
    "right": {
        "image": "ekans/head/ekanshead1.png"
    },
    "down": {
        "image": "ekans/head/ekanshead2.png"
    },
    "left": {
        "image": "ekans/head/ekanshead3.png"
    },
    "up": {
        "image": "ekans/head/ekanshead4.png"
    },
}

PLAYER_NECKIMAGE = {
    "right": {
        "image": "ekans/neck/ekansneck1.png"
    },
    "down": {
        "image": "ekans/neck/ekansneck2.png"
    },
    "left": {
        "image": "ekans/neck/ekansneck3.png"
    },
    "up": {
        "image": "ekans/neck/ekansneck4.png"
    }
}

PLAYER_TAIL_TIP_IMAGE = {
    "right": {
        "image": "ekans/tail/ekanstailtip1.png"
    },
    "down": {
        "image": "ekans/tail/ekanstailtip2.png"
    },
    "left": {
        "image": "ekans/tail/ekanstailtip3.png"
    },
    "up": {
        "image": "ekans/tail/ekanstailtip4.png"
    }
}

PLAYER_TAIL_JOINT_IMAGE = {
    "right": {
        "image": "ekans/ekanstailjoint1.png"
    },
    "down": {
        "image": "ekans/ekanstailjoint2.png"
    },
    "left": {
        "image": "ekans/ekanstailjoint3.png"
    },
    "up": {
        "image": "ekans/ekanstailjoint4.png"
    }
}

PLAYER_BODYIMAGE = {
    "right": {
        "image": "ekans/ekansbody1.png"
    },
    "down": {
        "image": "ekans/ekansbody2.png"
    },
    "left": {
        "image": "ekans/ekansbody3.png"
    },
    "up": {
        "image": "ekans/ekansbody4.png"
    }
}

IMAGE_BACKGROUND = "backgrounds/purple-universe.png"
# PLAYER_TAILIMAGE = "snake-tail/st1.png"