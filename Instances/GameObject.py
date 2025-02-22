from Settings import *

class GameObject:
    def __init__(self,LevelMap,TextureID,X,Z):
        self.Engine = LevelMap.Engine
        self.Application = self.Engine.Application
        self.TextureID = TextureID
        self.Position = glm.vec3(X+HORIZONTAL_WALL_SIZE,0,Z+HORIZONTAL_WALL_SIZE)
        self.Rotation = 0
        self.Scale = glm.vec3(1)
        self.MatrixModel: glm.mat4 = None

    def GetModelMatrix(self):
        MatrixModel = glm.translate(glm.mat4(),self.Position)
        MatrixModel = glm.rotate(MatrixModel,self.Rotation,glm.vec3(0, 1, 0))
        MatrixModel = glm.scale(MatrixModel,self.Scale)
        return MatrixModel

