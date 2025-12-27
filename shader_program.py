
from settings import *

class ShaderProgram:
    """
    Shader program management class for OpenGL rendering.

    The ShaderProgram class handles the creation, compilation, and management
    of OpenGL shader programs. It loads shader source code from files,
    compiles them, and manages uniform variable updates for rendering.

    :var engine: Reference to the main VoxelEngine instance
    :var ctx: OpenGL context for shader operations
    :var player: Reference to the player for camera data
    :var chunk: Shader program for chunk rendering
    """

    def __init__(self, engine):
        """
        Initialize shader programs with engine context.

        :param engine: Reference to the main VoxelEngine instance
        """
        self.engine = engine
        self.ctx = engine.ctx
        self.player = engine.player

        # Shaders
        self.chunk = self.get_program(shader_name='chunk')

        self.set_uniforms_on_init()

    def set_uniforms_on_init(self):
        """
        Set initial uniform values for shader programs.

        Configures projection matrix, model matrix, and texture units
        that remain constant or change infrequently during rendering.
        """
        # Pass the CPU-calculated player positional data into the vertex shader.
        self.chunk['m_projection'].write(self.player.m_projection)
        self.chunk['m_model'].write(glm.mat4())
        self.chunk['u_texture_0'] = 0

    def update(self):
        """
        Update shader uniforms that change frequently.

        Updates the view matrix each frame based on current
        camera position and orientation.
        """
        self.chunk['m_view'].write(self.player.m_view)

    def get_program(self, shader_name):
        """
        Load and compile a shader program from source files.

        Reads vertex and fragment shader source code from files,
        compiles them, and returns a ready-to-use shader program.

        :param shader_name: Base name of shader files (without extension)
        :return: Compiled shader program ready for use
        :rtype: moderngl.Program
        """
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program