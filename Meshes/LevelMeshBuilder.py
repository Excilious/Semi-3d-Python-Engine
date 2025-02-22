from Settings import *

class LevelBuilder:
    def __init__(self,Mesh):
        self.Mesh = Mesh
        self.Map = Mesh.Engine.LevelMap

    def IsBlocked(self,X,Z):
        if (not (0 <= X < self.Map.Width and 0 <= Z < self.Map.Depth)):
            return True
        return (X,Z) in self.Map.WallMap
    
    def AddData(self,VertexData,Index,*Vertices):
        for Vertex in Vertices:
            for Attributes in Vertex:
                VertexData[Index] = Attributes
                Index += 1
        return Index

    def GetArrayObject(self,X,Z,Plane):
        if (Plane == 'Y'):
            A = not self.IsBlocked(X,Z-1)
            B = not self.IsBlocked(X-1,Z-1)
            C = not self.IsBlocked(X-1,Z)
            D = not self.IsBlocked(X-1,Z+1)
            E = not self.IsBlocked(X,Z+1)
            F = not self.IsBlocked(X+1,Z+1)
            G = not self.IsBlocked(X+1,Z)
            H = not self.IsBlocked(X+1,Z-1)
        
        elif (Plane == 'X'):
            A = not self.IsBlocked(X,Z-1)
            B,C,D = 0,0,0
            E = not self.IsBlocked(X,Z+1)
            F,G,H = 0,0,0

        else:
            A = not self.IsBlocked(X-1,Z)
            B,C,D = 0,0,0
            E = not self.IsBlocked(X+1,Z)
            F,G,H = 0,0,0

        ArrayObject = (A+B+C), (G+H+A), (E+F+G), (C+D+E)
        return ArrayObject

    def BuildMesh(self):
        VertexData = numpy.empty(
            [self.Map.Width * self.Map.Depth * self.Mesh.FormatSize * 18], dtype='uint16'
        )
        Index = 0

        for X in range(self.Map.Width):
            for Z in range(self.Map.Depth):
                if (PositionNotInWallMap := (X,Z) not in self.Map.WallMap):
                    ArrayObject = self.GetArrayObject(X,Z,Plane='Y')
                    FlipID = ArrayObject[1] + ArrayObject[3] > ArrayObject[0] + ArrayObject[2]

                    if ((X,Z) in self.Map.FloorMap):
                        TextureID = self.Map.FloorMap[(X,Z)]
                        FaceID = 0 

                        Vertex0 = (X,0,Z,TextureID,FaceID,ArrayObject[0],FlipID)
                        Vertex1 = (X+1,0,Z,TextureID,FaceID,ArrayObject[1],FlipID)
                        Vertex2 = (X+1,0,Z+1,TextureID,FaceID,ArrayObject[2],FlipID)
                        Vertex3 = (X,0,Z+1,TextureID,FaceID,ArrayObject[3],FlipID)

                        if (FlipID):
                            Index = self.AddData(VertexData,Index,Vertex1,Vertex0,Vertex3,Vertex1,Vertex3,Vertex2)
                        else:
                            Index = self.AddData(VertexData,Index,Vertex0,Vertex3,Vertex2,Vertex0,Vertex2,Vertex1)

                    if ((X,Z) in self.Map.CeilingMap):
                        TextureID = self.Map.CeilingMap[(X,Z)]
                        FaceID = 1

                        Vertex0 = (X,1,Z,TextureID,FaceID,ArrayObject[0],FlipID)
                        Vertex1 = (X+1,1,Z,TextureID,FaceID,ArrayObject[1],FlipID)
                        Vertex2 = (X+1,1,Z+1,TextureID,FaceID,ArrayObject[2],FlipID)
                        Vertex3 = (X,1,Z+1,TextureID,FaceID,ArrayObject[3],FlipID)

                        if (FlipID):
                            Index = self.AddData(VertexData,Index,Vertex1,Vertex3,Vertex0,Vertex1,Vertex2,Vertex3)
                        else:
                            Index = self.AddData(VertexData,Index,Vertex0,Vertex2,Vertex3,Vertex0,Vertex1,Vertex2)

                if (PositionNotInWallMap): continue

                TextureID = self.Map.WallMap[(X,Z)]

                if (not self.IsBlocked(X,Z-1)):
                    FaceID = 2
                    ArrayObject = self.GetArrayObject(X,Z-1,Plane='Z')
                    FlipID = ArrayObject[1] + ArrayObject[3] > ArrayObject[0] + ArrayObject[2]

                    Vertex0 = (X,0,Z,TextureID,FaceID,ArrayObject[0],FlipID)
                    Vertex1 = (X,1,Z,TextureID,FaceID,ArrayObject[1],FlipID)
                    Vertex2 = (X+1,1,Z,TextureID,FaceID,ArrayObject[2],FlipID)
                    Vertex3 = (X+1,0,Z,TextureID,FaceID,ArrayObject[3],FlipID)

                    if (FlipID):
                        Index = self.AddData(VertexData,Index,Vertex3,Vertex0,Vertex1,Vertex3,Vertex1,Vertex2)
                    else:
                        Index = self.AddData(VertexData,Index,Vertex0,Vertex1,Vertex2,Vertex0,Vertex2,Vertex3)

                if (not self.IsBlocked(X,Z+1)):
                    FaceID = 3
                    ArrayObject = self.GetArrayObject(X,Z+1,Plane='Z')
                    FlipID = ArrayObject[1] + ArrayObject[3] > ArrayObject[0] + ArrayObject[2]

                    Vertex0 = (X,0,Z+1,TextureID,FaceID,ArrayObject[0],FlipID)
                    Vertex1 = (X,1,Z+1,TextureID,FaceID,ArrayObject[1],FlipID)
                    Vertex2 = (X+1,1,Z+1,TextureID,FaceID,ArrayObject[2],FlipID)
                    Vertex3 = (X+1,0,Z+1,TextureID,FaceID,ArrayObject[3],FlipID)

                    if (FlipID):
                        Index = self.AddData(VertexData,Index,Vertex3,Vertex1,Vertex0,Vertex3,Vertex2,Vertex1)
                    else:
                        Index = self.AddData(VertexData,Index,Vertex0,Vertex2,Vertex1,Vertex0,Vertex3,Vertex2)

                if (not self.IsBlocked(X+1,Z)):
                    FaceID = 4
                    ArrayObject = self.GetArrayObject(X+1,Z,Plane='X')
                    FlipID = ArrayObject[1] + ArrayObject[3] > ArrayObject[0] + ArrayObject[2]
                    
                    Vertex0 = (X+1,0,Z,TextureID,FaceID,ArrayObject[0],FlipID)
                    Vertex1 = (X+1,1,Z,TextureID,FaceID,ArrayObject[1],FlipID)
                    Vertex2 = (X+1,1,Z+1,TextureID,FaceID,ArrayObject[2],FlipID)
                    Vertex3 = (X+1,0,Z+1,TextureID,FaceID,ArrayObject[3],FlipID)

                    if (FlipID):
                        Index = self.AddData(VertexData,Index,Vertex3,Vertex0,Vertex1,Vertex3,Vertex1,Vertex2)
                    else:
                        Index = self.AddData(VertexData,Index,Vertex0,Vertex1,Vertex2,Vertex0,Vertex2,Vertex3)

                if (not self.IsBlocked(X-1,Z)):
                    FaceID = 5
                    ArrayObject = self.GetArrayObject(X-1,Z,Plane='X')
                    FlipID = ArrayObject[1] + ArrayObject[3] > ArrayObject[0] + ArrayObject[2]

                    Vertex0 = (X,0,Z,TextureID,FaceID,ArrayObject[0],FlipID)
                    Vertex1 = (X,1,Z,TextureID,FaceID,ArrayObject[1],FlipID)
                    Vertex2 = (X,1,Z+1,TextureID,FaceID,ArrayObject[2],FlipID)
                    Vertex3 = (X,0,Z+1,TextureID,FaceID,ArrayObject[3],FlipID)

                    if (FlipID):
                        Index = self.AddData(VertexData,Index,Vertex3,Vertex1,Vertex0,Vertex3,Vertex2,Vertex1)
                    else:
                        Index = self.AddData(VertexData,Index,Vertex0,Vertex2,Vertex1,Vertex0,Vertex3,Vertex2)
       
        return VertexData[:Index]

                    
