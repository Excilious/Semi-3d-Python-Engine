from Enviroment.Player import *
from Enviroment.Scene import *
from Enviroment.Shader import *
from Enviroment.Characters.PathFinding import *
from Enviroment.Raycasting import *
from Enviroment.LevelMap import *
from Enviroment.Textures import *
from Enviroment.Sound import *
from Enviroment.InstanceRendering.Mesh import *
from Enviroment.Lighting import *


class Engine:
    def __init__(self,Application):
        self.Application = Application
        self.Context = Application.Context
        self.Level = 0

        self.Textures = Textures(self)
        self.Sound = Sound()

        self.PlayerAttributes = PlayerAttributes()
        self.Player: Player = None
        self.Shader: ShaderProgram = None
        self.Scene: Scene = None

        self.LevelMap: LevelMap = None
        self.Raycasting: RayCasting = None
        self.PathFinding: PathFinder = None
        self.NewGame()

    def NewGame(self):
        pygame.mixer.music.play(-1)
        self.Player = Player(self)
        self.Shader = ShaderProgram(self)
        self.Lighting = PointLight()
        self.Mesh = Mesh(self)
        self.LevelMap = LevelMap(
            self, TMXFile=f'level_{self.PlayerAttributes.Level}.tmx'
        )
        self.Raycasting = RayCasting(self)
        self.PathFinding = PathFinder(self)
        self.Scene = Scene(self)

    def UpdateNPCMap(self):
        NPCMap = {}
        for Npc in self.LevelMap.NPCList:
            if (Npc.Module.IsAlive):
                NPCMap[Npc.Module.TilePosition] = Npc
            else:
                self.LevelMap.NPCList.remove(Npc)
        self.LevelMap.NPCMap = NPCMap

    def Events(self,Event):
        self.Player.Events(Event=Event)

    def Update(self):
        self.UpdateNPCMap()
        self.Player.Update()
        self.Shader.Update()
        self.Scene.Update()

    def Render(self):
        self.Scene.Render()
