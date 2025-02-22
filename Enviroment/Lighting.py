from Settings import *

class PointLight:
    def __init__(self,Position=LIGHT_POSITION,Colour=LIGHT_COLOUR):
        self.Position = Position
        self.Colour = Colour
        self.Direction = LIGHT_DIRECTION

        self.LightingAmbience = LIGHT_AMBIENCE * self.Colour
        self.LightingDiffusion = LIGHT_DIFFUSION * self.Colour
        self.LightSpecular = LIGHT_SPECULAR * self.Colour

        self.LightViewMatrix = self.GetLightViewMatrix()

    def GetLightViewMatrix(self):
        return glm.lookAt(self.Position, self.Direction, glm.vec3(0,1,0))
    