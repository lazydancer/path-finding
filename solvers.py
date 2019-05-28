from pathState import PathState

import numpy as np
import random

class BreathFirst:
    def __init__(self, board):
        # Constants
        self.board = board
        
        # Variables
        self.visited = set()
        self.queue = [(self.board.start, [self.board.start])]
        self.next_queue = []
        self.state = np.full(board.size, PathState.NOTHING)
        self.solution_path = []

    def step(self):
        if self.solution_path != []:
            return self.state
        
        self._calculation()
        self._updateState()

        return self.state

    def isComplete(self):
        return self.solution_path != []

    def _calculation(self):
        if self.queue == []:
            self.queue = self.next_queue
            self.next_queue = []

        vertex, path = self.queue.pop(0)
        self.visited.add(vertex)       

        for node in self._add_neighbours(vertex):
            if node == self.board.end:
                self.solution_path =  path + [self.board.end]
            else:
                self.visited.add(node)
                self.next_queue.append((node, path + [node]))
        

    def _updateState(self):
        for v in self.visited:
            self.state[v[1], v[0]] = PathState.REVIEWED        
        for v in self.queue:
            self.state[v[0][1], v[0][0]] = PathState.QUEUED
        for v in self.next_queue:
            self.state[v[0][1], v[0][0]] = PathState.QUEUED
        for v in self.solution_path:
            self.state[v[1], v[0]] = PathState.FOUND
    
    def _add_neighbours(self, pos):
        (x, y) = pos
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        
        results = filter(self._in_bounds, results)
        results = filter(self._passable, results)
 
        return results

    def _in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.board.size[0] and 0 <= y < self.board.size[1]

    def _passable(self, id):
        return id not in self.visited and id not in self.board.walls

class DepthFirst:
    def __init__(self, board):
        # Constants
        self.board = board
        
        # Variables
        self.visited = set()
        self.stack = [(self.board.start, [self.board.start])]
        self.state = np.full(board.size, PathState.NOTHING)
        self.solution_path = []

    def step(self):
        if self.solution_path != []:
            return self.state
        
        self._calculation()
        self._updateState()

        return self.state

    def isComplete(self):
        return self.solution_path != []

    def _calculation(self):
        (vertex, path) = self.stack.pop()

        if vertex not in self.visited:
            self.visited.add(vertex)

            for neighbour in self._add_neighbours(vertex):
                if neighbour == self.board.end:
                    self.solution_path = path
                else:
                    self.stack.append((neighbour, path + [neighbour]))

    def _updateState(self):
        for v in self.stack:
            self.state[v[0][1], v[0][0]] = PathState.QUEUED
        for v in self.visited:
            self.state[v[1], v[0]] = PathState.REVIEWED        
        for v in self.solution_path:
            self.state[v[1], v[0]] = PathState.FOUND

    def _add_neighbours(self, pos):
        (x, y) = pos
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        
        results = filter(self._in_bounds, results)
        results = filter(self._passable, results)
 
        results = list(results)
        random.shuffle(results)

        return results

    def _in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.board.size[0] and 0 <= y < self.board.size[1]

    def _passable(self, id):
        return id not in self.visited and id not in self.board.walls


class Dijkstra:
    def __init__(self, board):
        # Constants
        self.board = board
        
        # Variables
        self.visited = set()
        self.stack = [(self.board.start, [self.board.start], 0)]
        self.state = np.full(board.size, PathState.NOTHING)
        self.solution_path = []

    def step(self):
        if self.solution_path != []:
            return self.state
        
        self._calculation()
        self._updateState()

        return self.state

    def isComplete(self):
        return self.solution_path != []

    def _calculation(self):
        self.stack = sorted(self.stack,key=lambda x: x[2], reverse=True)
        (vertex, path, prev_weight) = self.stack.pop()

        if vertex not in self.visited:
            self.visited.add(vertex)

            for neighbour in self._add_neighbours(vertex):
                if neighbour == self.board.end:
                    self.solution_path = path
                else:
                    self.stack.append((neighbour, path + [neighbour], prev_weight + self._added_weight(neighbour) ))

    def _added_weight(self, pos):
        return abs(pos[0] - pos[1])

    def _updateState(self):
        for v in self.stack:
            self.state[v[0][1], v[0][0]] = PathState.QUEUED
        for v in self.visited:
            self.state[v[1], v[0]] = PathState.REVIEWED        
        for v in self.solution_path:
            self.state[v[1], v[0]] = PathState.FOUND

    def _add_neighbours(self, pos):
        (x, y) = pos
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        
        results = filter(self._in_bounds, results)
        results = filter(self._passable, results)
 
        results = list(results)
        random.shuffle(results)

        return results

    def _in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.board.size[0] and 0 <= y < self.board.size[1]

    def _passable(self, id):
        return id not in self.visited and id not in self.board.walls


