from Settings import *

class BaseMesh:
    def __init__(self):
        self.Context = None
        self.Program = None
        self.VertexBufferFormat = None
        self.Attributes: tuple[str, ...] = None
        self.VertexArray = None

    def GetVertexData(self) -> numpy.array: ...

    def GetVertexArray(self):
        VertexArray = self.GetVertexData()
        VertexBuffer = self.Context.buffer(VertexArray)
        VertexArray = self.Context.vertex_array(
            self.Program, [(VertexBuffer, self.VertexBufferFormat, *self.Attributes)], skip_errors=True
        )
        return VertexArray

    def Render(self):
        self.VertexArray.render()
