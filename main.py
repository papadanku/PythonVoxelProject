
import sys

import moderngl as mgl
import pygame as pg

from settings import *
from shader_program import ShaderProgram
from scene import Scene
from player import Player
from textures import Textures

class VoxelEngine:
    """
    Main engine class that initializes and manages the 3D voxel game engine.

    The VoxelEngine handles OpenGL context creation, window management,
    core system initialization, and the main game loop. It coordinates
    all major subsystems including rendering, player input, and scene management.
    """

    def __init__(self):
        """
        Initialize the voxel engine with OpenGL context and core systems.

        Sets up Pygame, creates an OpenGL 3.3 Core context, configures the
        display window, and initializes all engine subsystems including
        textures, player control, shaders, and scene management.
        """
        pg.init()

        # We will use OpenGL 3.3 Core with a 24-integer depth buffer.
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)

        # Our window display settings.
        pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)

        # Prevent the mouse from displaying outside the border.
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        # The VoxelEngine will have a context.
        self.ctx = mgl.create_context()

        # Enable depth testing, face culling, and buffer blending.
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)

        # Automatic garbage collection.
        self.ctx.gc_mode = 'auto'

        # Time data.
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0
        self.is_running = True

        self.on_init()

    def on_init(self):
        """
        Initialize all engine subsystems.

        Creates and configures the core engine components including texture
        management, player control, shader programs, and scene rendering.
        """
        # Initialize essential engine data.
        self.texture = Textures(self)
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)

    def update(self):
        """
        Update all engine systems and track performance metrics.

        Updates player input, shader uniforms, and scene state. Calculates
        delta time and total elapsed time for smooth animations and
        physics. Updates the window caption with current FPS.
        """
        self.player.update()
        self.shader_program.update()
        self.scene.update()

        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        pg.display.set_caption(f'{self.clock.get_fps() : .0f}')

    def render(self):
        """
        Render the current frame.

        Clears the screen, renders all scene objects, and presents the
        final frame to the display. Handles OpenGL buffer swapping.
        """
        self.ctx.clear(color=BACKGROUND_COLOR)
        self.scene.render()
        pg.display.flip()

    def handle_events(self):
        """
        Process system and user input events.

        Handles window close events and keyboard input. Checks for quit
        conditions including window close button and ESC key press.
        """
        # Discontinue the engine from running if the user quits or hits certain keys.
        for event in pg.event.get():
            if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False

    def run(self):
        """
        Execute the main game loop.

        Runs the continuous engine loop that processes events, updates
        game state, and renders frames until the user requests exit.
        Cleans up resources and exits gracefully when done.
        """
        # Execute the conditionally continuous rendering loop.
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()

        # Stop running if the user does something that stops self.is_running
        pg.quit()
        sys.exit()

if __name__ == '__main__':
    app = VoxelEngine()
    app.run()
