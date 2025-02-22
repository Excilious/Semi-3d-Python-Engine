from Settings import *
from Meshes.InstancedQuadMesh import *

class ParticleBuilder:
    def __init__(self,TextureID,X,Z,Rotation=0):
        self.MatrixModel = self.GetModelMatrix()
        self.Position = glm.vec3(X+HORIZONTAL_WALL_SIZE,0,Z+HORIZONTAL_WALL_SIZE)
        self.Scale = glm.vec3(1)
        self.TextureID
        self.Rotation = Rotation

    def GetModelMatrix(self):
        ModelMatrix = glm.translate(glm.mat4(), self.Position)
        ModelMatrix = glm.rotate(ModelMatrix, self.Rotation, glm.vec3(0,1,0))
        ModelMatrix = glm.scale(ModelMatrix,self.Scale)

class Particle:
    ParticleModules = {}
    def __init__(self,Engine,Name): 
        Particle.ParticleModules[Name] = InstancedQuadMesh(
            Engine,
        )
