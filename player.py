
import pygame as pg

from settings import *
from camera import Camera

class Player(Camera):
    """
    Player class that extends Camera to provide first-person control.

    The Player class handles user input for movement and camera control,
    providing a first-person experience in the 3D voxel world. It processes
    keyboard input for movement and mouse input for looking around.
    """

    def __init__(self, engine, position=PLAYER_POSITION, yaw=-90, pitch=0):
        """
        Initialize the player with engine reference and starting position.

        Args:
            engine: Reference to the main VoxelEngine instance
            position: Initial 3D position (defaults to PLAYER_POSITION)
            yaw: Initial horizontal rotation in degrees (defaults to -90)
            pitch: Initial vertical rotation in degrees (defaults to 0)
        """
        super().__init__(position, yaw, pitch)

        self.engine = engine

    def update(self):
        """
        Update player state by processing input and camera orientation.

        Handles keyboard and mouse input, then updates the camera
        view matrix based on the new orientation.
        """
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def mouse_control(self):
        """
        Process mouse input for camera look control.

        Reads mouse movement and applies it to camera rotation.
        Horizontal mouse movement controls yaw (left/right), vertical
        movement controls pitch (up/down).
        """
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        """
        Process keyboard input for player movement.

        Checks keyboard state and moves the player accordingly:
        - W: Move forward
        - S: Move backward
        - D: Move right
        - A: Move left
        - Q: Move up
        - E: Move down

        Movement speed is scaled by delta time for consistent movement
        regardless of frame rate.
        """
        key_state = pg.key.get_pressed()
        velocity = PLAYER_SPEED * self.engine.delta_time

        if key_state[pg.K_w]:
            self.move_forward(velocity)
        if key_state[pg.K_s]:
            self.move_backward(velocity)
        if key_state[pg.K_d]:
            self.move_right(velocity)
        if key_state[pg.K_a]:
            self.move_left(velocity)
        if key_state[pg.K_q]:
            self.move_up(velocity)
        if key_state[pg.K_e]:
            self.move_down(velocity)
