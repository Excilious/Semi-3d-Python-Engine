from Settings import *

class BehaviourAI:
    def __init__(self,Object,Width,Depth,WallMap,DoorMap):
        self.Object = Object
        self.Width = Width
        self.Depth = Depth
        self.WallMap = WallMap
        self.DoorMap = DoorMap

    def Movement(self):
        RandomPositionX,RandomPositionZ = random.randint(0,int(self.Width/5)), random.randint(0,int(self.Depth/5))
        for x in range(0,RandomPositionX):
            for z in range(0,RandomPositionZ):
                print(x,z)
                if (not self.DoesCollide(DeltaX=x)):
                    self.Object.Position += glm.vec3(x,0,0)
                if (not self.DoesCollide(DeltaZ=z)):
                    self.Object.Position += glm.vec3(0,0,z)

    def DoesCollide(self,DeltaX=0,DeltaZ=0):
        IntegerPosition = (
            int(self.Object.Position.x + DeltaX + (
                0.022 if DeltaX > 0 else -0.022 if DeltaX < 0 else 0)
                ),
            int(self.Object.Position.z + DeltaZ + (
                0.022 if DeltaZ > 0 else -0.022 if DeltaZ < 0 else 0)
                )
        )
        if (IntegerPosition in self.DoorMap):
            return self.DoorMap[IntegerPosition].IsClosed
        return IntegerPosition in self.WallMap