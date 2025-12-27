
import math

import glm
from numba import njit
import numpy as np

# Configuration settings for the Python Voxel Project
# This file contains all global constants and parameters used throughout the engine

import math
import glm
from numba import njit
import numpy as np

# Display settings
WIN_RES = glm.vec2(1600, 900)
"""Window resolution in pixels (width, height). Defines the size of the game window."""

# Chunk settings
CHUNK_SIZE = 32
"""Size of each chunk in voxels along one dimension. Chunks are cubic."""
HORIZONTAL_CHUNK_SIZE = CHUNK_SIZE // 2
"""Half of CHUNK_SIZE, used for center calculations."""
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
"""Area of a chunk in voxels (CHUNK_SIZE squared)."""
CHUNK_VOLUME = CHUNK_AREA * CHUNK_SIZE
"""Volume of a chunk in voxels (CHUNK_SIZE cubed)."""

# World settings
WORLD_WIDTH, WORLD_HEIGHT = 10, 3
"""World dimensions in chunks (width, height)."""
WORLD_DEPTH = WORLD_WIDTH
"""World depth in chunks, equal to width for square worlds."""
WORLD_AREA = WORLD_WIDTH * WORLD_DEPTH
"""Total world area in chunks (WORLD_WIDTH * WORLD_DEPTH)."""
WORLD_VOLUME = WORLD_AREA * WORLD_HEIGHT
"""Total world volume in chunks (WORLD_AREA * WORLD_HEIGHT)."""

# World center settings
CENTER_XZ = WORLD_WIDTH * HORIZONTAL_CHUNK_SIZE
"""X and Z coordinate of the world center in voxels."""
CENTER_Y = WORLD_HEIGHT * HORIZONTAL_CHUNK_SIZE
"""Y coordinate of the world center in voxels."""

# Camera settings
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
"""Aspect ratio of the window (width/height)."""
FOV_DEGREES = 50
"""Field of view in degrees for the camera."""
FOV_VERTICAL = glm.radians(FOV_DEGREES)
"""Vertical field of view in radians."""
FOV_HORIZONTAL = 2 * math.atan(math.atan(FOV_VERTICAL * 0.5) * ASPECT_RATIO)
"""Horizontal field of view in radians, calculated from vertical FOV and aspect ratio."""
NEAR = 0.1
"""Near clipping plane distance for the camera."""
FAR = 2000.0
"""Far clipping plane distance for the camera."""
PITCH_MAX = glm.radians(89)
"""Maximum pitch angle in radians to prevent camera flipping."""

# Player settings
PLAYER_SPEED = 0.005
"""Base movement speed for the player."""
PLAYER_ROTATION_SPEED = 0.003
"""Rotation speed for the player."""
PLAYER_POSITION = glm.vec3(CENTER_XZ, WORLD_HEIGHT * CHUNK_SIZE, CENTER_XZ)
"""Initial player position at the center of the world."""
MOUSE_SENSITIVITY = 0.002
"""Mouse sensitivity for camera rotation."""

# Colors
BACKGROUND_COLOR = glm.vec3(0.0627, 0.0902, 0.1255)
"""Background color of the scene in RGB values (dark blue)."""
