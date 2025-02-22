from Settings import *
from Instances.Door import *
from Instances.Npc import *

from Enviroment.InstanceRendering.Model import *
from Enviroment.Characters.BehaviourSystem import *

class LevelMap:
    def __init__(self,Engine,TMXFile='test.tmx'):
        self.Engine = Engine
        self.TiledMap = pytmx.TiledMap(f'resources/levels/{TMXFile}')
        self.GIDMap = self.TiledMap.tiledgidmap

        self.ResourceItems = {
            ID.PISTOL_ICON: {
                "MeshID": "Resources/Assets/Meshes/Gun.obj",
                "TextureID": "PistolTexture"
            },
            ID.AMMO:{
                "MeshID": "Resources/Assets/Meshes/Gun.obj",
                "TextureID": "BulletCase"
            },
            ID.KEY:{
                "MeshID": "Resources/Assets/Meshes/Gun.obj",
                "TextureID": "Gun"
            },
            ID.MED_KIT:{
                "MeshID": "Resources/Assets/Meshes/Gun.obj",
                "TextureID": "BulletCase"
            },
            ID.RIFLE_ICON:{
                "MeshID": "Resources/Assets/Meshes/Gun.obj",
                "TextureID": "BulletCase"
            }
        }

        self.Width = self.TiledMap.width
        self.Depth = self.TiledMap.height

        self.WallMap,self.FloorMap,self.CeilingMap = {}, {}, {}
        self.DoorMap,self.ItemMap = {}, {}
        self.NPCMap, self.NPCList = {}, []
        self.ParseLevel()

    def GetID(self,GID):
        return self.GIDMap[GID] - 1

    def ParseLevel(self):
        Player = self.TiledMap.get_layer_by_name('player').pop()
        PlayerPosition = glm.vec3(Player.x/TEXTURE_SIZE,PLAYER_HEIGHT,Player.y/TEXTURE_SIZE)
        self.Engine.Player.Position = PlayerPosition

        Wall = self.TiledMap.get_layer_by_name('walls')
        Floors = self.TiledMap.get_layer_by_name('floors')
        Ceilings = self.TiledMap.get_layer_by_name('ceilings')

        for X in range(self.Width):
            for Z in range(self.Depth):
                if (Gid := Wall.data[Z][X]):
                    self.WallMap[(X,Z)] = self.GetID(Gid)
                if (Gid := Floors.data[Z][X]):
                    self.FloorMap[(X,Z)] = self.GetID(Gid)
                if (Gid := Ceilings.data[Z][X]):
                    self.CeilingMap[(X,Z)] = self.GetID(Gid)

        # DoorInstance = self.TiledMap.get_layer_by_name('doors')
        # for Object in DoorInstance:
        #     Position = int(Object.x/TEXTURE_SIZE), int(Object.y/TEXTURE_SIZE)
        #     print(Object.gid)
        #     DoorObject = Door(self,TextureID=self.GetID(Object.gid),X=Position[0],Z=Position[1])
        #     self.DoorMap[Position] = DoorObject

        ItemInstance = self.TiledMap.get_layer_by_name('items')
        for Object in ItemInstance:
            Position = int(Object.x/TEXTURE_SIZE), int(Object.y/TEXTURE_SIZE)
            ItemObject = MeshBrickModel(
                self.Engine,
                WorldSpaceName="Bullet_"+str(Position),
                MeshID=self.ResourceItems[self.GetID(Object.gid)]["MeshID"],
                Position=glm.vec3(Position[0],-0.15,Position[1]),
                Scale=glm.vec3(0.15,0.15,0.15),Rotation=glm.vec3(0,-90,0),
                TextureID=self.ResourceItems[self.GetID(Object.gid)]["TextureID"],VertexArrayName="Bullet_"+str(Position),
                ID = self.GetID(Object.gid)
                )
            self.ItemMap[Position] = ItemObject

        # BookShelf = self.TiledMap.get_layer_by_name('bookshelf')
        # for Object in BookShelf:
        #     Position = int(Object.x/TEXTURE_SIZE), int(Object.y/TEXTURE_SIZE)
        #     ItemObject = MeshBrickModel(
        #         self.Engine,
        #         WorldSpaceName="A"+str(Position),
        #         MeshID='Resources/Assets/Meshes/Bookshelf.obj',
        #         Position=glm.vec3(Position[0],-0.15,Position[1]),
        #         Scale=glm.vec3(1.5,1.5,1.5),Rotation=glm.vec3(0,-90,0),
        #         TextureID="Bookshelf",VertexArrayName="A"+str(Position),
        #         ID = self.GetID(Object.gid)
        #         )
        #     self.ItemMap[Position] = ItemObject

        NPCInstance = self.TiledMap.get_layer_by_name('npc')
        for Object in NPCInstance:
            Position = int(Object.x/TEXTURE_SIZE), int(Object.y/TEXTURE_SIZE)
            NPCObject = MeshBrickModel(
                self.Engine,
                WorldSpaceName="Character_"+str(Position),
                MeshID="Resources/Assets/Meshes/Robot.obj",
                Position=glm.vec3(Position[0],0.5,Position[1]-0.05),
                Scale=glm.vec3(0.022,0.022,0.022),Rotation=glm.vec3(0,-90,0),
                TextureID="RobotAlternate",VertexArrayName="Bullet_"+str(Position),
                ID = self.GetID(Object.gid),
                ModuleAttachment = NPC(self,TextureID=self.GetID(Object.gid),X=Position[0],Z=Position[1])
                )


            self.NewAI = BehaviourAI(NPCObject,self.Width,self.Depth,self.WallMap,self.DoorMap)
            self.NPCMap[Position] = NPCObject
            self.NPCList.append(NPCObject)

        self.Engine.Player.WallMap = self.WallMap
        self.Engine.Player.DoorMap = self.DoorMap
        self.Engine.Player.ItemMap = self.ItemMap
        self.Engine.Player.NpcMap  = self.NPCMap
