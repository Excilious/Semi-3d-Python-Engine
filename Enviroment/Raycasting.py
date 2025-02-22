from Settings import *

class RayCasting:
    def __init__(self, Engine):
        self.Engine = Engine
        self.LevelMap = Engine.LevelMap
        self.WallMap = Engine.LevelMap.WallMap
        self.DoorMap = Engine.LevelMap.DoorMap
        self.Player = Engine.Player

    @staticmethod
    def GetData(Position1,Position2):
        LastDelta = glm.sign(Position2 - Position1)
        Delta = min(LastDelta / (Position2 - Position1), 10000000.0) if LastDelta != 0 else 10000000.0
        MaxDelta = Delta * (1.0 - glm.fract(Position1)) if LastDelta > 0 else Delta * glm.fract(Position1)
        return LastDelta,Delta,MaxDelta

    def Run(self,StartPosition,Direction,MaxDistance=RAYCAST_DISTANCE,NpcToPlayerFlag=True):
        X1,Y1,Z1 = StartPosition
        X2,Y2,Z2 = StartPosition + Direction * MaxDistance 
        VoxelPosition = glm.ivec3(X1,Y1,Z1)

        Dx,DeltaX,MaxX = self.GetData(X1,X2)
        Dy,DeltaY,MaxY = self.GetData(Y1,Y2)
        Dz,DeltaZ,MaxZ = self.GetData(Z1,Z2)

        while (not (MaxX > 1.0 and MaxY > 1.0 and MaxZ > 1.0)):
            TilePosition = (VoxelPosition.x,VoxelPosition.z)
            if (TilePosition in self.WallMap): return False

            if (TilePosition in self.DoorMap):
                if self.DoorMap[TilePosition].IsClosed: return False

            if NpcToPlayerFlag:
                if (self.Player.TilePosition == VoxelPosition): return True
            
            elif TilePosition in self.LevelMap.NPCMap: return TilePosition
            
            if (MaxX < MaxY):
                if (MaxX < MaxZ):
                    VoxelPosition.x += Dx
                    MaxX += DeltaX
                else:
                    VoxelPosition.z += Dz
                    MaxZ += DeltaZ
            else:
                if (MaxY < MaxZ):
                    VoxelPosition.y += Dy
                    MaxY += DeltaY
                else:
                    VoxelPosition.z += Dz
                    MaxZ += DeltaZ
        return False
