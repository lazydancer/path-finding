import sys
from collections import namedtuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from solvers import BreathFirst, DepthFirst
from pathState import PathState

# Create a board type to seperate the const board to the changing state of the solver function
Board = namedtuple('Board', 'size, walls, start, end')

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
    

class Grapher:

    def __init__(self, board, solver_class):
        self.fig = plt.figure()
        self.im = plt.imshow(np.random.random(board.size), interpolation='none')
        self.board = board
        self.solver_class = solver_class

    # initialization function: plot the background of each frame
    def init(self):
        self.solver = self.solver_class(self.board)
        x = color(self.board, self.solver.step())
        self.im.set_data(x)
        
        return [self.im]

    # animation function.  This is called sequentially
    def update(self, _frame_num):
        x = color(self.board, self.solver.step())
        self.im.set_data(x)
        
        return [self.im]

    def isComplete(self):
        return self.solver.isComplete()

if __name__ == '__main__':
    board = Board(
        size = (50, 50),
        walls = [(1, 1), (1, 2)],
        start = (0, 1),
        end   = (49, 41)
    )

    graph = Grapher(board, BreathFirst)

    def gen():
        i = 0
        while not graph.isComplete():
            i += 1
            yield i

    anim = FuncAnimation(
        graph.fig, 
        graph.update, 
        frames=200,
        init_func=graph.init,
        blit=True,
        interval=16,
        repeat_delay=200,
    )

    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        anim.save('dist/line.gif', dpi=80, writer='imagemagick') # progress_callback=lambda i, n: print(f'Saving frame {i} of {n}')
    else:
        plt.show() # will just loop the animation forever.
