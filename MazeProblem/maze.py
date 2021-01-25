import sys

dimension = []
start = []
goal = []

class Node():
    def __init__(self, modifier, index):
        global goal
        self.walls = '{0:04b}'.format(modifier)
        self.heuristic = abs(index[0]-goal[0]) + abs(index[1]-goal[1])

    def __str__(self):
        return self.walls + "  " +  str(self.heuristic)

def initMaze(src):
    with open(src, 'r') as reader:
        global dimension, start, goal
        # Reading dimension of states
        dimension = reader.readline().strip('\n').split(' ')
        dimension = [ int(x) for x in dimension ]
        # Reading start state
        start = reader.readline().strip('\n').split(' ')
        start = [ int(x) for x in start ]
        # Reading goal state
        goal = reader.readline().strip('\n').split(' ')
        goal = [ int(x) for x in goal ]
        # Reading modifier number of each state and initializing nodes
        nodes = [[0 for _ in range(dimension[1])] for _ in range(dimension[0])]
        modifiers = [[int(x) for x in line.split(' ')] for line in reader]
        for i in range(dimension[0]):
            for j in range(dimension[1]):
                nodes[i][j] = Node(modifiers[i][j], [i, j])
        return nodes


nodes = initMaze(sys.argv[1])
