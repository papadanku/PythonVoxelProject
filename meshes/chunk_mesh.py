
from meshes.base_mesh import BaseMesh
from meshes.chunk_mesh_builder import build_chunk_mesh

class ChunkMesh(BaseMesh):
    """
    Specialized mesh class for rendering voxel chunks.

    The ChunkMesh class extends BaseMesh to provide optimized rendering
    of 3D voxel chunks. It handles the conversion of voxel data into
    renderable geometry with proper vertex attributes for position,
    voxel ID, and face identification.

    :var engine: Reference to the main VoxelEngine instance
    :var chunk: Reference to the parent Chunk instance
    :var ctx: OpenGL context for rendering
    :var program: Shader program for chunk rendering
    :var vbo_format: Vertex buffer format string
    :var format_size: Size of each vertex in the format
    :var attributes: Vertex attribute names for shader binding
    :var vao: Vertex array object for rendering
    """

    def __init__(self, chunk):
        """
        Initialize the chunk mesh with reference to its parent chunk.

        :param chunk: Parent Chunk object containing voxel data
        """
        super().__init__()

        self.engine = chunk.engine
        self.chunk = chunk
        self.ctx = self.engine.ctx
        self.program = self.engine.shader_program.chunk

        # Vertex buffer format: 3 unsigned bytes for position, 1 for voxel ID, 1 for face ID
        self.vbo_format = '3u1 1u1 1u1'
        # Total size of each vertex in the format
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        # Vertex attribute names for shader binding
        self.attributes = ('in_position', 'voxel_id', 'face_id')
        self.vao = self.get_vao()

    def get_vertex_data(self):
        """
        Generate vertex data from chunk voxel data.

        Uses the chunk mesh builder to convert voxel data into
        optimized vertex data for rendering, including face culling
        to avoid rendering hidden faces.

        :return: Numpy array containing vertex data for all visible voxel faces
        :rtype: numpy.ndarray
        """
        mesh = build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,
            format_size=self.format_size,
            chunk_position=self.chunk.position,
            world_voxels=self.chunk.world.voxels
        )
        return mesh