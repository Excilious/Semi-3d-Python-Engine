from Settings import *

class PathFinder:
    def __init__(self,Engine):
        self.Engine = Engine
        self.LevelMap = Engine.LevelMap
        self.WallMap = Engine.LevelMap.WallMap
        self.Direction = ([-1,0],[0,-1],[1,0],[0,1],[-1,-1],[1,-1],[1,1],[-1,1])
        self.Graph = {}
        self.UpdateGraph()

    @lru_cache
    def Find(self,StartPosition,EndPosition):
        Visited = self.Branch(StartPosition,EndPosition)
        Path = [EndPosition]
        Step = Visited.get(EndPosition,StartPosition)

        while (Step and Step != StartPosition):
            Path.append(Step)
            Step = Visited[Step]
        return Path[-1]

    def Branch(self,Start,Goal):
        Queue = deque([Start])
        Visited = {Start: None}

        while Queue:
            CurrentNode = Queue.popleft()
            if CurrentNode == Goal: break
            NextNode = self.Graph[CurrentNode]

            for NewNode in NextNode:
                if (NewNode not in Visited and NewNode not in self.Engine.LevelMap.NPCMap):
                    Queue.append(NewNode)
                    Visited[NewNode] = CurrentNode
        return Visited

    def GetNextNode(self,X,Y):
        return [
            (X +DeltaX,Y+DeltaY) for DeltaX,DeltaY in self.Direction if (X+DeltaX,Y+DeltaY) not in self.WallMap
        ]

    def UpdateGraph(self):
        for Y in range(self.LevelMap.Depth):
            for X in range(self.LevelMap.Width):
                self.Graph[(X,Y)] = self.Graph.get((X,Y),[]) + self.GetNextNode(X,Y)
