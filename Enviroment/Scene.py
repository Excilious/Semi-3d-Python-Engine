from Meshes.LevelMesh import *
from Meshes.InstancedQuadMesh import *
from Instances.HUD import *
from Instances.Weapon import *
from Enviroment.InstanceRendering.Model import *

class Scene:
    SceneObjects = {}

    def __init__(self,Engine):
        self.Engine = Engine
        self.LevelMesh = LevelMesh(Engine)

        self.Hud = HUD(Engine)
        self.Doors = self.Engine.LevelMap.DoorMap.values()
        self.Items = self.Engine.LevelMap.ItemMap.values()
        self.Npc = self.Engine.LevelMap.NPCMap.values()
        self.Weapon = Weapon(Engine)

        self.InstanceDoorMesh = InstancedQuadMesh(
            Engine,self.Doors,Engine.Shader.InstancedDoor
        )
        self.InstancedHudMesh = InstancedQuadMesh(
            Engine,self.Hud.Objects,Engine.Shader.InstancedHud
        )
        self.Engine.Player.GenerateWeapons()

    def LoadEnviromentScene(self):
        Scene.SceneObjects["ControlPanel"] = MeshBrickModel(self.Engine,
            WorldSpaceName="ControlPanel",MeshID='Resources/Assets/Meshes/ControlPanel.obj',
            TextureID="ControlPanel",Position=glm.vec3(1.5,0,1.5),Rotation=glm.vec3(0,0,0),
            Scale=glm.vec3(0.05,0.05,0.05))
        
 
    def Update(self):
        for Door in self.Doors:
            Door.Update()
        self.Hud.Update()
        self.Weapon.Update()

    def Render(self):
        self.LevelMesh.Render()
        self.InstanceDoorMesh.Render()

        for Instance in Scene.SceneObjects.values():
            Instance.Render()

        for Instance in self.Npc:
            Instance.RenderShadows()
            Instance.Render()

        for Instance in self.Items:
            Instance.RenderShadows()
            Instance.Render()
        self.Engine.Player.Backpack()