class BestFirst:
    def __init__(self, board):
        # Constants
        self.board = board
        
        # Variables
        self.visited = set()
        self.stack = [(self.board.start, [self.board.start])]
        self.state = np.full(board.size, PathState.NOTHING)
        self.solution_path = []

    def step(self):
        if self.solution_path != []:
            return self.state
        
        self._calculation()
        self._updateState()

        return self.state

    def isComplete(self):
        return self.solution_path != []

    def _calculation(self):
        self.stack = sorted(self.stack,key=lambda x: self._added_weight(x[0]), reverse=True)
        (vertex, path) = self.stack.pop()

        if vertex not in self.visited:
            self.visited.add(vertex)

            for neighbour in self._add_neighbours(vertex):
                if neighbour == self.board.end:
                    self.solution_path = path
                else:
                    self.stack.append((neighbour, path + [neighbour]))

    def _added_weight(self, pos):
        target = self.board.end
        distance = abs(target[0] - pos[0]) + abs(target[1]-pos[1])
        return distance  

    def _updateState(self):
        for v in self.stack:
            self.state[v[0][1], v[0][0]] = PathState.QUEUED
        for v in self.visited:
            self.state[v[1], v[0]] = PathState.REVIEWED        
        for v in self.solution_path:
            self.state[v[1], v[0]] = PathState.FOUND

    def _add_neighbours(self, pos):
        (x, y) = pos
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        
        results = filter(self._in_bounds, results)
        results = filter(self._passable, results)
 
        results = list(results)
        random.shuffle(results)

        return results

    def _in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.board.size[0] and 0 <= y < self.board.size[1]

    def _passable(self, id):
        return id not in self.visited and id not in self.board.walls

class AStar:
    def __init__(self, board):
        # Constants
        self.board = board
        
        # Variables
        self.visited = set()
        self.stack = [(self.board.start, [self.board.start], 0)]
        self.state = np.full(board.size, PathState.NOTHING)
        self.solution_path = []

    def step(self):
        if self.solution_path != []:
            return self.state
        
        self._calculation()
        self._updateState()

        return self.state

    def isComplete(self):
        return self.solution_path != []

    def _calculation(self):
        self.stack = sorted(self.stack,key=lambda x: x[2] + self._added_weight(x[0]), reverse=True)
        (vertex, path, prev_weight) = self.stack.pop()

        if vertex not in self.visited:
            self.visited.add(vertex)

            for neighbour in self._add_neighbours(vertex):
                if neighbour == self.board.end:
                    self.solution_path = path
                else:
                    self.stack.append((neighbour, path + [neighbour], prev_weight + self._added_weight(neighbour) ))

    def _added_weight(self, pos):
        target = self.board.end
        distance = abs(target[0] - pos[0]) + abs(target[1]-pos[1])
        return distance 

    def _updateState(self):
        for v in self.stack:
            self.state[v[0][1], v[0][0]] = PathState.QUEUED
        for v in self.visited:
            self.state[v[1], v[0]] = PathState.REVIEWED        
        for v in self.solution_path:
            self.state[v[1], v[0]] = PathState.FOUND

    def _add_neighbours(self, pos):
        (x, y) = pos
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        
        results = filter(self._in_bounds, results)
        results = filter(self._passable, results)
 
        results = list(results)
        random.shuffle(results)

        return results

    def _in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.board.size[0] and 0 <= y < self.board.size[1]

    def _passable(self, id):
        return id not in self.visited and id not in self.board.walls