import math
import glm
import pygame
import moderngl
import pytmx
import sys
import random
import numpy
import pathlib
import re
import pywavefront

from Enviroment.TextureID import ID
from collections import deque
from functools import lru_cache
from itertools import cycle
from typing import Iterable, Any

DEFAULT_POSITION = glm.vec3(0,0,0)
DEFAULT_SCALE = glm.vec3(1,1,1)
DEFAULT_ROTATION = glm.vec3(0,90,0)

LIGHT_POSITION = glm.vec3(50,50,-10)
LIGHT_DIRECTION = glm.vec3(0,0,0)
LIGHT_COLOUR = glm.vec3(1,1,1)
LIGHT_AMBIENCE = 1.5
LIGHT_DIFFUSION = 1.0
LIGHT_SPECULAR = 1.6

MAJOR_VERSION = 3
MINOR_VERSION = 3
DEPTH_SIZE = 24
RESOLUTION = glm.vec2(1280, 720)

KEYS = {
    'FORWARD': pygame.K_w,
    'BACK': pygame.K_s,
    'UP': pygame.K_q,
    'DOWN': pygame.K_e,
    'STRAFE_L': pygame.K_a,
    'STRAFE_R': pygame.K_d,
    'INTERACT': pygame.K_f,
    'WEAPON_1': pygame.K_1,
    'WEAPON_2': pygame.K_2,
    'WEAPON_3': pygame.K_3,
}

ASPECT_RATIO = RESOLUTION.x / RESOLUTION.y
FIELD_OF_VIEW = 50
VERTICAL_FOV = glm.radians(FIELD_OF_VIEW) 
HORIZONTAL_FOV = 2 * math.atan(math.tan(VERTICAL_FOV * 0.5) * ASPECT_RATIO) 
NEAR = 0.01
FAR = 2000.0
PITCH_MAX = glm.radians(89)

VERTICAL_FOV, ASPECT_RATIO, NEAR, FAR
MAXFPS = 90

MOUSE_SENSITIVITY = 0.0015
PLAYER_SIZE = 0.005
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.004
PLAYER_HEIGHT = 0.65
PLAYER_POS = glm.vec3(1.5, PLAYER_HEIGHT, 1.5)

PLAYER_INIT_HEALTH = 80
PLAYER_INIT_AMMO = 25
MAX_HEALTH_VALUE = 100
MAX_AMMO_VALUE = 999

LEVELS = 2
BACKGROUND = glm.vec3(0.1, 0.16, 0.25)
TEXTURE_SIZE = 256
TEXTURE_UNIT = 0

WALL_SIZE = 300
HORIZONTAL_WALL_SIZE = WALL_SIZE 
SYNC = 10 
RAYCAST_DISTANCE = 50

ANIMATION_DOOR_SPEED = 0.01

MAX_SOUND_CHANNELS = 10
NUM_TEXTURES = len(ID)

ITEM_SETTINGS = {
    ID.AMMO: {
        'scale': 0.2,
        'value': 8
    },
    ID.MED_KIT: {
        'scale': 0.3,
        'value': 20
    },
    ID.PISTOL_ICON: {
        'scale': 1.0
    },
    ID.RIFLE_ICON: {
        'scale': 1.0
    },
    ID.KEY: {
        'scale': 0.9
    }
}

# hud object IDs
ID.HEALTH_DIGIT_0 = 0 + NUM_TEXTURES
ID.HEALTH_DIGIT_1 = 1 + NUM_TEXTURES
ID.HEALTH_DIGIT_2 = 2 + NUM_TEXTURES
ID.AMMO_DIGIT_0 = 3 + NUM_TEXTURES
ID.AMMO_DIGIT_1 = 4 + NUM_TEXTURES
ID.AMMO_DIGIT_2 = 5 + NUM_TEXTURES
ID.FPS_DIGIT_0 = 6 + NUM_TEXTURES
ID.FPS_DIGIT_1 = 7 + NUM_TEXTURES
ID.FPS_DIGIT_2 = 8 + NUM_TEXTURES
ID.FPS_DIGIT_3 = 9 + NUM_TEXTURES

