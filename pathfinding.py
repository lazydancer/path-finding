import sys
from collections import namedtuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create a board type to seperate the const board to the changing state of the solver function
Board = namedtuple('Board', 'size, walls, start, end')

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
        PathState.REVIEWED: (120/255, 224/255, 237/255),
        PathState.QUEUED: (210/255, 245/255, 249/255),
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
        self.solution_found = False
        self._visited = set()
        self._queue = []
        self._queue.append((self._board.start, [self._board.start]))
        self._state = np.empty(board.size)
        self._state.fill(PathState.NOTHING)
        
    def _add_neighbours(self, pos):
        result = []
        
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dir in directions:
            new_x = pos[0] + dir[0]
            if new_x < 0 or new_x >= self._board.size[0]:
                continue
            new_y = pos[1] + dir[1]
            if new_y < 0 or new_y >= self._board.size[1]:
                continue
            
            new_pos = (new_x, new_y)

            if new_pos in self._visited:
                continue

            if new_pos in self._board.walls:
                continue
            
            result.append(new_pos)

        return result

    def step(self):

        if not self.solution_found:
            result = self._calculation()

            if result is not None:
                self._update_path(result)
                self.solution_found = True
            else:
                self._updateState()

        return self._state

    def _calculation(self):
        next_queue = []

        while self._queue:
            vertex, path = self._queue.pop(0)
            self._visited.add(vertex)       

            for node in self._add_neighbours(vertex):
                if node == self._board.end:
                    return path + [self._board.end]
                else:
                    self._visited.add(node)
                    next_queue.append((node, path + [node]))
        
        self._queue = next_queue

    def _updateState(self):
        for v in self._visited:
            self._state[v[1], v[0]] = PathState.REVIEWED        
        for q in self._queue:
            self._state[q[0][1], q[0][0]] = PathState.QUEUED
    
    def _update_path(self, path):
        for v in path:
            self._state[v[1], v[0]] = PathState.FOUND


class Grapher:
    def __init__(self, board, solver_class):
        self.fig = plt.figure()
        self.im = plt.imshow(np.random.random(board.size), interpolation='none')
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

    def isComplete(self):
        return not self.solver.solution_found


if __name__ == '__main__':
    board = Board(
        size = (50, 50),
        walls = [(1, 1), (1, 2)],
        start = (0, 1),
        end   = (49, 41)
    )

    graph = Grapher(board, Solver)

    def gen():
        i = 0
        while graph.isComplete():
            i += 1
            yield i

    anim = FuncAnimation(
        graph.fig, 
        graph.update, 
        frames=gen,
        init_func=graph.init,
        blit=True,
        interval=100
    )
    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        anim.save('dist/line.gif', dpi=80, writer='imagemagick')
    else:
        plt.show() # will just loop the animation forever.
