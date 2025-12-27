
from settings import *
from world_objects.chunk import Chunk

class World:
    """
    3D voxel world management class that handles chunk organization and rendering.

    The World class manages the collection of chunks that make up the 3D voxel world.
    It handles chunk creation, voxel data management, mesh building, and rendering
    of the entire world structure.
    """

    def __init__(self, engine):
        """
        Initialize the world with engine reference and create all chunks.

        Args:
            engine: Reference to the main VoxelEngine instance
        """
        self.engine = engine
        self.chunks = [None for _ in range(WORLD_VOLUME)]
        self.voxels = np.empty([WORLD_VOLUME, CHUNK_VOLUME], dtype='uint8')
        self.build_chunks()
        self.build_chunk_mesh()

    def build_chunks(self):
        """
        Create all chunks in the world and initialize their voxel data.

        Iterates through all world coordinates, creates Chunk objects,
        and stores them in the chunks array. Also builds voxel data
        for each chunk and stores it in the central voxels array.
        """
        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT):
                for z in range(WORLD_DEPTH):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_index = x + WORLD_WIDTH * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    # Put the chunk voxels in a separate array
                    self.voxels[chunk_index] = chunk.build_voxels()

                    # Get pointer to voxels
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        """
        Build meshes for all chunks in the world.

        Iterates through all chunks and calls their build_mesh method
        to generate the OpenGL-compatible mesh data for rendering.
        """
        for chunk in self.chunks:
            chunk.build_mesh()

    def update(self):
        """
        Update world state.

        Currently a placeholder for future world update logic.
        Will handle dynamic world changes, chunk loading/unloading,
        and other world management tasks.
        """
        pass

    def render(self):
        """
        Render all chunks in the world.

        Iterates through all chunks and calls their render method
        to draw the entire 3D voxel world.
        """
        for chunk in self.chunks:
            chunk.render()
