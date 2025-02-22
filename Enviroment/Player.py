from Settings import *
from Enviroment.Camera import *
from Enviroment.InstanceRendering.Model import *


class PlayerAttributes:
    def __init__(self):
        self.Health = PLAYER_INIT_HEALTH
        self.Ammo = PLAYER_INIT_AMMO
        self.Weapons = {ID.KNIFE_0: 1, ID.PISTOL_0: 0, ID.RIFLE_0: 0}
        self.EquippedWeapons = ID.KNIFE_0
        self.Level = 1

    def Update(self,Player):
        self.Health = Player.Health
        self.Ammo = Player.Ammo
        self.Weapons = Player.Weapons
        self.EquippedWeapons = Player.EquippedWeapons

class Player(Camera):
    def __init__(self,Engine,Position=PLAYER_POS,RotateX=0,RotateZ=0):
        self.Application = Engine.Application
        self.Engine = Engine
        self.Sound = Engine.Sound
        self.Play = Engine.Sound.Play
        super().__init__(Position,RotateX,RotateZ)

        self.DoorMap,self.WallMap,self.ItemMap,self.NpcMap = None, None, None, None
        self.Health = self.Engine.PlayerAttributes.Health
        self.Ammo = self.Engine.PlayerAttributes.Ammo
        self.TilePosition: tuple[int, int] = None

        self.Weapons = self.Engine.PlayerAttributes.Weapons
        self.EquippedWeapons = self.Engine.PlayerAttributes.EquippedWeapons
        self.WeaponCycle = cycle(self.Engine.PlayerAttributes.Weapons.keys())

        self.IsShot = False
        self.Key = None
        self.Object = {}

        self.Colour = LIGHT_COLOUR
        self.Direction = LIGHT_DIRECTION
        self.LightingAmbience = LIGHT_AMBIENCE * self.Colour
        self.LightingDiffusion = LIGHT_DIFFUSION * self.Colour
        self.LightingSpecular = LIGHT_SPECULAR * self.Colour

        self.ViewLightMatrix = self.GetViewLightMatrix()
        self.CameraTime = 0

    def GenerateWeapons(self):
        self.Object[ID.KNIFE_0] = MeshBrickModel(self.Engine,"UserKnife",MeshID="Resources/Assets/Meshes/New.obj",
            TextureID="Gun",Position=glm.vec3(0,0,0),Scale=glm.vec3(0.1,0.1,0.1),
            Rotation=glm.vec3(0,0,0))

    def Backpack(self):
        if (self.Object[self.EquippedWeapons]):
            self.Object[self.EquippedWeapons].Position = glm.vec3(self.RightPosition.x,self.UpPosition.y,self.ForwardPosition.z)
            self.Object[self.EquippedWeapons].Render()

    def GetViewLightMatrix(self):
        return glm.lookAt(self.Position, glm.vec3(0,0,0), glm.vec3(0,1,0))

    def Events(self,Event):
        if (Event.type == pygame.KEYDOWN):
            if Event.key == KEYS['INTERACT']:
                self.InteractWithDoor()

            if Event.key == KEYS['WEAPON_1']:
                self.SwitchWeapons(WeaponID=ID.KNIFE_0)
            elif Event.key == KEYS['WEAPON_2']:
                self.SwitchWeapons(WeaponID=ID.PISTOL_0)
            elif Event.key == KEYS['WEAPON_3']:
                self.SwitchWeapons(WeaponID=ID.RIFLE_0)

        if Event.type == pygame.MOUSEWHEEL:
            WeaponID = next(self.WeaponCycle)
            if self.Weapons[WeaponID]:
                self.SwitchWeapons(WeaponID=WeaponID)

        if Event.type == pygame.MOUSEBUTTONDOWN:
            if Event.button == 1:
                self.DoShot()

    def Update(self):
        super().Update()
        self.CheckHealth()
        self.UpdateTilePosition()
        self.PickUpItem()
        self.MouseControl()
        self.KeyboardControl()

    def CheckHealth(self):
        if self.Health <= 0:
            self.Play(self.Sound.PlayerDeath)
            pygame.time.wait(2000)
            self.Engine.PlayerAttributes = PlayerAttributes()
            self.Engine.NewGame()

    def CheckHitOnNPC(self):
        if WEAPON_SETTINGS[self.EquippedWeapons]['miss_probability'] > random.random(): return None
        if NPCPosition := self.Engine.Raycasting.Run(
                StartPosition=self.Position,
                Direction=self.ForwardPosition,
                MaxDistance=WEAPON_SETTINGS[self.EquippedWeapons]['max_dist'],
                NpcToPlayerFlag=False
        ):
            Npc = self.Engine.LevelMap.NPCMap[NPCPosition]
            Npc.Module.GetDamage()

    def SwitchWeapons(self,WeaponID):
        if self.Weapons[WeaponID]:
            self.WeaponInstance.WeaponID = self.EquippedWeapons = WeaponID

    def DoShot(self):
        if self.EquippedWeapons == ID.KNIFE_0:
            self.IsShot = True
            self.CheckHitOnNPC()
            self.Play(self.Sound.PlayerAttack[ID.KNIFE_0])
        elif self.Ammo:
            Consumption = WEAPON_SETTINGS[self.EquippedWeapons]['ammo_consumption']
            if (not self.IsShot and self.Ammo >= Consumption):
                self.IsShot = True
                self.CheckHitOnNPC()
                self.Ammo -= Consumption
                self.Ammo = max(0, self.Ammo)
                self.Play(self.Sound.PlayerAttack[self.EquippedWeapons])

    def UpdateTilePosition(self):
        self.TilePosition = int(self.Position.x), int(self.Position.z)

    def PickUpItem(self):
        if self.TilePosition not in self.ItemMap: return None
        Item = self.ItemMap[self.TilePosition]
    
        if (Item.ID == ID.MED_KIT):
            self.Health += ITEM_SETTINGS[ID.MED_KIT]['value']
            self.Health = min(self.Health, MAX_HEALTH_VALUE)
        elif (Item.ID == ID.AMMO):
            self.Ammo += ITEM_SETTINGS[ID.AMMO]['value']
            self.Ammo = min(self.Ammo, MAX_AMMO_VALUE)
        elif (Item.ID == ID.PISTOL_ICON):
            if (not self.Weapons[ID.PISTOL_0]):
                self.Weapons[ID.PISTOL_0] = 1
                self.SwitchWeapons(WeaponID=ID.PISTOL_0)
        elif (Item.ID == ID.RIFLE_ICON):
            if (not self.Weapons[ID.RIFLE_0]):
                self.Weapons[ID.RIFLE_0] = 1
                self.SwitchWeapons(WeaponID=ID.RIFLE_0)
        elif (Item.ID == ID.KEY):
            self.Key = 1
        self.Play(self.Sound.PickUp[Item.ID])
        del self.ItemMap[self.TilePosition]

    def InteractWithDoor(self):
        Position = self.Position + self.ForwardPosition
        IntegerPosition = int(Position.x), int(Position.z)

        if IntegerPosition not in self.DoorMap: return None
        Door = self.DoorMap[IntegerPosition]

        if (self.Key and Door.TextureID == ID.KEY_DOOR):
            Door.IsClosed = not Door.IsClosed
            self.Play(self.Sound.PlayerMissed)
            pygame.time.wait(300)
            self.Engine.PlayerAttributes.Update(Player=self)
            self.Engine.PlayerAttributes.Level += 1
            self.Engine.PlayerAttributes.Level %= LEVELS
            self.Engine.NewGame()
        else:
            Door.IsMoving = True
            self.Play(self.Sound.OpenDoor)

    def MouseControl(self):
        MouseDX,MouseDY = pygame.mouse.get_rel()
        if MouseDX:
            self.RotateXAxis(DeltaX=MouseDX * MOUSE_SENSITIVITY)
        if MouseDY:
            self.RotateZAxis(DeltaY=MouseDY * MOUSE_SENSITIVITY)

    def KeyboardControl(self):
        KeyState = pygame.key.get_pressed()
        Velocity = PLAYER_SPEED * self.Application.DeltaTime
        NextStep = glm.vec2()

        if KeyState[KEYS['FORWARD']]:
            NextStep += self.MoveForward(Velocity=Velocity)
        if KeyState[KEYS['BACK']]:
            NextStep += self.MoveBack(Velocity=Velocity)
        if KeyState[KEYS['STRAFE_R']]:
            NextStep += self.MoveRight(Velocity=Velocity)
        if KeyState[KEYS['STRAFE_L']]:
            NextStep += self.MoveLeft(Velocity=Velocity)

        self.Move(NextStep=NextStep)

    def Move(self,NextStep):
        if (not self.IsCollide(DeltaX=NextStep[0])):
            self.Position.x += NextStep[0] 
        if (not self.IsCollide(DeltaZ=NextStep[1])):
            self.Position.z += NextStep[1]
        if (NextStep[0] or NextStep[1]):
            self.Position.y += glm.sin(self.Engine.Application.Time * 12) / 300

    def IsCollide(self,DeltaX=0,DeltaZ=0):
        IntegerPosition = (
            int(self.Position.x + DeltaX + (
                PLAYER_SIZE if DeltaX > 0 else -PLAYER_SIZE if DeltaX < 0 else 0)
                ),
            int(self.Position.z + DeltaZ + (
                PLAYER_SIZE if DeltaZ > 0 else -PLAYER_SIZE if DeltaZ < 0 else 0)
                )
        )

        if (IntegerPosition in self.DoorMap):
            return self.DoorMap[IntegerPosition].IsClosed
        return IntegerPosition in self.WallMap
