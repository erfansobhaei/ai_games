import sys
import copy
import random
import math

n = 0
queens = []
temperature = 0

def init(src):
    with open(src, 'r') as reader:
        global queens,n, temperature
        n = int(reader.readline().strip('\n'))
        temperature = (n*(n-1))/2
        tmp = reader.readline().strip('\n').split(' ')

        # Adding column index to row indexes
        queens = [[int(item), index] for index,item in enumerate(tmp)]


def get_evalfunc_table():
    evalfunc_values = [ [0 for _ in range(n)] for _ in range(n) ]
    for i in range(n):
        for j in range(n):
            tmp = copy.deepcopy(queens)
            tmp[j] = [i, j]
            evalfunc_values[i][j] = calculate_h(tmp)
    return evalfunc_values


def calculate_h(queens):
    checks = 0
    for i in range(n):
        for j in range(i+1,n):
            if queens[i][0] == queens[j][0]:
                checks += 1
                continue
            delta_y = abs(queens[i][0]-queens[j][0])
            delta_x = abs(queens[i][1]-queens[j][1])
            if delta_x == delta_y:
                checks += 1

    return int((n*(n-1))/2) - (checks)


def simulated_annealing():
    global temperature
    t = 0
    current = copy.deepcopy(queens)
    while True: 
        temperature = schedule(t)
        if temperature <= 0:
            break
        next_state = make_random_successor(current)
        delta_E = calculate_h(next_state) - calculate_h(current)
    
        if delta_E > 0:
            current = copy.deepcopy(next_state)
        elif is_promising(delta_E):
            current = copy.deepcopy(next_state)
        t += 1
    return current

def schedule(t):
    return (n*(n-1))/2 - t*(((n*(n-1))/2)/50)

def make_random_successor(current):
    c = random.randint(0, n-1)
    r = random.randint(0, n-1)
    while [r,c] in current:
        r = random.randint(0, n-1)
    next_state = copy.deepcopy(current)
    next_state[c] = [r,c]
    return next_state

def is_promising(delta_E):
    p = (math.e)**(delta_E/temperature)
    return random.uniform(0 ,1) <= p




init(sys.argv[1].strip())
table = get_evalfunc_table()
solution = simulated_annealing()

