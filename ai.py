# NAME(S): Joe Binette, Tyler Harwood
#
# APPROACH: [WRITE AN OVERVIEW OF YOUR APPROACH HERE.]
#     Please use multiple lines (< ~80-100 char) for you approach write-up.
#     Keep it readable. In other words, don't write
#     the whole damned thing on one super long line.
#
#     In-code comments DO NOT count as a description of
#     of your approach.

import random


class AI:
    def __init__(self):
        """
        Called once before the sim starts. You may use this function
        to initialize any data or data structures you need.
        """
        self.turn = 0

    def update(self, percepts):
        """
        PERCEPTS:
        Called each turn. Parameter "percepts" is a dictionary containing
        nine entries with the following keys: X, N, NE, E, SE, S, SW, W, NW.
        Each entry's value is a single character giving the contents of the
        map cell in that direction. X gives the contents of the cell the agent
        is in.

        COMAMND:
        This function must return one of the following commands as a string:
        N, E, S, W, U

        N moves the agent north on the map (i.e. up)
        E moves the agent east
        S moves the agent south
        W moves the agent west
        U uses/activates the contents of the cell if it is useable. For
        example, stairs (o, b, y, p) will not move the agent automatically
        to the corresponding hex. The agent must 'U' the cell once in it
        to be transported.

        The same goes for goal hexes (0, 1, 2, 3, 4, 5, 6, 7, 8, 9).
        """
        
        return random.choice(['N', 'S', 'E', 'W'])

# Class that bundles together coordinate pairs.
class Coordinates(object):
     def __init__(self, x: int, y: int):
         self.x: int = x # Horizontal coordinate
         self.y: int = y # Vertical coordinate

# Abstract class that is a parent to all tiles.
# Defines behavior for how they are displayed on the map.
class Tile(object):
    def __init__(self):
        self.tile_marker: str = "T" # tile_marker is the symbol that will be used when displayed on the map.
        
    def __str__(self):
        return self.tile_marker

# Fills in positions on the map that have not been seen, but are known to exist.
# Adjacent grass tiles become frontiers.
class Unknown_Tile(Tile):
    def __init__(self):
        self.tile_marker: str = "❔"

# Represents an area that the AI cannot walk on.
class Wall_Tile(Tile):
    def __init__(self):
        self.tile_marker: str = "⬛"
        
# A walkable map tile.
# Contains a visited properties to prevent remapping the same position.
class Grass_Tile(Tile):
    def __init__(self, visited=False):
        self.tile_marker: str = "⬜"
        self.visited: bool = visited
        
# A grass tile that is next to an unknown tile. The AI is compelled to navigate to them.
class Frontier_Tile(Grass_Tile):
    def __init__(self):
        self.tile_marker: str = "🟨"
        self.visited: bool = False
        
# The exit, and ultimate objective of the AI.
class Exit_Tile(Grass_Tile):
    def __init__(self):
        self.tile_marker: str = "🟥"
        self.visited: bool = False
        
class Map(object):
    def __init__(self):
        map_height: int = 1
        map_width: int = 1
        tile_map = [[]]
        robot_location: Coordinates = Coordinates(0, 0)
        frontier_tiles = []

    def expand_x(self, distance: int):
        for row in self.tile_map:
            if distance > 0:
                row += [Unknown_Tile()] * distance
            elif distance < 0:
                row = ([Unknown_Tile()] * abs(distance)) + row
                self.robot_location.x -= distance
        self.map_width += abs(distance)

    def expand_y(self, distance: int):
        new_space = []
        for i in range(abs(distance)):
            new_space.append([Unknown_Tile()] * self.map_width)
        if distance > 0:
            self.tile_map += new_space
        elif distance < 0:
            self.tile_map = new_space + self.tile_map
            self.robot_location.y -= distance
        self.map_height += abs(distance)
        
    def print_map(self):
        for y in self.tile_map:
            for x in y:
                print(x, end="")
            print()
                
    def scan(self, percepts):
        pass