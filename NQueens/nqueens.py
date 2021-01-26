import sys
import copy

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


init(sys.argv[1])
table = get_evalfunc_table()


