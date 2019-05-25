from pathState import PathState

import numpy as np

class BreathFirst:
    def __init__(self, board):
        # Constants
        self._board = board
        
        # Variables
        self._visited = set()
        self._queue = [(self._board.start, [self._board.start])]
        self._state = np.full(board.size, PathState.NOTHING)
        self._solution_path = []

    def step(self):
        if self._solution_path != []:
            return self._state
        
        self._calculation()
        self._updateState()

        return self._state

    def isComplete(self):
        return self._solution_path != []

    def _calculation(self):
        next_queue = []

        while self._queue:
            vertex, path = self._queue.pop(0)
            self._visited.add(vertex)       

            for node in self._add_neighbours(vertex):
                if node == self._board.end:
                    self._solution_path =  path + [self._board.end]
                else:
                    self._visited.add(node)
                    next_queue.append((node, path + [node]))
        
        self._queue = next_queue

    def _updateState(self):
        for v in self._visited:
            self._state[v[1], v[0]] = PathState.REVIEWED        
        for v in self._queue:
            self._state[v[0][1], v[0][0]] = PathState.QUEUED
        for v in self._solution_path:
            self._state[v[1], v[0]] = PathState.FOUND
    
    def _add_neighbours(self, pos):
        (x, y) = pos
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        
        results = filter(self._in_bounds, results)
        results = filter(self._passable, results)
 
        return results

    def _in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self._board.size[0] and 0 <= y < self._board.size[1]

    def _passable(self, id):
        return id not in self._visited and id not in self._board.walls

class DepthFirst:
    def __init__(self, board):
        # Constants
        self._board = board
        
        # Variables
        self._visited = set()
        self._stack = [(self._board.start, [self._board.start])]
        self._state = np.full(board.size, PathState.NOTHING)
        self._solution_path = []

    def step(self):
        if self._solution_path != []:
            return self._state
        
        self._calculation()
        self._updateState()

        return self._state

    def isComplete(self):
        return self._solution_path != []

    def _calculation(self):
        (vertex, path) = self._stack.pop()

        if vertex not in self._visited:
            self._visited.add(vertex)

            for neighbour in self._add_neighbours(vertex):
                if neighbour == self._board.end:
                    self._solution_path = path
                else:
                    self._stack.append((neighbour, path + [neighbour]))

    def _updateState(self):
        for v in self._stack:
            self._state[v[0][1], v[0][0]] = PathState.QUEUED
        for v in self._visited:
            self._state[v[1], v[0]] = PathState.REVIEWED        
        for v in self._solution_path:
            self._state[v[1], v[0]] = PathState.FOUND

    def _add_neighbours(self, pos):
        (x, y) = pos
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        
        results = filter(self._in_bounds, results)
        results = filter(self._passable, results)
 
        return results

    def _in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self._board.size[0] and 0 <= y < self._board.size[1]

    def _passable(self, id):
        return id not in self._visited and id not in self._board.walls