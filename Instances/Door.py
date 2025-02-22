from Settings import *
from Instances.GameObject import *

class Door(GameObject):
    def __init__(self,LevelMap,TextureID,X,Z):
        super().__init__(LevelMap,TextureID,X,Z)
        self.LevelMap = LevelMap
        self.Rotation = self.GetRotation(X,Z)
        self.MatrixModel = self.GetModelMatrix()
        self.IsClosed = True
        self.IsMoving = False

    def Update(self):
        if not self.IsMoving: return None

        if (self.IsClosed and self.Position.y < WALL_SIZE - ANIMATION_DOOR_SPEED):
            if self.Application.AnimationTrigger:
                self.Position.y += ANIMATION_DOOR_SPEED
                self.MatrixModel = self.GetModelMatrix()

        elif (not self.IsClosed and self.Position.y > 0):
            if self.Application.AnimationTrigger:
                self.Position.y -= ANIMATION_DOOR_SPEED
                self.MatrixModel = self.GetModelMatrix()
        else:
            self.IsMoving = False
            self.IsClosed = not self.IsClosed

    def GetRotation(self,X,Z):
        WallMap = self.LevelMap.WallMap
        if ((X,Z-1) in WallMap and (X,Z+1) in WallMap):
            return glm.half_pi()
        return 0
