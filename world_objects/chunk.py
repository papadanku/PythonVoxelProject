
import random

from settings import *
from meshes.chunk_mesh import ChunkMesh

class Chunk:
    """
    3D chunk class that manages a grid of voxels and their rendering.

    The Chunk class represents a 3D grid of voxels (32*32*32) that forms the basic building block of the voxel world. It handles voxel data generation, mesh creation, and rendering of the chunk.

    :var engine: Reference to the main VoxelEngine instance
    :var world: Reference to the parent World instance
    :var position: Chunk position in world coordinates
    :var m_model: Model matrix for chunk transformation
    :var voxels: Numpy array containing voxel data
    :var mesh: ChunkMesh object for rendering
    :var is_empty: Flag indicating if chunk contains any voxels
    """

    def __init__(self, world, position):
        """
        Initialize the chunk with engine reference and generate voxel data.

        :param world: Reference to the parent World instance
        :param position: Chunk position in world coordinates
        """
        self.engine = world.engine
        self.world = world
        self.position = position
        self.m_model = self.get_model_matrix()
        self.voxels: np.array = None
        self.mesh: ChunkMesh = None
        self.is_empty = True

        self.center = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
        self.is_on_frustum = self.engine.player.frustum.is_on_frustum

    def get_model_matrix(self):
        """
        Calculate the model matrix for this chunk.

        Creates a transformation matrix that positions the chunk in world space based on its chunk coordinates.

        :return: Model matrix that transforms chunk coordinates to world space
        :rtype: mat4
        """
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model

    def set_uniform(self):
        """
        Update shader uniforms for this chunk.

        Writes the model matrix to the shader program so the chunk can be rendered in the correct position in world space.
        """
        self.mesh.program['m_model'].write(self.m_model)

    def build_mesh(self):
        """
        Create the renderable mesh for this chunk.

        Generates a ChunkMesh object that converts the voxel data into optimized geometry for rendering.
        """
        self.mesh = ChunkMesh(self)

    def render(self):
        """
        Render this chunk.

        Delegates rendering to the chunk's mesh object.
        """
        if not self.is_empty and self.is_on_frustum(self):
            self.set_uniform()
            self.mesh.render()

    def build_voxels(self):
        """
        Generate procedural voxel data for this chunk.

        Creates a 3D array of voxel values using simplex noise to generate interesting terrain patterns. Voxel values are determined by position and noise, creating a procedural world structure.

        :return: Numpy array containing voxel data for the entire chunk
        :rtype: numpy.ndarray
        """
        # Create empty chunk
        voxels = np.zeros(CHUNK_VOLUME, dtype='uint8')

        # Generate voxel data
        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE
        random_number = random.randrange(1, 100)

        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                wx = x + cx
                wz = z + cz
                world_height = int(glm.simplex(glm.vec2(wx, wz) * 0.01) * 32 + 32)
                local_height = min(world_height - cy, CHUNK_SIZE)

                for y in range(local_height):
                    wy = y + cy
                    voxel_index = x + CHUNK_SIZE * z + CHUNK_AREA * y
                    voxels[voxel_index] = random_number

        if np.any(voxels):
            self.is_empty = False

        return voxels