from Settings import *

class VertexBuffer:
    def __init__(self,Application):
        self.VertexBuffers = {}
        self.Context = Application.Context

        self.VertexBuffers['MeshBrick'] = MeshBrick(self.Context)
        self.VertexBuffers['PartBrick'] = PartBrick(self.Context)
        self.VertexBuffers['Skybox'] = Skybox(self.Context)

    def MeshCreator(self,Context,Name,ID):
        self.VertexBuffers[Name] = MeshCreation(ID,Context)
        return self.VertexBuffers

    def Destroy(self):
        [VertexBuffer.Destroy() for VertexBuffer in self.VertexBuffers.values()]

class VertexBufferBase:
    def __init__(self,Context):
        self.Context = Context
        self.VertexBuffer = self.GetVertexBuffer()

        self.Format: str = None
        self.Attributes: list = None
        self.MeshID:str = None

    def GetVertexData(self):
        ...

    def GetVertexBuffer(self):
        VertexData = self.GetVertexData()
        VertexBuffer = self.Context.buffer(VertexData)
        return VertexBuffer
    
    def Destroy(self):
        self.VertexBuffer.release()


class MeshCreation:
    def __init__(self,ID,Context):
        self.Context = Context
        self.Format = '2f 3f 3f'
        self.Attributes = ['in_texcoord_0','in_normal','in_position']
        
        self.MeshID = ID
        self.VertexBuffer = self.GetVertexBuffer()

    def GetVertexBuffer(self):
        VertexData = self.GetVertexData()
        VertexBuffer = self.Context.buffer(VertexData)
        return VertexBuffer
    
    def SetData(self):
        ...
    
    def GetVertexData(self):
        NewObject = pywavefront.Wavefront(self.MeshID,cache=True,parse=True)
        NewObject = NewObject.materials.popitem()[1]
        VertexData = NewObject.vertices 
        VertexData = numpy.array(VertexData,dtype='f4')
        return VertexData

    def Destroy(self):
        self.VertexBuffer.release()


class MeshBrick(VertexBufferBase):
    def __init__(self,Application):
        super().__init__(Application)
        self.Format = '2f 3f 3f'
        self.Attributes = ['in_texcoord_0','in_normal','in_position']

    def GetVertexData(self):
        NewObject = pywavefront.Wavefront(f'Resources/Assets/Meshes/Baseplate.obj',cache=True,parse=True)
        NewObject = NewObject.materials.popitem()[1]
        VertexData = NewObject.vertices 
        VertexData = numpy.array(VertexData,dtype='f4')

        return VertexData
    
class PartBrick(VertexBufferBase):
    def __init__(self,Context):
        super().__init__(Context)
        self.Format = '2f 3f 3f'
        self.Attributes = ['in_texcoord_0','in_normal','in_position']

    @staticmethod
    def GetData(Vertices,Indices):
        Data = [Vertices[Index] for Triangle in Indices for Index in Triangle]
        return numpy.array(Data, dtype='f4')
    
    def GetVertexData(self):
        Vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        Indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        
        VertexData = self.GetData(Vertices,Indices)
        TextureVertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        TextureIndices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1),]
        TextureData = self.GetData(TextureVertices,TextureIndices)
        Normals = [( 0, 0, 1) * 6,
                   ( 1, 0, 0) * 6,
                   ( 0, 0,-1) * 6,
                   (-1, 0, 0) * 6,
                   ( 0, 1, 0) * 6,
                   ( 0,-1, 0) * 6,]
        Normals = numpy.array(Normals, dtype='f4').reshape(36, 3)
        VertexData = numpy.hstack([Normals, VertexData])
        VertexData = numpy.hstack([TextureData,VertexData])
        return VertexData


class Skybox(VertexBufferBase):
    def __init__(self,Context):
        super().__init__(Context)
        self.Format = '3f'
        self.Attributes = ['in_position']
    
    def GetVertexData(self):
        Z = 0.9999
        Vertices = [(-1,-1,Z), (3,-1,Z), (-1,3,Z)]
        VertexData = numpy.array(Vertices,dtype='f4')
        return VertexData