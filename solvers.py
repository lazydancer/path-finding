from pathState import PathState

import numpy as np

class BreathFirst:
    def __init__(self, board):
        # Constants for an object
        self._board = board
        
        # State Variables
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
        result = []
        
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dir in directions:
            new_pos = (pos[0] + dir[0], pos[1] + dir[1])

            if new_pos[0] < 0 or new_pos[0] >= self._board.size[0]:
                continue
            if new_pos[1] < 0 or new_pos[1] >= self._board.size[1]:
                continue
            
            if new_pos in self._visited:
                continue

            if new_pos in self._board.walls:
                continue
            
            result.append(new_pos)

        return result