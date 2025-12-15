
from settings import *
from meshes.base_mesh import BaseMesh

class QuadMesh(BaseMesh): 
    def __init__(self, engine):
        super().__init__()

        self.engine = engine
        self.ctx = engine.ctx
        self.program = engine.shader_program.quad

        # VAO information
        self.vbo_format = '3f 3f'
        self.attributes = ('in_position', "in_color")
        self.vao = self.get_vao()
    
    def get_vertex_data(self):
        vertices = [
            (0.5, 0.5, 0.0), (-0.5, 0.5, 0.0), (-0.5, -0.5, 0.0),
            (0.5, 0.5, 0.0), (-0.5, -0.5, 0.0), (0.5, -0.5, 0.0)
        ]

        colors = [
            (0, 1, 0), (1, 0, 0), (1, 1, 0),
            (0, 1, 0), (1, 1, 0), (0, 0, 1)
        ]

        vertex_data = np.hstack([vertices, colors], dtype='float32')
        return vertex_data
