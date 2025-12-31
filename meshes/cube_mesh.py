
from settings import *
from meshes.base_mesh import BaseMesh

class CubeMesh(BaseMesh):
    """
    Specialized mesh class for rendering cube geometry.

    The CubeMesh class extends BaseMesh to provide optimized rendering of cube geometry. It's primarily used for the voxel marker that indicates which voxel the player is currently targeting. The mesh includes both vertex position and texture coordinate data for rendering.

    :var engine: Reference to the main VoxelEngine instance
    :var ctx: OpenGL context for rendering
    :var program: Shader program for cube rendering
    :var vbo_format: Vertex buffer format string
    :var attributes: Vertex attribute names for shader binding
    :var vao: Vertex array object for rendering
    """

    def __init__(self, engine):
        """
        Initialize the cube mesh with engine reference.

        :param engine: Reference to the main VoxelEngine instance
        """
        super().__init__()
        self.engine = engine
        self.ctx = self.engine.ctx
        self.program = self.engine.shader_program.voxel_marker

        # VBO-VAO settings
        self.vbo_format = '2f2 3f2'
        self.attributes = ('in_tex_coord_0', 'in_position',)
        self.vao = self.get_vao()

    @staticmethod
    def get_data(vertices, indices):
        """
        Extract vertex data from vertices and indices.

        :param vertices: List of vertex positions
        :param indices: List of triangle indices
        :return: Numpy array containing vertex data in the order specified by indices
        :rtype: numpy.ndarray
        """
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='float16')

    def get_vertex_data(self):
        """
        Generate vertex data for a unit cube.

        Creates vertex position and texture coordinate data for a unit cube centered at the origin. The cube consists of 12 triangles (6 faces * 2 triangles).

        :return: Numpy array containing interleaved texture coordinate and position data
        :rtype: numpy.ndarray
        """

        # Vertex data for cube
        vertices = [
            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1),
            (0, 1, 0), (0, 0, 0), (1, 0, 0), (1, 1, 0)
        ]
        indices = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (1, 6, 7),
            (6, 5, 4), (4, 7, 6),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6)
        ]
        vertex_data = self.get_data(vertices, indices)

        # Texture coordinate data for cube
        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3), (0, 1, 2),
            (0, 2, 3), (0, 1, 2),
            (0, 1, 2), (2, 3, 0),
            (2, 3, 0), (2, 0, 1),
            (0, 2, 3), (0, 1, 2),
            (3, 1, 2), (3, 0, 1),
        ]

        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)
        vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data
