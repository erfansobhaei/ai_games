import sys
import copy

dimension = []
start = []
goal = []

class Node():
    def __init__(self, modifier, index, status = None):
        global goal
        self.index = index
        self.walls = '{0:04b}'.format(modifier)
        self.heuristic = abs(index[0]-goal[0]) + abs(index[1]-goal[1])
        self.evalfunc = abs(index[0]-goal[0]) + abs(index[1]-goal[1])
        self.status = status
        self.left = self.up = self.right = self.down = None

    def successors(self, nodes):
        result = []
        # Check for left succesor
        if self.walls[0] == '0' and self.status != "RIGHT":
            self.left = copy.deepcopy(nodes[self.index[0]][self.index[1]-1])
            self.left.increase_evalfunc(self.evalfunc - self.heuristic + 1)
            self.left.set_status("LEFT")
            result.append(self.left)
        # Check for upper succesor
        if self.walls[1] == '0' and self.status != "DOWN":
            self.up = copy.deepcopy(nodes[self.index[0]-1][self.index[1]])
            self.up.increase_evalfunc(self.evalfunc - self.heuristic + 1)
            self.up.set_status("UP")
            result.append(self.up)
        # Check for right succesor
        if self.walls[2] == '0' and self.status != "LEFT":
            self.right = copy.deepcopy(nodes[self.index[0]][self.index[1]+1])
            self.right.increase_evalfunc(self.evalfunc - self.heuristic + 1)
            self.right.set_status("RIGHT")
            result.append(self.right)
        # Check for bottom succesor
        if self.walls[3] == '0' and self.status != "UP":
            self.down = copy.deepcopy(nodes[self.index[0]+1][self.index[1]])
            self.down.increase_evalfunc(self.evalfunc - self.heuristic + 1)
            self.down.set_status("DOWN")
            result.append(self.down)
        return result
    
    def increase_evalfunc(self, number):
        self.evalfunc += number

    def set_status(self, status):
        self.status = status

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
        nodes = [ [0 for _ in range(dimension[1])] for _ in range(dimension[0]) ]
        modifiers = [[int(x) for x in line.split(' ')] for line in reader]
        for i in range(dimension[0]):
            for j in range(dimension[1]):
                nodes[i][j] = Node(modifiers[i][j], [i, j])
        return nodes

def A_start_search(nodes):
    actions = []
    closed_list = []
    
    # Appending start state at begininng of algorithm
    open_list = [ nodes[start[0]][start[1]] ]

    while open_list:
        # Searching open list for find node with minimum evaluation function
        chosen = 0
        for i in range(len(open_list)):
            min = float('inf')
            if open_list[i].evalfunc < min:
                min = open_list[i].evalfunc
                chosen = i
        node = open_list.pop(chosen)
        if node.status:
            actions.append(node.status)

        # Checking goal description for chosen node
        if (node.index == goal):
            return actions

        # Checking weather chosen node has not any child
        successors = node.successors(nodes)
        if not successors:
            closed_list.append(node)
            continue

        for child in successors:
            flag = True
            # Checking if chosen child is already on open_list (and update it)
            for n in open_list:
                if n.index == child.index:
                    flag = False
                    if n.evalfunc > child.evalfunc:
                        open_list.remove(n)
                        open_list.append(child)
                    

            # Checking if chosen child is already on closed_list (and update it)
            for n in closed_list:
                if n.index == child.index:
                    flag = False
                    if n.evalfunc > child.evalfunc:
                        closed_list.remove(n)
                        open_list.append(child)

            # Appending child to open_list
            if flag:
                open_list.append(child)

        # Appending child to closed_list
        closed_list.append(node)
     
    return False


nodes = initMaze(sys.argv[1])
print(A_start_search(nodes))