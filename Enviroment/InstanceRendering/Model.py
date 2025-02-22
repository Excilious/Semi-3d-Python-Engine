from Settings import *
from Enviroment.InstanceRendering.VertexArrayObject import *
from Enviroment.InstanceRendering.VertexBufferObject import *

class Model:
    Array = None

    def __init__(self,Application,VertexArrayName,MeshID,TextureID=1,Position = PLAYER_POS,Rotation = glm.vec3(0,-90,0),Scale = glm.vec3(3,3,3),ID=None,ModuleAttachment=None):
        self.Application = Application
        self.VertexArrayName = VertexArrayName
        self.VertexArrayDude = None
        self.VertexArray = self.Application.Mesh.VertexArrayObject
        self.ID = ID
        self.Module = ModuleAttachment

        self.Position = Position
        self.Rotation = glm.vec3([glm.radians(Value) for Value in Rotation])
        self.Scale = Scale

        if (MeshID): self.SetMeshID(MeshID)

        self.MatrixModel = self.GetModelMatrix()
        self.TextureID = TextureID
        self.VertexArray = self.VertexArray.VertexArrays[VertexArrayName]
        self.NewVertexArray = None

        self.Program = self.VertexArray.program
        self.Camera = self.Application.Player

    def SetMeshID(self,MeshID):
        self.VertexBufferCreation = VertexBuffer(self.Application)
        self.VertexArray = self.Application.Mesh.VertexArrayObject
        Array = self.VertexArray.AddNewArray(self.VertexArrayName,'Default',MeshID)
        Model.Array = Array

    def Update(self):
        ...

    def GetModelMatrix(self):
        ModelMatrix = glm.mat4()

        ModelMatrix = glm.translate(ModelMatrix, self.Position)
        ModelMatrix = glm.rotate(ModelMatrix,self.Rotation.z, glm.vec3(0,0,1))
        ModelMatrix = glm.rotate(ModelMatrix,self.Rotation.y, glm.vec3(0,1,0))
        ModelMatrix = glm.rotate(ModelMatrix,self.Rotation.x, glm.vec3(1,0,0))

        ModelMatrix = glm.scale(ModelMatrix, self.Scale)
        return ModelMatrix
    
    def Render(self):
        self.Update()
        if (Model.Array): Model.Array[self.VertexArrayName].render()

class ModelConstructor(Model):
    def __init__(self,Application,VertexArrayName,MeshID,TextureID,Position,Rotation,Scale,ID,ModuleAttachment):
        super().__init__(Application,VertexArrayName,MeshID,TextureID,Position,Rotation,Scale,ID,ModuleAttachment)
        self.Start()

    def Update(self):
        self.Texture.use(location=0)
        self.Program['CameraPosition'].write(self.Camera.Position)
        self.Program['MatrixView'].write(self.Camera.MatrixView)
        self.Program['MatrixModel'].write(self.MatrixModel)

    def UpdateShadow(self):
        self.ShadowMapProgram['MatrixModel'].write(self.MatrixModel)

    def RenderShadows(self):
        self.UpdateShadow()
        self.ShadowMapArray.render()

    def Start(self):
        self.Program['MatrixViewLight'].write(self.Camera.ViewLightMatrix)
        self.Program['Resolution'].write(RESOLUTION)
        self.DepthTexture = self.Application.Mesh.Texture.TextureStorage['DepthTexture']
        self.Program['ShadowMap'] = 1
        self.DepthTexture.use(location=1)

        self.ShadowMapArray = self.Application.Mesh.VertexArrayObject.VertexArrays["Shadow_"+str(self.VertexArrayName)]
        self.ShadowMapProgram = self.ShadowMapArray.program
        self.ShadowMapProgram['MatrixProjection'].write(self.Camera.MatrixProjection)
        self.ShadowMapProgram['MatrixViewLight'].write(self.Application.Lighting.LightViewMatrix)
        self.ShadowMapProgram['MatrixModel'].write(self.MatrixModel)

        self.Texture = self.Application.Mesh.Texture.TextureStorage[self.TextureID]
        self.Program['Texture'] = 0
        self.Texture.use(location=0)

        self.Program['MatrixProjection'].write(self.Camera.MatrixProjection)
        self.Program['MatrixView'].write(self.Camera.MatrixView)
        self.Program['MatrixModel'].write(self.MatrixModel)

        self.Program['light.LightingPosition'].write(self.Application.Lighting.Position)
        self.Program['light.LightingAmbience'].write(self.Application.Lighting.LightingAmbience)
        self.Program['light.LightingDiffusion'].write(self.Application.Lighting.LightingDiffusion)
        self.Program['light.LightingSpecular'].write(self.Application.Lighting.LightSpecular)


class MeshBrickModel(ModelConstructor):
    def __init__(self,Application,WorldSpaceName,MeshID,VertexArrayName='MeshBrick',TextureID=1,Position=glm.vec3(0,0,0),Rotation=glm.vec3(-90,0,0),Scale=glm.vec3(1,1,1),ID=None,ModuleAttachment=None):
        assert WorldSpaceName,"WorldSpaceName would be needed to create the instance!"
        assert MeshID, "MeshID would be required to create a mesh!"
        super().__init__(Application,VertexArrayName,MeshID,TextureID,Position,Rotation,Scale,ID,ModuleAttachment)
        self.InstanceName = WorldSpaceName

    def Update(self):
        self.MatrixModel = self.GetModelMatrix()
        super().Update()

class PartBrickModel(ModelConstructor):
    def __init__(self,Application,WorldSpaceName,VertexArrayName='PartBrick',TextureID=0,Position=glm.vec3(0,0,0),Rotation=glm.vec3(-90,0,0),Scale=glm.vec3(1,1,1),ID=None):
        assert WorldSpaceName,"WorldSpaceName would be needed to create the instance!"
        super().__init__(Application,VertexArrayName,None,TextureID,Position,Rotation,Scale,ID)
        self.InstanceName = WorldSpaceName

    def Update(self):
        self.MatrixModel = self.GetModelMatrix()
        super().Update()