from Settings import *
from Enviroment.TextureBuilder import TextureArrayBuilder

class Textures:
    TextureStorage = {}
    def __init__(self, Engine):
        self.Engine = Engine
        self.Context = Engine.Context
        TextureArrayBuilder(Build=True)

        self.TextureArray = self.Load('TextureArray/TextureArray.png')
        self.TextureArray.use(location=TEXTURE_UNIT)
        Textures.TextureStorage[0] = self.GetTexture(Path='Resources/Assets/MeshTextures/Placeholder.png')
        Textures.TextureStorage["BulletCase"] = self.GetTexture(Path='Resources/Assets/MeshTextures/BulletCrate.png')
        Textures.TextureStorage["PistolTexture"] = self.GetTexture(Path='Resources/Assets/MeshTextures/Pistol.png')
        Textures.TextureStorage["ControlPanel"] = self.GetTexture(Path='Resources/Assets/MeshTextures/ControlPanel.jpg')
        Textures.TextureStorage["Robot"] = self.GetTexture(Path='Resources/Assets/MeshTextures/Robot.png')
        Textures.TextureStorage["RobotAlternate"] = self.GetTexture(Path='Resources/Assets/MeshTextures/RobotAlternate.png')
        Textures.TextureStorage["Gun"] = self.GetTexture(Path="Resources/Assets/MeshTextures/Gun.jpg")
        Textures.TextureStorage["Bookshelf"] = self.GetTexture(Path='Resources/Assets/MeshTextures/Bookshelf.png')

        Textures.TextureStorage["DepthTexture"] = self.GetDepthTexture()
 
    def GetTexture(self,Path):
        Texture = pygame.image.load(Path).convert()
        Texture = pygame.transform.flip(Texture, flip_x=False,flip_y=True)
        Texture = self.Context.texture(size=Texture.get_size(),components=3,data=pygame.image.tostring(Texture, 'RGB'))

        Texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        Texture.build_mipmaps()
        Texture.anisotropy = 32.0
        return Texture

    def GetDepthTexture(self):
        DepthTexture = self.Context.depth_texture((int(RESOLUTION.x),int(RESOLUTION.y)))
        DepthTexture.repeat_x = False
        DepthTexture.repeat_y = False
        return DepthTexture

    def Load(self,FilePath):
        Texture = pygame.image.load(f'Resources/Assets/{FilePath}')
        Texture = pygame.transform.flip(Texture, flip_x=True, flip_y=False)

        NumberLayers = Texture.get_height() // Texture.get_width()
        Texture = self.Engine.Context.texture_array(
            size=(Texture.get_width(), Texture.get_height() // NumberLayers, NumberLayers),
            components=4,
            data=pygame.image.tostring(Texture, 'RGBA', False)
        )

        Texture.anisotropy = 32.0
        Texture.build_mipmaps()
        Texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        return Texture
