from pathState import PathState

import numpy as np
import abc


class Solver(abc.ABC):
    # Create an interface for a solver class
    # This is more of a formality than holding logic

    @abc.abstractmethod
    def step(self):
    # Next update to the function returns the np array of size of the board using path states        
        pass

class BreathFirst(Solver):
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