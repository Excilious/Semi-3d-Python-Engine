from Meshes.BaseMesh import *
from Settings import *

class QuadMesh:
    def __init__(self,Engine,Shader):
        self.Engine = Engine
        self.Context = Engine.Context
        self.Program = Shader

        self.VertexFormat = '4f 2f'
        self.VertexAttributes = ('in_position', 'in_uv')
        self.VertexArray = self.GetVertexArray()

    def GetVertexArray(self):
        VertexData = self.GetVertexData()
        VertexBuffer = self.Context.buffer(VertexData)
        VertexArray = self.Context.vertex_array(
            self.Program,
            [
                (VertexBuffer,self.VertexFormat,*self.VertexAttributes)
            ],
            skip_errors=True
        )
        return VertexArray

    def Render(self):
        self.VertexArray.render()

    def GetVertexData(self):
        VertexPosition = (
            [-0.5,0.0,0.0,1.0],[-0.5,1.0,0.0,1.0],
            [ 0.5,1.0,0.0,1.0],[0.5,0.0,0.0,1.0]
        )
        UVCoordinates = (
            [1,1],[1,0],[0,0],[0,1]
        )
        VerticesIndices = [
            0, 2, 1, 0, 3, 2
        ]

        VertexData = []
        for Vertices in VerticesIndices:
            VertexData += VertexPosition[Vertices]
            VertexData += UVCoordinates[Vertices]

        VertexData = numpy.array(VertexData, dtype='float32')
        return VertexData
