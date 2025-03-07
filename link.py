# link.py
#
# The code that defines the behaviour of Link.
#
# You should be able to write the code for a simple solution to the
# game version of the Wumpus World here, getting information about the
# game state from self.gameWorld, and using makeMove() to generate the
# next move.
#
# Written by: Simon Parsons
# Last Modified: 25/08/20

import world
import random
import utils
from utils import Directions

class Link():

    def __init__(self, dungeon):
        # Make a copy of the world an attribute, so that Link can
        # query the state of the world
        self.gameWorld = dungeon

        # What moves are possible.
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]

        # Initialize DFS attributes
        self.visited = set()  # To track visited cells
        self.stack = []       # To implement DFS
        self.path = []        # To store the current path

    def makeMove(self):
        # Get Link's current position
        myPosition = self.gameWorld.getLinkLocation()

        # Get the location of the gold
        allGold = self.gameWorld.getGoldLocation()
        if len(allGold) == 0:
            return Directions.STAY  # No gold left to find

        nextGold = allGold[0]
        goldPosition = (nextGold.x, nextGold.y)

        # If gold is found, stop
        if (myPosition.x, myPosition.y) == goldPosition:
            return Directions.STAY

        # Initialize stack and visited set on first move
        if not self.stack:
            self.stack.append((myPosition.x, myPosition.y))
            self.path = []

        # Perform DFS
        while self.stack:
            current = self.stack.pop()
            if current == goldPosition:
                # Move along the path
                if self.path:
                    next_move = self.path[0]
                    self.path = self.path[1:]  # Remove the move from the path
                    return self.getDirection((myPosition.x, myPosition.y), next_move)
                return Directions.STAY

            if current not in self.visited:
                self.visited.add(current)
                # Get valid neighbors
                neighbors = self.getNeighbors(current)
                for neighbor in neighbors:
                    if self.isSafe(neighbor):
                        self.stack.append(neighbor)
                        self.path.append(neighbor)

        # If no path is found, stay in place
        return Directions.STAY

    def getNeighbors(self, position):
        x, y = position
        neighbors = []
        # Check all four directions
        if x > 0:
            neighbors.append((x - 1, y))  # WEST
        if x < self.gameWorld.getWidth() - 1:
            neighbors.append((x + 1, y))  # EAST
        if y > 0:
            neighbors.append((x, y - 1))  # SOUTH
        if y < self.gameWorld.getHeight() - 1:
            neighbors.append((x, y + 1))  # NORTH
        return neighbors

    def isSafe(self, position):
        # Check if the position is safe (no pit or Wumpus)
        x, y = position
        return not self.gameWorld.isPit(x, y) and not self.gameWorld.isWumpus(x, y)

    def getDirection(self, current, next):
        # Determine the direction to move
        cx, cy = current
        nx, ny = next
        if nx > cx:
            return Directions.EAST
        if nx < cx:
            return Directions.WEST
        if ny > cy:
            return Directions.NORTH
        if ny < cy:
            return Directions.SOUTH
        return Directions.STAY