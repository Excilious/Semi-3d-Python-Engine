from Enviroment.InstanceRendering.VertexBufferObject import *
from Enviroment.Shader import *

class VertexArray:
    def __init__(self,Application,NewVertexBuffer=None):
        if (not NewVertexBuffer): NewVertexBuffer = VertexBuffer(Application)

        self.Context = Application.Context
        self.VertexBuffer = VertexBuffer(Application)
        self.Programs = ShaderProgram(Application)

        self.VertexArrays = {}

        self.VertexArrays['MeshBrick'] = self.GetVertexArray(
            Program = self.Programs.Default,
            VertexBuffer = self.VertexBuffer.VertexBuffers['MeshBrick'],
        )
        self.VertexArrays['PartBrick'] = self.GetVertexArray(
            Program = self.Programs.Default,
            VertexBuffer = self.VertexBuffer.VertexBuffers['PartBrick'],
        )


    def AddNewArray(self,InstanceName,Shader,MeshID):
        self.VertexBuffer.VertexBuffers = self.VertexBuffer.MeshCreator(self.Context,InstanceName,MeshID)
        self.VertexArrays[InstanceName] = self.GetVertexArray(
                Program = self.Programs.Default,
                VertexBuffer = self.VertexBuffer.VertexBuffers[InstanceName],
            )
        self.VertexArrays["Shadow_"+str(InstanceName)] = self.GetVertexArray(
            Program = self.Programs.Shadow,
            VertexBuffer = self.VertexBuffer.VertexBuffers[InstanceName]
        )
        return self.VertexArrays
        
    def GetVertexArray(self,Program,VertexBuffer):
        VertexArrayObject = self.Context.vertex_array(Program,[
            (VertexBuffer.VertexBuffer, VertexBuffer.Format, *VertexBuffer.Attributes)
        ],
        skip_errors=True)
        return VertexArrayObject
    
    def Destroy(self):
        self.VertexBuffer.Destroy()
        self.Programs.Destroy()