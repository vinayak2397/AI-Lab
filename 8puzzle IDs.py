import copy
import time
import numpy as np

class PuzzleNode:
    def __init__(self, init=None):
        self.goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        self.node = self.goal.copy() if init is None else init.copy()
        self.i0 = 2
        self.j0 = 2
        if init is not None:
            for i in range(3):
                for j in range(3):
                    if self.node[i][j] == 0:
                        self.i0 = i
                        self.j0 = j
        self.parent = None

    def down(self):
        assert self.i0 > 0
        i0 = self.i0
        j0 = self.j0
        self.node[i0][j0], self.node[i0 - 1][j0] = self.node[i0 - 1][j0], self.node[i0][j0]
        self.i0 -= 1

    def up(self):
        assert self.i0 < 2
        i0 = self.i0
        j0 = self.j0
        self.node[i0][j0], self.node[i0 + 1][j0] = self.node[i0 + 1][j0], self.node[i0][j0]
        self.i0 += 1

    def right(self):
        assert self.j0 > 0
        i0 = self.i0
        j0 = self.j0
        self.node[i0][j0], self.node[i0][j0 - 1] = self.node[i0][j0 - 1], self.node[i0][j0]
        self.j0 -= 1

    def left(self):
        assert self.j0 < 2
        i0 = self.i0
        j0 = self.j0
        self.node[i0][j0], self.node[i0][j0 + 1] = self.node[i0][j0 + 1], self.node[i0][j0]
        self.j0 += 1

    def getValidMoves(self):
        validDir = []

        if self.i0 > 0:
            validDir.append('d')
        if self.i0 < 2:
            validDir.append('u')
        if self.j0 > 0:
            validDir.append('r')
        if self.j0 < 2:
            validDir.append('l')
        return validDir

    def doMove(self, moveChar):
        if moveChar == 'd':
            self.down()
        elif moveChar == 'u':
            self.up()
        elif moveChar == 'r':
            self.right()
        elif moveChar == 'l':
            self.left()

    def randomStep(self):
        validDir = self.getValidMoves()

        dirNum = len(validDir)
        randomDir = validDir[np.random.randint(0, dirNum)]
        self.doMove(randomDir)

    def shuffle(self, shuffleTime=20):
        for i in range(shuffleTime):
            self.randomStep()

    def isGoal(self):
        return (self.node == self.goal).all()

    def numOfWrong(self):
        return 9 - np.sum(self.node == self.goal)

    def show(self):
        print(self.node)


def iterativeDeepeningSearch(startNode):
    maxLayer = 1
    while True:
        dfsList = []
        layer = 0
        dfsList.append((startNode, layer))

        while len(dfsList) != 0:
            top = dfsList.pop()
            tmpNode = top[0]
            tmpLayer = top[1]
            if tmpNode.isGoal():
                trace = []
                ptr = tmpNode
                while ptr is not None:
                    trace.append(ptr.node)
                    ptr = ptr.parent
                return tmpLayer, trace

            nextLayer = tmpLayer + 1
            if nextLayer > maxLayer:
                continue

            validMoves = tmpNode.getValidMoves()
            for moveChar in validMoves:
                nextNode = copy.deepcopy(tmpNode)
                nextNode.doMove(moveChar)
                if not inDFSNodeList(nextNode, dfsList):
                    dfsList.append((nextNode, nextLayer))
                    nextNode.parent = tmpNode
        maxLayer += 1


# check if tNode is in nList (used in iterativeDeepeningSearch())
# nList is a list of tuple (puzzleNode, layer)
def inDFSNodeList(tNode, nList):
    for node in nList:
        if (node[0].node == tNode.node).all():
            return True
    return False

# check is tNode is in nList (used in AStarSearch() and greedySearch())
# nList is a list of PuzzleNode
def inNodeList(tNode, nList):
    for node in nList:
        if (node.node == tNode.node).all():
            return True
    return False

# test average execution time of 20 randomly generated samples
def testIDS():
    totaltime = 0
    print('Testing IDS:')
    for i in range(20):
        print('sample ' + str(i))
        test = PuzzleNode()
        test.shuffle()
        test.show()
        start = time.time()
        step, _ = iterativeDeepeningSearch(test)
        end = time.time()
        print(step)
        totaltime += (end - start)
    avg = totaltime / 20
    print(avg)

# print solution trace
test = PuzzleNode()
test.shuffle()
test.show()
step, trace = iterativeDeepeningSearch(test)
print(step)
while len(trace) != 0:
    n = trace.pop()
    print(n)
