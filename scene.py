
from settings import *
from meshes.quad_mesh import QuadMesh

class Scene:
    def __init__(self, engine):
        self.engine = engine
        self.quad = QuadMesh(self.engine)

    def update(self):
        pass

    def render(self):
        self.quad.render()
