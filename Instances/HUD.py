from Meshes.QuadMesh import *
from Instances.GameObject import *
from Settings import *


class HUDObject:
    def __init__(self,Hud,TextureID):
        self.TextureID = TextureID
        self.Position = glm.vec3(HUD_SETTINGS[TextureID]['pos'], 0)
        self.Rotation = 0
        Hud.Objects.append(self)
        Scale = HUD_SETTINGS[TextureID]['scale']
        self.Scale = glm.vec3(Scale/ASPECT_RATIO,Scale,0)
        self.MatrixModel = GameObject.GetModelMatrix(self)

class HUD:
    def __init__(self,Engine):
        self.Engine = Engine
        self.Application = Engine.Application
        self.Objects = []

        self.Health = HUDObject(self, ID.MED_KIT)
        self.Ammo = HUDObject(self, ID.AMMO)
        self.Fps = HUDObject(self, ID.FPS)
        
        self.AmmoDigit0 = HUDObject(self, ID.AMMO_DIGIT_0)
        self.AmmoDigit1 = HUDObject(self, ID.AMMO_DIGIT_1)
        self.AmmoDigit2 = HUDObject(self, ID.AMMO_DIGIT_2)
        
        self.HealthDigit0 = HUDObject(self, ID.HEALTH_DIGIT_0)
        self.HealthDigit1 = HUDObject(self, ID.HEALTH_DIGIT_1)
        self.HealthDigit2 = HUDObject(self, ID.HEALTH_DIGIT_2)
        
        self.FpsDigit0 = HUDObject(self, ID.FPS_DIGIT_0)
        self.FpsDigit1 = HUDObject(self, ID.FPS_DIGIT_1)
        self.FpsDigit2 = HUDObject(self, ID.FPS_DIGIT_2)
        
        self.Digits = [0, 0, 0]

    def UpdateDigit(self,Value):
        MinValue = min(Value,999)
        self.Digits[2] = MinValue % 10
        
        MinValue //= 10
        self.Digits[1] = MinValue % 10
        
        MinValue //= 10
        self.Digits[0] = MinValue % 10

    def Update(self):
        self.UpdateDigit(self.Engine.Player.Ammo)
        self.AmmoDigit0.TextureID = self.Digits[0] + ID.DIGIT_0
        self.AmmoDigit1.TextureID = self.Digits[1] + ID.DIGIT_0
        self.AmmoDigit2.TextureID = self.Digits[2] + ID.DIGIT_0

        self.UpdateDigit(self.Engine.Player.Health)
        self.HealthDigit0.TextureID = self.Digits[0] + ID.DIGIT_0
        self.HealthDigit1.TextureID = self.Digits[1] + ID.DIGIT_0
        self.HealthDigit2.TextureID = self.Digits[2] + ID.DIGIT_0

        self.UpdateDigit(self.Engine.Application.FramesPerSecond)
        self.FpsDigit0.TextureID = self.Digits[0] + ID.DIGIT_0
        self.FpsDigit1.TextureID = self.Digits[1] + ID.DIGIT_0
        self.FpsDigit2.TextureID = self.Digits[2] + ID.DIGIT_0
