import sys
import copy
import random
import math

n = 0
queens = []
temperature = 0
no_of_setps = 0

def init(src, steps):
    with open(src, 'r') as reader:
        global queens,n, temperature, no_of_setps
        n = int(reader.readline().strip('\n'))
        temperature = (n*(n-1))/2
        no_of_setps = steps
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


def simulated_annealing(src):
    global temperature
    t = 0
    current = copy.deepcopy(queens)
    with open(src + "_log.txt", 'w') as writer:
        writer.write("No.{}Current{}h{}Next{}h{}Temprature{}DeltaE{}Status\n".format(" "*5, " "*n*8, " "*8, " "*n*8, " "*8, " "*2, " "*5))
        writer.write("-"*n*30 + '\n')
        while True:
            flag = False
            temperature = schedule(t)
            if temperature <= 0:
                break
            next_state = make_random_successor(current)
            current_h = calculate_h(current)
            next_state_h = calculate_h(next_state)
            delta_E = next_state_h - current_h
            tmp = current
            if delta_E > 0:
                flag = True
                current = copy.deepcopy(next_state)
            elif is_promising(delta_E):
                flag = True
                current = copy.deepcopy(next_state)
            writer.write(format_iteration(t, tmp, current_h, next_state, next_state_h, delta_E, flag))
            t += 1
    return current

def schedule(t):
    return (n*(n-1))/2 - t*(((n*(n-1))/2)/no_of_setps)

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


def format_iteration(t, current, h1, next_state, h2, delta_E, flag):
    sign = " "
    if delta_E > 0:
        sign = "+"
    elif delta_E < 0:
        sign = ""
    return '{:02d}. \t{}       {}\t\t{}    {}\t\t{:04f}\t{}{}\t\t  {}\n'.format(t, current, h1, next_state, h2, temperature, sign ,delta_E, "Taken" if flag else "Not Taken")

def print_solution(solution):
    print("Solution is " + str(solution) + "  with h = {} from {}".format(calculate_h(solution), int(n*(n-1)/2)))
    map = [["-  " for _ in range(n)] for _ in range(n)]
    for i in solution:
        map[i[0]][i[1]] = '\u2655  '
    for row in map:
        print("".join(row))


init(sys.argv[1], steps= 100 if len(sys.argv) < 3 else int(sys.argv[2]))
table = get_evalfunc_table()
solution = simulated_annealing(sys.argv[1])


