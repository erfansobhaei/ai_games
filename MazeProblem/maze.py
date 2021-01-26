import sys
import copy
import matplotlib.pyplot as plt

dimension = []
start = []
goal = []

class Node():
    def __init__(self, modifier, index, status = None):
        global goal
        self.index = index
        self.walls = '{0:04b}'.format(modifier)
        self.heuristic = self.manhattan_distance(self.index, goal)
        self.evalfunc = self.manhattan_distance(self.index, goal)
        self.status = status
        self.left = self.up = self.right = self.down = None
    
    def manhattan_distance(self, index, goal):
        return abs(index[0]-goal[0]) + abs(index[1]-goal[1])

    def successors(self, nodes):
        result = []
        path_cost = self.evalfunc - self.heuristic
        index = self.index

        # Check for left succesor
        if self.walls[0] == '0' and self.status != "RIGHT":
            self.left = copy.deepcopy(nodes[index[0]][index[1]-1])
            self.left.increase_evalfunc(path_cost + 1)
            self.left.set_status("LEFT")
            self.left.right = self
            result.append(self.left)

        # Check for upper succesor
        if self.walls[1] == '0' and self.status != "DOWN":
            self.up = copy.deepcopy(nodes[index[0]-1][index[1]])
            self.up.increase_evalfunc(path_cost + 1)
            self.up.set_status("UP")
            self.up.down = self
            result.append(self.up)

        # Check for right succesor
        if self.walls[2] == '0' and self.status != "LEFT":
            self.right = copy.deepcopy(nodes[index[0]][index[1]+1])
            self.right.increase_evalfunc(path_cost + 1)
            self.right.set_status("RIGHT")
            self.right.left = self
            result.append(self.right)

        # Check for bottom succesor
        if self.walls[3] == '0' and self.status != "UP":
            self.down = copy.deepcopy(nodes[index[0]+1][index[1]])
            self.down.increase_evalfunc(path_cost + 1)
            self.down.set_status("DOWN")
            self.down.up = self
            result.append(self.down)

        return result
    
    def increase_evalfunc(self, number):
        self.evalfunc += number

    def set_status(self, status):
        self.status = status

    def __str__(self):
        return str(self.index) + "  " + self.evalfunc

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

        # Choosing new node from open_list
        chosen_node = open_list.pop(chosen)

        # Checking goal description for chosen node
        if (chosen_node.index == goal):
            return chosen_node

        # Checking weather chosen node has not any child
        successors = chosen_node.successors(nodes)
        if not successors:
            closed_list.append(chosen_node)
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
        closed_list.append(chosen_node)

    return False

def travers_tree_action(goal):
    actions = []
    if not isinstance(goal, Node):
        return []
    elif goal.status == "LEFT":
        actions.append("LEFT")
        actions.extend(travers_tree_action(goal.right))
    elif goal.status == "UP":
        actions.append("UP")
        actions.extend(travers_tree_action(goal.down))
    elif goal.status == "RIGHT":
        actions.append("RIGHT")
        actions.extend(travers_tree_action(goal.left))
    elif goal.status == "DOWN":
        actions.append("DOWN")
        actions.extend(travers_tree_action(goal.up))
    return actions

def travers_tree_index(goal):
    index = []
    if not isinstance(goal, Node):
        return []
    else:
        index.append(goal.index)
        if goal.status == "LEFT":
            index.extend(travers_tree_index(goal.right))
        elif goal.status == "UP":
            index.extend(travers_tree_index(goal.down))
        elif goal.status == "RIGHT":
            index.extend(travers_tree_index(goal.left))
        elif goal.status == "DOWN":
            index.extend(travers_tree_index(goal.up))
    return index

def make_visual_solution(nodes, indexes):
    maze = [ [" " for _ in range(dimension[1])] for _ in range(dimension[0]) ]
    
    plt.xticks([])
    plt.yticks([])
    plt.axes().invert_yaxis()
    plt.axis('off')
    t = plt.table(maze)
    for i in range(len(indexes)):
        t[(indexes[i][0], indexes[i][1])].get_text().set_text(str(i))
    plt.savefig("test.png", bbox_inches='tight')




for i in range(1, len(sys.argv)):
    nodes = initMaze(sys.argv[i])
    goal = A_start_search(nodes)
    actions = travers_tree_action(goal)[::-1]
    indexes = travers_tree_index(goal)[::-1]
    print("Actions of " + sys.argv[i] + ": " + str(actions))
    make_visual_solution(nodes, indexes)
    
