
import math

import glm
from numba import njit
import numpy as np

# Display settings.
WIN_RES = glm.vec2(1600, 900)

# Chunk settings.
CHUNK_SIZE = 32
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOLUME = CHUNK_AREA * CHUNK_SIZE

# Camera settings.
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEGREES = 50
FOV_VERTICAL = glm.radians(FOV_DEGREES)
FOV_HORIZONTAL = 2 * math.atan(math.atan(FOV_VERTICAL * 0.5) * ASPECT_RATIO)
NEAR = 0.1
FAR = 2000.0
PITCH_MAX = glm.radians(89)

# Player settings.
PLAYER_SPEED = 0.005
PLAYER_ROTATION_SPEED = 0.003
PLAYER_POSITION = glm.vec3(H_CHUNK_SIZE, CHUNK_SIZE, 1.5 * CHUNK_SIZE)
MOUSE_SENSITIVITY = 0.002

# Colors
BACKGROUND_COLOR = glm.vec3(0.0627, 0.0902, 0.1255)
