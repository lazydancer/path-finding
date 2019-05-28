import sys
from collections import namedtuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from solvers import BreathFirst, DepthFirst, Dijkstra, BestFirst, AStar
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
        self.board = board
        self.solver_class = solver_class

        self.fig = plt.figure()
        self.im = plt.imshow(np.random.random(board.size), interpolation='none')
        

    # initialization function: plot the background of each frame
    def init_solver(self):
        self.solver = self.solver_class(self.board)
        return self.update(0)

    # animation function.  This is called sequentially
    def update(self, _frame_num):
        colored_board = color(self.board, self.solver.step())
        self.im.set_data(colored_board)
        
        return [self.im]

    def isComplete(self):
        return self.solver.isComplete()

if __name__ == '__main__':
    board = Board(
        size = (30, 30),
        walls = [(10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (17, 11), (17, 12), (17, 13), (17, 14), (17, 15), (17, 16), (17, 17), (17, 18), (17, 19), (17, 20), (16, 20), (15, 20), (14, 20), (13, 20), (12, 20), (11, 20), (10, 20)],
        start = (1, 15),
        end   = (29, 15)
    )

    graph = Grapher(board, Dijkstra)

    anim = FuncAnimation(
        graph.fig, 
        graph.update, 
        frames=2000,
        init_func=graph.init_solver,
        blit=True,
        interval=16,
        repeat_delay=200,
    )

    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        #anim.save('dist/line.gif', dpi=100, writer='imagemagick', progress_callback=lambda i, n: print(f'Saving frame {i} of {n}'))
        anim.save('dist/line.mkv', 
            codec='vp8', # used instead of h264 
            extra_args=["-auto-alt-ref", "0"], #Error if not used with vp8
            progress_callback=lambda i, n: print(f'Saving frame {i} of {n}')
        )
    else:
        plt.show() # will just loop the animation forever.
