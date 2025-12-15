
import numpy as np

class BaseMesh:
    def __init__(self):
        # OpenGL context
        self.ctx = None
        # Shader program
        self.program = None
        # Vertex buffer data type format: "3f 3f"
        self.vbo_format = None
        # Attribute names 
        self.attributes: tuple[str, ...] = None
        # Vertex array objects
        self.vao = None

    def get_vertex_data(self) -> np.array: ...

    def get_vao(self):
        # Creates a VAO, an object that interprets the purpose of the data stored in the VBO
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        vao = self.ctx.vertex_array(
            self.program,
            [
                (vbo, self.vbo_format, *self.attributes)
            ],
            skip_errors=True
        )
        return vao

    def render(self):
        self.vao.render()
