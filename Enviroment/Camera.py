from Settings import *

class Camera:
    def __init__(self,Position,RotateX,RotateZ):
        self.Position = glm.vec3(Position)
        self.RotateX = glm.radians(RotateX)
        self.RotateZ = glm.radians(RotateZ)

        self.UpPosition = glm.vec3(0,1,0)
        self.RightPosition = glm.vec3(1,0,0)
        self.ForwardPosition = glm.vec3(0,0,-1)

        self.MatrixProjection = glm.perspective(VERTICAL_FOV, ASPECT_RATIO, NEAR, FAR)
        self.MatrixView = glm.mat4()

    def Update(self):
        self.UpdateVectors()
        self.UpdateViewMatrix()

    def UpdateViewMatrix(self):
        self.MatrixView = glm.lookAt(self.Position, self.Position + self.ForwardPosition, self.UpPosition)

    def UpdateVectors(self):
        self.ForwardPosition.x = glm.cos(self.RotateX) * glm.cos(self.RotateZ)
        self.ForwardPosition.y = glm.sin(self.RotateZ)
        self.ForwardPosition.z = glm.sin(self.RotateX) * glm.cos(self.RotateZ)

        self.ForwardPosition = glm.normalize(self.ForwardPosition)
        self.RightPosition = glm.normalize(glm.cross(self.ForwardPosition, glm.vec3(0,1,0)))
        self.UpPosition = glm.normalize(glm.cross(self.RightPosition, self.ForwardPosition))

    def RotateZAxis(self,DeltaY):
        self.RotateZ -= DeltaY
        self.RotateZ = glm.clamp(self.RotateZ,-PITCH_MAX,PITCH_MAX)

    def RotateXAxis(self,DeltaX):
        self.RotateX += DeltaX

    def MoveLeft(self,Velocity):
        return -self.RightPosition.xz * Velocity

    def MoveRight(self,Velocity):
        return self.RightPosition.xz * Velocity

    def MoveUp(self,Velocity):
        self.Position += self.UpPosition * Velocity

    def MoveDown(self,Velocity):
        self.Position -= self.UpPosition * Velocity

    def MoveForward(self,Velocity):
        return self.ForwardPosition.xz * Velocity

    def MoveBack(self,Velocity):
        return -self.ForwardPosition.xz * Velocity
