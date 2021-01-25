import sys

dimension = []
start = []
goal = []

def initMaze(src):
    with open(src, 'r') as reader:
        global dimension, start, goal
        dimension = reader.readline().strip('\n').split(' ')
        dimension = [ int(x) for x in dimension ]
        start = reader.readline().strip('\n').split(' ')
        start = [ int(x) for x in start ]
        goal = reader.readline().strip('\n').split(' ')
        goal = [ int(x) for x in goal ]
        lines = reader.readlines()


initMaze(sys.argv[1])
print(dimension)
print(start)
print(goal)
