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
        self.ai_map = Map()
        self.test_path = ["E", "E", "S", "S"][::-1]

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
        self.ai_map.scan(percepts)
        self.ai_map.print_map()
        d = self.test_path.pop()
        if d == "N":
            self.ai_map.robot_location.y -= 1
        elif d == "E":
            self.ai_map.robot_location.x += 1
        elif d == "S":
            self.ai_map.robot_location.y += 1
        elif d == "W":
            self.ai_map.robot_location.x -= 1
        return d

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
        self.tile_marker: str = "?"
        #❔

# Represents an area that the AI cannot walk on.
class Wall_Tile(Tile):
    def __init__(self):
        self.tile_marker: str = "w"
        #⬛
        
# A walkable map tile.
# Contains a visited properties to prevent remapping the same position.
class Grass_Tile(Tile):
    def __init__(self, visited=False):
        self.tile_marker: str = "g"
        self.visited: bool = visited
        #⬜
        
# A grass tile that is next to an unknown tile. The AI is compelled to navigate to them.
class Frontier_Tile(Grass_Tile):
    def __init__(self):
        self.tile_marker: str = "f"
        self.visited: bool = False
        #🟨
        
# The exit, and ultimate objective of the AI.
class Exit_Tile(Grass_Tile):
    def __init__(self):
        self.tile_marker: str = "r"
        self.visited: bool = False
        #🟥
        
# Keeps track of where everything is.
# Expands and changes based on the AI's discoveries.
class Map(object):
    def __init__(self):
        self.map_height: int = 1
        self.map_width: int = 1
        self.tile_map = [[Grass_Tile()]] # This is the 2D array that stores the bulk of mapping information.
        self.robot_location: Coordinates = Coordinates(0, 0) # Keeps track of the AI's position.
        self.frontier_tiles = [] # Keeps track of tiles that may lead to new space being mapped.

	# Expands self.tile_map along the x axis in either direction.
    # Negative values expand West, positive values expand East.
    def expand_x(self, distance: int):
        for index, row in enumerate(self.tile_map):
            # Case for postive values. Expands the map East by {distance} tiles.
            if distance > 0:
                self.tile_map[index] = row + ([Unknown_Tile()] * distance)
            # Case for negative values. Expands the map West by {distance} tiles.
            elif distance < 0:
                self.tile_map[index] = ([Unknown_Tile()] * abs(distance)) + row
        # Corrects the robot's position if the map was expanded on the West.
        if distance < 0:
            self.robot_location.x += abs(distance)
        self.map_width += abs(distance)

	# Expands self.tile_map along the y axis in either direction.
    # Negative values expand North, positve values expand South.
    def expand_y(self, distance: int):
        new_space = []
        # Prepares the tiles that will be added to the map.
        for i in range(abs(distance)):
            new_space.append([Unknown_Tile()] * self.map_width)
        # Adds tiles at the south if distance is positive.
        if distance > 0:
            self.tile_map += new_space
        # Adds tiles at the north if distance is negative.
        elif distance < 0:
            self.tile_map = new_space + self.tile_map
            # Corrects the robots position if map was expanded north.
            self.robot_location.y += abs(distance)
        self.map_height += abs(distance)
    
	# Prints the map in an easy to read format.
    def print_map(self):
        for y in self.tile_map:
            for x in y:
                print(x, end="")
            print()
            
	# Returns a new tile based on characters found in the percepts.
    def charToTile(self, character):
        if character == "g":
            return Grass_Tile()
        elif character == "w":
            return Wall_Tile()
        elif character == "r":
            return Exit_Tile()
    
	# Adds newly discovered tiles to the map. This one's a whopper.
    def scan(self, percepts):
        robot_x = self.robot_location.x
        robot_y = self.robot_location.y
        self.tile_map[robot_y][robot_x] = self.charToTile(percepts["X"][0])
        # x_distance are the distance from where the robot is to the edge of the map.
        north_distance = robot_y
        east_distance = (self.map_width - 1) - robot_x
        south_distance = (self.map_height - 1) - robot_y
        west_distance = robot_x
        # Checks if expanding North is necessary, and expands if needed.
        if len(percepts["N"]) > north_distance:
            self.expand_y(north_distance - len(percepts["N"]))
        # Places tiles in a row starting from the robot's position.
        tile_placement_offset = 0
        for i in percepts["N"]:
            tile_placement_offset -= 1
            if isinstance(self.tile_map[self.robot_location.y + tile_placement_offset][self.robot_location.x], Unknown_Tile):
                self.tile_map[self.robot_location.y + tile_placement_offset][self.robot_location.x] = self.charToTile(i)
        # Checks if expanding East is necessary, and expands if needed.
        if len(percepts["E"]) > east_distance:
            self.expand_x(len(percepts["E"]) - east_distance)
        # Places tiles in a row starting from the robot's position.
        tile_placement_offset = 0
        for i in percepts["E"]:
            tile_placement_offset += 1
            if isinstance(self.tile_map[self.robot_location.y][self.robot_location.x + tile_placement_offset], Unknown_Tile):
                self.tile_map[self.robot_location.y][self.robot_location.x + tile_placement_offset] = self.charToTile(i)
        # Checks if expanding South is necessary, and expands if needed.
        if len(percepts["S"]) > south_distance:
            self.expand_y(len(percepts["S"]) - south_distance)
        # Places tiles in a row starting from the robot's position.
        tile_placement_offset = 0
        for i in percepts["S"]:
            tile_placement_offset += 1
            if isinstance(self.tile_map[self.robot_location.y + tile_placement_offset][self.robot_location.x], Unknown_Tile):
                self.tile_map[self.robot_location.y + tile_placement_offset][self.robot_location.x] = self.charToTile(i)
        # Checks if expanding West is necessary, and expands if needed.
        if len(percepts["W"]) > west_distance:
            self.expand_x(west_distance - len(percepts["W"]))
        # Places tiles in a row starting from the robot's position.
        tile_placement_offset = 0
        for i in percepts["W"]:
            tile_placement_offset -= 1
            if isinstance(self.tile_map[self.robot_location.y][self.robot_location.x + tile_placement_offset], Unknown_Tile):
                self.tile_map[self.robot_location.y][self.robot_location.x + tile_placement_offset] = self.charToTile(i)