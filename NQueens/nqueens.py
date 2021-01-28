import sys
import copy
import random
import math

n = 0
nC2 = 0
queens = []
temperature = 0
no_of_setps = 0


def init(src, steps):
    with open(src, "r") as reader:
        global queens, n, nC2, temperature, no_of_setps
        # Reading basic info
        n = int(reader.readline().strip("\n"))

        # Max number of queens' pairs
        nC2 = (n * (n - 1)) / 2
        temperature = nC2
        no_of_setps = steps
        tmp = reader.readline().strip("\n").split(" ")

        # Adding column index to row indexes
        queens = [[int(item), index] for index, item in enumerate(tmp)]


def calculate_h(queens):

    checks = 0

    # Checking each combination for number of checks
    for i in range(n):
        for j in range(i + 1, n):
            # Cheking for same row
            if queens[i][0] == queens[j][0]:
                checks += 1
                continue

            # Checking for same diagonal
            delta_y = abs(queens[i][0] - queens[j][0])
            delta_x = abs(queens[i][1] - queens[j][1])
            if delta_x == delta_y:
                checks += 1

    # Returning number queens' paris which do not check each other
    return int(nC2) - (checks)


def simulated_annealing(src):
    global temperature
    t = 0
    current = copy.deepcopy(queens)

    # Printing header of log file
    with open(src + "_log.txt", "w") as writer:
        writer.write(
            "No.{}Current{}h{}Next{}h{}Temprature{}DeltaE{}Status\n".format(
                " " * 5, " " * n * 8, " " * 8, " " * n * 8, " " * 8, " " * 2,
                " " * 5))
        writer.write("-" * n * 30 + "\n")

        # Main loop of Simulated Annealing algorithm
        while True:
            flag = False

            # Updating temprature
            temperature = schedule(t)
            if temperature <= 0:
                break

            # Processing random chosen successor
            next_state = make_random_successor(current)
            current_h = calculate_h(current)
            next_state_h = calculate_h(next_state)
            delta_E = next_state_h - current_h
            tmp = current

            # Better state
            if delta_E > 0:
                flag = True
                current = copy.deepcopy(next_state)

            # Worse or equal state
            elif is_promising(delta_E):
                flag = True
                current = copy.deepcopy(next_state)

            # Writng properties of this iteration in the log file
            writer.write(
                format_iteration(t, tmp, current_h, next_state, next_state_h,
                                 delta_E, flag))
            t += 1

    return current


def schedule(t):
    return nC2 - t * ((nC2) / no_of_setps)


def make_random_successor(current):

    # Choosing random column number
    c = random.randint(0, n - 1)

    # Choosing random row number
    r = random.randint(0, n - 1)

    # Keep trying until choosing a row which is not equal to current row
    while [r, c] in current:
        r = random.randint(0, n - 1)

    # Updating new random state
    next_state = copy.deepcopy(current)
    next_state[c] = [r, c]

    return next_state


def is_promising(delta_E):

    # Calculating probabilty of movement
    p = (math.e)**(delta_E / temperature)

    return random.uniform(0, 1) <= p


def format_iteration(t, current, h1, next_state, h2, delta_E, flag):

    # Checking for sign of delta E
    sign = " "
    sign = "+" if delta_E > 0 else ""

    # Adjusting properties of iteration
    return "{:02d}. \t{}       {}\t\t{}    {}\t\t{:04f}\t{}{}\t\t  {}\n".format(
        t,
        current,
        h1,
        next_state,
        h2,
        temperature,
        sign,
        delta_E,
        "Taken" if flag else "Not Taken",
    )


def print_solution(solution):
    # Printing properties of final solution
    print("Solution is " + str(solution) +
          "  with h = {} from {}".format(calculate_h(solution), int(nC2)))

    # Printing map of final solution
    map = [["-  " for _ in range(n)] for _ in range(n)]
    for i in solution:
        map[i[0]][i[1]] = "\u265B  "
    for row in map:
        print("".join(row))


# Default number of steps is 100 unless command has corresponding argument
init(sys.argv[1], steps=1000 if len(sys.argv) < 3 else int(sys.argv[2]))

# Calling function and printing solution
solution = simulated_annealing(sys.argv[1])
print_solution(solution)
