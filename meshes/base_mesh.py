
import numpy as np

class BaseMesh:
    """
    Abstract base class for all mesh types in the voxel engine.

    The BaseMesh class provides the fundamental interface and functionality
    for creating and rendering 3D meshes. It handles vertex buffer objects,
    vertex array objects, and the rendering pipeline. Subclasses must
    implement get_vertex_data() to provide mesh-specific geometry data.

    :var ctx: OpenGL context for rendering
    :var program: Shader program for mesh rendering
    :var vbo_format: Vertex buffer format string
    :var attributes: Vertex attribute names for shader binding
    :var vao: Vertex array object for rendering
    """

    def __init__(self):
        """
        Initialize base mesh properties.

        Sets up the fundamental properties needed for mesh rendering:
        - OpenGL context reference
        - Shader program reference
        - Vertex buffer format specification
        - Vertex attribute names
        - Vertex array object
        """
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

    def get_vertex_data(self) -> np.array:
        """
        Get vertex data for this mesh (to be implemented by subclasses).

        This abstract method must be implemented by concrete mesh classes
        to provide the actual geometry data for rendering.

        :return: Numpy array containing vertex data in the specified format
        :rtype: numpy.ndarray
        """
        ...

    def get_vao(self):
        """
        Create a vertex array object for this mesh.

        Generates a VAO that interprets the vertex data stored in the VBO.
        The VAO defines how the vertex data should be processed by the
        shader program during rendering.

        :return: Configured vertex array object ready for rendering
        :rtype: moderngl.VertexArray
        """
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
        """
        Render this mesh.

        Executes the OpenGL draw call to render the mesh using
        its vertex array object.
        """
        self.vao.render()
