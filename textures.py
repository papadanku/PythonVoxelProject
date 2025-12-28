
import pygame as pg
import moderngl as mgl

class Textures:
    """
    Texture management class for loading and configuring OpenGL textures.

    The Textures class handles loading image files, converting them to
    OpenGL texture objects, and configuring their sampling parameters.
    It manages texture units and makes textures available to shaders.

    :var engine: Reference to the main VoxelEngine instance
    :var ctx: OpenGL context for texture operations
    :var texture_0: Main texture object for rendering
    """

    def __init__(self, engine):
        """
        Initialize texture manager with engine context.

        :param engine: Reference to the main VoxelEngine instance
        """
        self.engine = engine
        self.ctx = engine.ctx

        # Load texture
        self.texture_0 = self.load('frame.png')
        # self.texture_0 = self.load('test.png')

        # Assign the texture unit so the shaders can use it
        self.texture_0.use(location=0)

    def load(self, file_name):
        """
        Load an image file and create an OpenGL texture object.

        Loads the image, flips it appropriately for OpenGL coordinates,
        creates a texture object, and configures filtering and mipmapping.

        :param file_name: Name of the image file to load (from assets directory)
        :return: Configured OpenGL texture object ready for rendering
        :rtype: moderngl.Texture
        """
        texture = pg.image.load(f'assets/{file_name}')
        texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
        texture = self.ctx.texture(
            size=texture.get_size(),
            components=4,
            data=pg.image.tostring(texture, 'RGBA', False)
        )
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR_MIPMAP_LINEAR)
        return texture
