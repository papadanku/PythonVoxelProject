
from settings import *
from meshes.chunk_mesh import ChunkMesh

class Chunk:
    """
    3D chunk class that manages a grid of voxels and their rendering.

    The Chunk class represents a 3D grid of voxels (32×32×32) that forms
    the basic building block of the voxel world. It handles voxel data
    generation, mesh creation, and rendering of the chunk.
    """

    def __init__(self, engine):
        """
        Initialize the chunk with engine reference and generate voxel data.

        Args:
            engine: Reference to the main VoxelEngine instance
        """
        self.engine = engine
        self.voxels: np.array = self.build_voxels()
        self.mesh: ChunkMesh = None
        self.build_mesh()

    def build_mesh(self):
        """
        Create the renderable mesh for this chunk.

        Generates a ChunkMesh object that converts the voxel data
        into optimized geometry for rendering.
        """
        self.mesh = ChunkMesh(self)

    def render(self):
        """
        Render this chunk.

        Delegates rendering to the chunk's mesh object.
        """
        self.mesh.render()

    def build_voxels(self):
        """
        Generate procedural voxel data for this chunk.

        Creates a 3D array of voxel values using simplex noise to
        generate interesting terrain patterns. Voxel values are
        determined by position and noise, creating a procedural
        world structure.

        Returns:
            numpy array containing voxel data for the entire chunk
        """
        # Empty chunk
        voxels = np.zeros(CHUNK_VOLUME, dtype='uint8')

        # Fill chunk
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = (
                        x + y + z if int(glm.simplex(glm.vec3(x, y, z) * 0.1) + 1) else 0
                    )

        return voxels