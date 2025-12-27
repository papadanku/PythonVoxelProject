
from settings import *
from meshes.chunk_mesh import ChunkMesh

class Chunk:
    def __init__(self, engine):
        self.engine = engine
        self.voxels: np.array = self.build_voxels()
        self.mesh: ChunkMesh = None
        self.build_mesh()

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        self.mesh.render()

    def build_voxels(self):
        # Empty chunk
        voxels = np.zeros(CHUNK_VOLUME, dtype='uint8')

        # Fill chunk
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = 1
        
        return voxels