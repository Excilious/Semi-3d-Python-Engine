from Enviroment.Textures import *
from Enviroment.InstanceRendering.VertexArrayObject import *
from Enviroment.InstanceRendering.VertexBufferObject import *

class Mesh:
    def __init__(self,Application):
        self.Application = Application
        self.VertexBufferObject = VertexBuffer(Application)
        self.VertexArrayObject = VertexArray(Application)
        self.Texture = Textures(Application)

    def Destroy(self):
        self.VertexArrayObject.Destroy()
        self.Texture.Destroy()