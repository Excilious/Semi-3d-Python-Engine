from Settings import *
from Instances.GameObject import *
from Meshes.QuadMesh import *

class InstancedQuadMesh:
    def __init__(self,Engine,Objects: Iterable[GameObject],ShaderProgram:moderngl.Program):
        self.Context = Engine.Application.Context
        self.Program = ShaderProgram
        self.Objects = Objects
        self.Instances = len(Objects)

        self.QuadVertexBuffer = self.Context.buffer(QuadMesh.GetVertexData(self))
        self.MatrixModelBuffer: moderngl.Buffer = None
        self.TextureIDBuffer: moderngl.Buffer = None
        self.VertexArray = self.GetVertexArray() if self.Instances else None

    def UpdateBuffers(self):
        MatrixModelList,TextureIDList = [], []

        for Object in self.Objects:
            MatrixModelList += sum(Object.MatrixModel.to_list(), [])
            TextureIDList += [Object.TextureID]

        self.MatrixModelBuffer = self.Context.buffer(numpy.array(MatrixModelList, dtype='float32'))
        self.TextureIDBuffer = self.Context.buffer(numpy.array(TextureIDList, dtype='int32'))

    def GetVertexArray(self):
        self.UpdateBuffers()
        VertexArrayObject = self.Context.vertex_array(
            self.Program,
            [
                (self.QuadVertexBuffer, '4f 2f /v', 'in_position', 'in_uv'),
                (self.MatrixModelBuffer, '16f /i', 'm_model',),
                (self.TextureIDBuffer, '1i /i', 'in_tex_id'),
            ],
            skip_errors=True
        )
        return VertexArrayObject

    def Render(self):
        if len(self.Objects):
            self.VertexArrayObject = self.GetVertexArray()
            self.VertexArrayObject.render(instances=self.Instances)