HUD_SETTINGS = {
    ID.HEALTH_DIGIT_0: {
        'scale': 0.1,
        'pos': glm.vec2(0.85, -0.95),
    },
    ID.HEALTH_DIGIT_1: {
        'scale': 0.1,
        'pos': glm.vec2(0.90, -0.95),
    },
    ID.HEALTH_DIGIT_2: {
        'scale': 0.1,
        'pos': glm.vec2(0.95, -0.95),
    },
    ID.AMMO_DIGIT_0: {
        'scale': 0.1,
        'pos': glm.vec2(-0.95, -0.95),
    },
    ID.AMMO_DIGIT_1: {
        'scale': 0.1,
        'pos': glm.vec2(-0.90, -0.95),
    },
    ID.AMMO_DIGIT_2: {
        'scale': 0.1,
        'pos': glm.vec2(-0.85, -0.95),
    },
    ID.AMMO: {
        'scale': 0.25,
        'pos': glm.vec2(-0.9, -0.82),
    },
    ID.MED_KIT: {
        'scale': 0.25,
        'pos': glm.vec2(0.9, -0.82),
    },
    ID.FPS_DIGIT_0: {
        'scale': 0.11,
        'pos': glm.vec2(-0.75, 0.87),
    },
    ID.FPS_DIGIT_1: {
        'scale': 0.11,
        'pos': glm.vec2(-0.68, 0.87),
    },
    ID.FPS_DIGIT_2: {
        'scale': 0.11,
        'pos': glm.vec2(-0.61, 0.87),
    },
    ID.FPS_DIGIT_3: {
        'scale': 0.11,
        'pos': glm.vec2(-0.54, 0.87),
    },
    ID.FPS: {
        'scale': 0.35,
        'pos': glm.vec2(-0.89, 0.74),
    },
    ID.YELLOW_SCREEN: {
        'scale': 4.0,
        'pos': glm.vec2(0.0, -2.0),
    },
    ID.RED_SCREEN: {
        'scale': 4.0,
        'pos': glm.vec2(0.0, -2.0),
    },
}

# weapon settings
WEAPON_SCALE = 1.9
WEAPON_NUM_FRAMES = 5
WEAPON_POS = glm.vec3(0.0, -1.0, 0.0)
WEAPON_ANIM_PERIODS = 4

WEAPON_SETTINGS = {
    ID.KNIFE_0: {
        'ammo_consumption': 0,
        'damage': 8,
        'max_dist': 2,
        'miss_probability': 0.3
    },
    ID.PISTOL_0: {
        'ammo_consumption': 0,
        'damage': 20,
        'max_dist': 10,
        'miss_probability': 0.1
    },
    ID.RIFLE_0: {
        'ammo_consumption': 2,
        'damage': 41,
        'max_dist': 30,
        'miss_probability': 0.045
    },
}

# npc settings
NPC_SETTINGS = {
    #
    ID.SOLDIER_BROWN_0: {
        'scale': glm.vec3(1.00),
        'anim_periods': 9,
        'num_frames': {
            'walk': 4, 'attack': 2, 'hurt': 2, 'death': 5
        },
        'state_tex_id': {
            'walk': ID.SOLDIER_BROWN_0,
            'attack': ID.SOLDIER_BROWN_0 + 4,
            'hurt': ID.SOLDIER_BROWN_0 + 6,
            'death': ID.SOLDIER_BROWN_0 + 6,
        },
        'attack_dist': 3,
        'health': 10,
        'speed': 0.004,
        'size': 0.3,
        'damage': 90,
        'hit_probability': 0.001,
        'drop_item': ID.AMMO
    },
    #
    ID.SOLDIER_BLUE_0: {
        'scale': glm.vec3(0.85),
        'anim_periods': 9,
        'num_frames': {
            'walk': 4, 'attack': 2, 'hurt': 2, 'death': 5
        },
        'state_tex_id': {
            'walk': ID.SOLDIER_BLUE_0,
            'attack': ID.SOLDIER_BLUE_0 + 4,
            'hurt': ID.SOLDIER_BLUE_0 + 6,
            'death': ID.SOLDIER_BLUE_0 + 6,
        },
        'attack_dist': 4,
        'health': 10,
        'speed': 0.0045,
        'size': 0.3,
        'damage': 1000,
        'hit_probability': 0.0015,
        'drop_item': ID.AMMO
    },
    #
    ID.RAT_0: {
        'scale': glm.vec3(1.0),
        'anim_periods': 12,
        'num_frames': {
            'walk': 4, 'attack': 3, 'hurt': 2, 'death': 5
        },
        'state_tex_id': {
            'walk': ID.RAT_0,
            'attack': ID.RAT_0 + 4,
            'hurt': ID.RAT_0 + 7,
            'death': ID.RAT_0 + 7,
        },
        'attack_dist': 0.6,
        'health': 10,
        'speed': 0.0045,
        'size': 0.2,
        'damage': 50,
        'hit_probability': 0.002,
        'drop_item': ID.AMMO
    },
}
