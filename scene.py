
from settings import *
from world import World
from world_objects.voxel_marker import VoxelMarker

class Scene:
    """
    Scene management class that handles 3D world composition and rendering.

    The Scene class manages the collection of world objects including chunks, coordinates their updates, and handles the rendering of the entire 3D world.

    :var engine: Reference to the main VoxelEngine instance
    :var world: World instance containing all chunks and voxels
    """

    def __init__(self, engine):
        """
        Initialize the scene with engine reference and create initial world objects.

        :param engine: Reference to the main VoxelEngine instance
        """
        self.engine = engine
        self.world = World(self.engine)
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)

    def update(self):
        """
        Update all scene objects.

        Currently a placeholder for future scene update logic.

        Will handle updates for multiple chunks and world objects.
        """
        self.world.update()
        self.voxel_marker.update()

    def render(self):
        """
        Render all objects in the scene.

        Delegates rendering to all contained world objects, currently just the single world.
        """
        self.world.render()
        self.voxel_marker.render()
