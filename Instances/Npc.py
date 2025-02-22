from Settings import *
from Instances.GameObject import *
from Enviroment.InstanceRendering.Model import *

class NPC(GameObject):
    def __init__(self,LevelMap,TextureID,X,Z):
        super().__init__(LevelMap,TextureID,X,Z)
        self.LevelMap = LevelMap
        self.Player = self.Engine.Player
        self.NPCID = TextureID
        
        self.Scale = NPC_SETTINGS[self.NPCID]['scale']
        self.Speed = NPC_SETTINGS[self.NPCID]['speed']
        self.Size = NPC_SETTINGS[self.NPCID]['size']
        self.AttackDistance = NPC_SETTINGS[self.NPCID]['attack_dist']
        self.Health = NPC_SETTINGS[self.NPCID]['health']
        self.Damage = NPC_SETTINGS[self.NPCID]['damage']
        self.HitProbability = NPC_SETTINGS[self.NPCID]['hit_probability']
        self.DropItem = NPC_SETTINGS[self.NPCID]['drop_item']
        
        self.AnimationPeriods = NPC_SETTINGS[self.NPCID]['anim_periods']
        self.AnimationCounter = 0
        self.Frame = 0
        self.IsAnimate = True
        
        self.NumberFrames, self.StateTextureID = None, None
        self.SetState(State='walk')
        
        self.TilePosition: tuple[int, int] = None
        
        self.IsPlayerSpotted: bool = False
        self.PathToPlayer: tuple[int, int] = None
        
        self.IsAlive = True
        self.IsHurt = False
        
        self.Play = self.Engine.Sound.Play
        self.Sound = self.Engine.Sound
        
        self.MatrixModel = self.GetModelMatrix()
        self.UpdateTilePosition()

    def Update(self):
        if self.IsHurt: 
            self.SetState(State='hurt')
        elif self.Health > 0:
            self.UpdateTilePosition()
            self.RaycastToPlayer()
            self.GetPathToPlayer()
            if not self.Attack():
                self.MoveToPlayer()
        else:
            self.IsAlive = False
            self.SetState('death')
        
        self.Animate()
        self.TextureID = self.StateTextureID + self.Frame

    def GetDamage(self):
        self.Health -= WEAPON_SETTINGS[self.Player.EquippedWeapons]['damage']
        self.IsHurt = True

        if not self.IsPlayerSpotted: 
            self.IsPlayerSpotted = True

    def Attack(self):
        if not self.IsPlayerSpotted: return False
        if glm.length(self.Player.Position.xz - self.Position.xz) > self.AttackDistance:
            return False

        DirectionToPlayer = glm.normalize(self.Player.Position - self.Position)
        
        if self.Engine.Raycasting.Run(StartPosition=self.Position,Direction=DirectionToPlayer):
            self.SetState(State='attack')

            if self.Application.SoundTrigger:
                self.Play(self.Sound.EnemyAttack[self.NPCID])

            if random.random() < self.HitProbability:
                self.Player.Health -= self.Damage
                self.Play(self.Sound.PlayerHurt)
            return True

    def GetPathToPlayer(self):
        if not self.IsPlayerSpotted: return None
        
        self.PathToPlayer = self.Engine.PathFinding.Find(
            StartPosition=self.TilePosition,
            EndPosition=self.Player.TilePosition
        )

    def MoveToPlayer(self):
        if not self.PathToPlayer:
            return None

        self.SetState(State='walk')
        DirectionVector = glm.normalize(glm.vec2(self.PathToPlayer) + HORIZONTAL_WALL_SIZE - self.Position.xz)
        DeltaVector = DirectionVector * self.Speed * self.Application.DeltaTime

        if not self.IsCollide(DeltaX=DeltaVector[0]):
            self.Position.x += DeltaVector[0]
        if not self.IsCollide(DeltaZ=DeltaVector[1]):
            self.Position.z += DeltaVector[1]

        DoorMap = self.LevelMap.DoorMap
        if self.TilePosition in DoorMap:
            Door = DoorMap[self.TilePosition]
            if Door.IsClosed and not Door.IsMoving:
                Door.IsMoving = True
                self.Play(self.Sound.OpenDoor)

        self.MatrixModel = self.GetModelMatrix()

    def IsCollide(self,DeltaX=0,DeltaZ=0):
        IntegerPosition = (
            int(self.Position.x + DeltaX + (self.Size if DeltaX > 0 else -self.Size if DeltaX < 0 else 0)),
            int(self.Position.z + DeltaZ + (self.Size if DeltaZ > 0 else -self.Size if DeltaZ < 0 else 0))
        )
        return (IntegerPosition in self.LevelMap.WallMap or
                IntegerPosition in (self.LevelMap.NPCMap.keys() - {self.TilePosition}))

    def UpdateTilePosition(self):
        self.TilePosition = int(self.Position.x), int(self.Position.z)

    def RaycastToPlayer(self):
        if not self.IsPlayerSpotted:
            return None

        DirectionToPlayer = glm.normalize(self.Player.Position - self.Position)
        if self.Engine.Raycasting.Run(StartPosition=self.Position,Direction=DirectionToPlayer):
            self.IsPlayerSpotted = True
            self.Play(self.Sound.Spotted[self.NPCID])

    def SetState(self,State):
        self.NumberFrames = NPC_SETTINGS[self.NPCID]['num_frames'][State]
        self.StateTextureID = NPC_SETTINGS[self.NPCID]['state_tex_id'][State]
        self.Frame %= self.NumberFrames

    def Animate(self):
        if not (self.IsAnimate and self.Application.AnimationTrigger): return None
        self.AnimationCounter += 1
        if self.AnimationCounter == self.AnimationPeriods:
            self.AnimationCounter = 0
            self.Frame = (self.Frame + 1) % self.NumberFrames
            if self.IsHurt:
                self.IsHurt = False
            elif not self.IsAlive and self.Frame == self.NumberFrames - 1:
                self.IsAnimate = False
                self.ToDropItem()
                self.Play(self.Engine.Sound.Death[self.NPCID])

    def ToDropItem(self):
        if self.DropItem is not None:
            self.LevelMap.ItemMap[self.TilePosition] = MeshBrickModel(
                self.Engine,
                WorldSpaceName="Bullet_"+str(self.TilePosition),
                MeshID=self.ResourceItems[self.GetID(self.DropItem.gid)]["MeshID"],
                Position=glm.vec3(self.TilePosition[0],-0.15,self.TilePosition[1]),
                Scale=glm.vec3(0.15,0.15,0.15),Rotation=glm.vec3(0,-90,0),
                TextureID=self.ResourceItems[self.GetID(self.DropItem.gid)]["TextureID"],VertexArrayName="Bullet_"+str(self.TilePosition),
                ID = self.GetID(self.DropItem.gid)
                )
    