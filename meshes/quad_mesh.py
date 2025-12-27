
from settings import *
from meshes.base_mesh import BaseMesh

class QuadMesh(BaseMesh):
    """
    Simple 2D quad mesh for debugging and testing purposes.

    The QuadMesh class creates a basic 2D quad (two triangles) with
    colored vertices. It's primarily used for testing the rendering
    pipeline and shader functionality during development.
    """

    def __init__(self, engine):
        """
        Initialize the quad mesh with engine context.

        Args:
            engine: Reference to the main VoxelEngine instance
        """
        super().__init__()

        self.engine = engine
        self.ctx = engine.ctx
        self.program = engine.shader_program.quad

        # VAO information
        # Vertex buffer format: 3 floats for position, 3 floats for color
        self.vbo_format = '3f 3f'
        # Vertex attribute names for shader binding
        self.attributes = ('in_position', "in_color")
        self.vao = self.get_vao()

    def get_vertex_data(self):
        """
        Generate vertex data for a colored quad.

        Returns:
            numpy array containing vertex positions and colors

        Creates vertex data for two triangles forming a quad with
        different colored vertices for visual distinction.
        """
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
