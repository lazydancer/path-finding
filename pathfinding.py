import sys
from collections import namedtuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create a board type to seperate the const board to the changing state of the solver function
Board = namedtuple('Board', 'walls, start, end')

# Enum
class PathState:
    FOUND = 0
    REVIEWED = 1
    QUEUED = 2
    NOTHING = 3 

def color(board, state):
    # Inputs the board and the state and ouputs an narray of colours
    _COLORS = {
        PathState.FOUND: (25/255, 170/255, 188/255),
        PathState.REVIEWED: (30/255, 201/255, 223/255),
        PathState.QUEUED: (60/255, 255/255, 255/255),
        PathState.NOTHING: (1,1,1), #White
        'Wall': (35/255, 35/255, 35/255),
        'Start': (25/255, 170/255, 188/255),
        'End': (188/255, 44/255, 25/255)
    }
    
    result = np.array([[_COLORS[y] for y in x] for x in state], dtype=np.float)
    result[board.start[1], board.start[0]] = _COLORS['Start']
    result[board.end[1], board.end[0]] = _COLORS['End']
    for wall in board.walls:
        result[wall[1], wall[0]] = _COLORS['Wall']
    
    return result
    

class Solver:
    def __init__(self, board):
        # Constants for an object
        self._board = board
        
        # State Variables
        self._visited = set()
        self._queue = set()
        self._queue.add(self._board.start)
        self._state = np.empty([3, 3])
        self._state.fill(PathState.NOTHING)
        
    def _add_neighbours(self, pos):
        result = []
        
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dir in directions:
            new_x = pos[0] + dir[0]
            if new_x < 0 or new_x > 2:
                continue
            new_y = pos[1] + dir[1]
            if new_y < 0 or new_y > 2:
                continue
            
            new_pos = (new_x, new_y)

            if new_pos in self._visited:
                continue

            if new_pos in self._board.walls:
                continue
            
            result.append(new_pos)

        return result

    def step(self):
        self._calculation()
        self._updateState()

        return self._state

    def _calculation(self):
        next_queue = set()

        for pos in self._queue:

            if pos == self._board.end:
                print("Party")
            
            self._visited.add(pos)

            for n in self._add_neighbours(pos):
                next_queue.add(n)
        
        self._queue = next_queue

    def _updateState(self):
        for v in self._visited:
            self._state[v[1], v[0]] = PathState.REVIEWED        
        for q in self._queue:
            self._state[q[1], q[0]] = PathState.QUEUED
       
class Grapher:
    def __init__(self, board, solver_class):
        self.fig = plt.figure()
        self.im = plt.imshow(np.random.random((3,3)), interpolation='none')
        self._board = board
        self._solver_class = solver_class

    # initialization function: plot the background of each frame
    def init(self):
        self.solver = self._solver_class(self._board)
        x = color(self._board, self.solver.step())
        self.im.set_data(x)
        
        return [self.im]

    # animation function.  This is called sequentially
    def update(self, _frame_num):
        x = color(self._board, self.solver.step())
        self.im.set_data(x)
        
        return [self.im]


if __name__ == '__main__':
    board = Board(
        walls = [(1, 1)],
        start = (0, 1),
        end   = (2, 1)
    )

    graph = Grapher(board, Solver)

    anim = FuncAnimation(
        graph.fig, 
        graph.update, 
        frames=5,
        init_func=graph.init,
        blit=True,
        interval=1000
    )
    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        anim.save('dist/line.gif', dpi=80, writer='imagemagick')
    else:
        plt.show() # will just loop the animation forever.
