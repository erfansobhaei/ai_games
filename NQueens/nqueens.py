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


init(sys.argv[1])
