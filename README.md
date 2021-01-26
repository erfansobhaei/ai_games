# Simple Artificial Inteligence Games
This repository consists of three simple games which are using artificial intelligence search algorithms:

## 1. Maze Problem using A* Algorithm
The [maze solver script](/MazeProblem/maze.py) using A* algorithm which is an informed search algorithm and it utilizes [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry) as heuristic for finding optimal path from the start state of the maze to its goal state.

### How to Specify Mazes?
As you can see in the following figure, each tile is made of a 4-bit binary number.

![bits](/MazeProblem/docs/bits.png)

Thus, each tile in the maze has a corresponding 4-bit number, from 0 to 15. See the conversion table:

![conversion table](/MazeProblem/docs/conversion_table.png)

The text file should have following sections respectivly:
1. Dimenstion of maze. ```n m``` specifies a maze with ```n``` rows and ```m``` columns.
2. Indexes of the start state. ```i j```
3. Indexes of the goal state. ```i j```
4. A matrix consists of ```n``` rows and ```m``` decimal numbers based on the conversion table.

#### Example
The following maze is modified using conversion table:

![example](/MazeProblem/docs/example.png)

### How to Run Code?
First of all, make sure of installing python. Second, install *matplotlib* using following command.

```pip3 install matplotlib```

For running program use following command while you are in *maze.py* directory

```python3 maze.py path-to-map.txt [path-to-other-map(s).txt]```

### How to Find Out Solution?
As you run script, it will print actions sequence from the start state to the goal in the terminal. You can see previous example solution:
```Actions of map.txt: ['DOWN', 'DOWN', 'DOWN', 'DOWN', 'DOWN', 'RIGHT', 'DOWN', 'RIGHT', 'RIGHT', 'RIGHT', 'UP', 'RIGHT', 'UP', 'RIGHT', 'RIGHT', 'DOWN', 'DOWN', 'RIGHT', 'DOWN', 'DOWN', 'DOWN', 'RIGHT', 'UP', 'UP']```

Also you can see the visual form of steps in the corresponding ```.png```(s) file which is created in the same directory. The figure below is image of example's solution:

![example](/MazeProblem/docs/example_result.png)
