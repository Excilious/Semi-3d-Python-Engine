from Instances.GameObject import *
from Meshes.QuadMesh import *
from Settings import *

class Weapon:
    def __init__(self,Engine):
        self.Engine = Engine
        self.Application = Engine.Application

        self.Player = self.Engine.Player
        self.EquippedWeapon = self.Player.EquippedWeapons
        self.Player.WeaponInstance = self
        
        self.Position = WEAPON_POS
        self.Rotation = 0
        self.Scale = glm.vec3(WEAPON_SCALE / ASPECT_RATIO, WEAPON_SCALE, 0)
        self.MatrixModel = GameObject.GetModelMatrix(self)
        
        self.Frame = 0
        self.AnimationCounter = 0

    def Update(self):
        if self.Player.IsShot and self.Application.AnimationTrigger:
            self.AnimationCounter += 1

            if self.AnimationCounter == WEAPON_ANIM_PERIODS:
                self.AnimationCounter = 0
                self.Frame += 1

                if self.Frame == WEAPON_NUM_FRAMES:
                    self.Frame = 0
                    self.Player.IsShot = False

    def Render(self):
        self.SetUniform()
        self.Mesh.Render()
