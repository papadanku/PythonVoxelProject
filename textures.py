
import pygame as pg
import moderngl as mgl

class Textures:
    def __init__(self, engine):
        self.engine = engine
        self.ctx = engine.ctx

        # Load texture
        self.texture_0 = self.load('frame.png')

        # Assign the texture unit so the shaders can use it
        self.texture_0.use(location=0)
    
    # Loads a texture and configures its sample state
    def load(self, file_name):
        texture = pg.image.load(f'assets/{file_name}')
        texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
        texture = self.ctx.texture(
            size=texture.get_size(),
            components=4,
            data=pg.image.tostring(texture, 'RGBA', False)
        )
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        return texture
