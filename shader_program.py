
from settings import *

class ShaderProgram:

    def __init__(self, engine):
        self.engine = engine
        self.ctx = engine.ctx
        self.player = engine.player

        # Shaders
        self.quad = self.get_program(shader_name='quad')

        self.set_uniforms_on_init()
    
    def set_uniforms_on_init(self):
        # Pass the CPU-calculated player positional data into the vertex shader.
        self.quad['m_projection'].write(self.player.m_projection)
        self.quad['m_model'].write(glm.mat4())

    def update(self):
        self.quad['m_view'].write(self.player.m_view)
    
    # This function binds shaders into the engine by reading contents from shader files.
    def get_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program