
from meshes.base_mesh import BaseMesh
from meshes.chunk_mesh_builder import build_chunk_mesh

class ChunkMesh(BaseMesh):
    def __init__(self, chunk):
        super().__init__()

        self.engine = chunk.engine
        self.chunk = chunk
        self.ctx = self.engine.ctx
        self.program = self.engine.shader_program.chunk

        self.vbo_format = '3u1 1u1 1u1'
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attributes = ('in_position', 'voxel_id', 'face_id')
        self.vao = self.get_vao()

    def get_vertex_data(self):
        mesh = build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,
            format_size=self.format_size
        )
        return mesh