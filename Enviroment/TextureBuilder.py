from Settings import *

class TextureArrayBuilder:
    def __init__(self,Build=True):
        if Build:
            self.Build(
                LoadPath='Resources/Assets/Textures',
                TextureArrayPath='Resources/Assets/TextureArray/TextureArray.png',
                SpriteSheetPath='Resources/Assets/SpriteSheet/SpriteSheet.png'
            )

    def Build(self,LoadPath,TextureArrayPath,SpriteSheetPath,TextureSize=TEXTURE_SIZE):
        TexturePath = [
            Item for Item in pathlib.Path(LoadPath).rglob('*.png') if Item.is_file()
        ]
        TexturePath = sorted(
            TexturePath,
            key=lambda tex_path: int(re.search('\\d+', str(tex_path)).group(0))
        )

        TextureArray = pygame.Surface([TextureSize,TextureSize * len(TexturePath)], pygame.SRCALPHA, 32)
        Size = int(math.sqrt(len(TexturePath))) + 1
        SheetSize = TextureSize * Size
        SpriteSheet = pygame.Surface([SheetSize,SheetSize], pygame.SRCALPHA, 32)

        for x,Path in enumerate(TexturePath):
            Texture = pygame.image.load(Path)
            TextureArray.blit(Texture,(0, x * TextureSize))
            SpriteSheet.blit(Texture, ((x % Size) * TextureSize, (x // Size) * TextureSize))

        pygame.image.save(SpriteSheet,SpriteSheetPath)
        pygame.image.save(TextureArray,TextureArrayPath)
