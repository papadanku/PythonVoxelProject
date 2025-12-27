
from settings import *
from world_objects.chunk import Chunk

class Scene:
    def __init__(self, engine):
        self.engine = engine
        self.chunk = Chunk(self.engine)

    def update(self):
        pass

    def render(self):
        self.chunk.render()
