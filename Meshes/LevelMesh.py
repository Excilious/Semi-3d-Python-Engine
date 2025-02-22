from Meshes.LevelMeshBuilder import *

class LevelMesh:
    def __init__(self,Engine):
        self.Engine = Engine
        self.Context = self.Engine.Context
        self.Program = self.Engine.Shader.Level

        self.VertexFormat = '3u2 1u2 1u2 1u2 1u2'
        self.FormatSize = sum(int(Format[:1]) for Format in self.VertexFormat.split())
        self.VertexAttributes = ('in_position', 'in_tex_id', 'face_id', 'ao_id', 'flip_id')

        self.MeshBuilder = LevelBuilder(self)
        self.VertexArray = self.GetVertexArray()

    def GetVertexArray(self):
        VertexData = self.GetVertexData()
        VertexBuffer = self.Context.buffer(VertexData)
        VertexArray = self.Context.vertex_array(
            self.Program,
            [
                (VertexBuffer, self.VertexFormat, *self.VertexAttributes)
            ],
            skip_errors=True
        )
        return VertexArray

    def Render(self):
        self.VertexArray.render()

    def GetVertexData(self):
        VertexData = self.MeshBuilder.BuildMesh()
        print('Vertices: ', len(VertexData) // 7 * 3)
        return VertexData
