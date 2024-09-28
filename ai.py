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


    def a_star(self, start, goal):
        """
        a_star for pathfinding to next frontier node.
        To prevent situations where we end up in a corner

        We will use manhattan distance as our heuristic
        """
        def calc_dir(coordinates):
            """
            This computes the direction of a coordinate
            vector relative to current position. 
            For use in A* to save the path.
            """
            x = coordinates[0]
            y = coordinates[1]
            dir = {
                    (1, 0): "E",
                    (-1, 0): "W",
                    (0, 1): "N",
                    (0, -1): "S",
                    (0, 0): "U"
            }
            #Compute the sign, then feed those into the dict
            return dir.get((x > 0) - (x < 0), (y > 0) - (y < 0))

        def manhattan_dist(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        path = []
        known = set()

        current_score = {start: 0}
        estimate_score = {start: manhattan_dist(start, goal)}

        path.append()
        while len(known) != 0:
            pos = path.pop()
            if current == goal:
                return path
            #for



    def set_current_visited(self):
        """
        sets the current tile to visited
        Solely just to cut down on spaghetti
        """
        self.ai_map.set_current_visited()

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

        #If it finds the goal immediately use the current tile.
        if percepts["X"][0] == 'r':
            return 'U'
        
        #Search frontier for closest node
        self.set_current_visited()

        #current location
        loc = self.ai_map.robot_location.pair()

        #expand frontier
        for tile_coordinates in self.ai_map.get_neighbors(loc):
            tile_x = tile_coordinates[0]
            tile_y = tile_coordinates[1]
            tile = self.ai_map.tile_map[tile_x][tile_y]
            if isinstance(tile, Grass_Tile) and tile.visited == False:
                self.ai_map.frontier_tiles.append(tile_coordinates)


        init_tile = self.ai_map.frontier_tiles[0]
        path = self.astar(loc, init_tile)
        for target in self.ai_map.frontier_tiles:
            newpath = self.astar(loc, target)
            if len(newpath) < len(path):
                path = newpath



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
    def pair(self):
        return (self.x, self.y)

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
        
class Map(object):
    def __init__(self):
        self.map_height: int = 1
        self.map_width: int = 1
        self.tile_map = [[Grass_Tile()]]
        self.robot_location: Coordinates = Coordinates(0, 0)
        self.frontier_tiles = []

    #This might break, this object system does not make things easy
    def set_current_visited(self):
        self.tile_map[self.robot_location.x][self.robot_location.y].visited = True

    def get_neighbors(self, coordinates):
        x, y = coordinates
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.map_width and 0 <= ny < self.map_height:
                neighbor_tile = self.tile_map[ny][nx]
                if isinstance(neighbor_tile, Grass_Tile) and not neighbor_tile.visited:
                    neighbors.append((nx, ny))
        return neighbors

    def expand_x(self, distance: int):
        for index, row in enumerate(self.tile_map):
            if distance > 0:
                self.tile_map[index] = row + ([Unknown_Tile()] * distance)
            elif distance < 0:
                self.tile_map[index] = ([Unknown_Tile()] * abs(distance)) + row
        if distance < 0:
            self.robot_location.x += abs(distance)
        self.map_width += abs(distance)

    def expand_y(self, distance: int):
        new_space = []
        for i in range(abs(distance)):
            new_space.append([Unknown_Tile()] * self.map_width)
        if distance > 0:
            self.tile_map += new_space
        elif distance < 0:
            self.tile_map = new_space + self.tile_map
            self.robot_location.y += abs(distance)
        self.map_height += abs(distance)
        
    def print_map(self):
        for y in self.tile_map:
            for x in y:
                print(x, end="")
            print()
            
    def charToTile(self, character):
        if character == "g":
            return Grass_Tile()
        elif character == "w":
            return Wall_Tile()
        elif character == "r":
            return Exit_Tile()
                
    def scan(self, percepts):
        robot_x = self.robot_location.x
        robot_y = self.robot_location.y
        self.tile_map[robot_y][robot_x] = self.charToTile(percepts["X"][0])
        north_distance = robot_y
        east_distance = (self.map_width - 1) - robot_x
        south_distance = (self.map_height - 1) - robot_y
        west_distance = robot_x
        if len(percepts["N"]) > north_distance:
            self.expand_y(north_distance - len(percepts["N"]))
        tile_placement_offset = 0
        for i in percepts["N"]:
            tile_placement_offset -= 1
            if isinstance(self.tile_map[self.robot_location.y + tile_placement_offset][self.robot_location.x], Unknown_Tile):
                self.tile_map[self.robot_location.y + tile_placement_offset][self.robot_location.x] = self.charToTile(i)
        if len(percepts["E"]) > east_distance:
            self.expand_x(len(percepts["E"]) - east_distance)
        tile_placement_offset = 0
        for i in percepts["E"]:
            tile_placement_offset += 1
            if isinstance(self.tile_map[self.robot_location.y][self.robot_location.x + tile_placement_offset], Unknown_Tile):
                self.tile_map[self.robot_location.y][self.robot_location.x + tile_placement_offset] = self.charToTile(i)
        if len(percepts["S"]) > south_distance:
            self.expand_y(len(percepts["S"]) - south_distance)
        tile_placement_offset = 0
        for i in percepts["S"]:
            tile_placement_offset += 1
            if isinstance(self.tile_map[self.robot_location.y + tile_placement_offset][self.robot_location.x], Unknown_Tile):
                self.tile_map[self.robot_location.y + tile_placement_offset][self.robot_location.x] = self.charToTile(i)
        if len(percepts["W"]) > west_distance:
            self.expand_x(west_distance - len(percepts["W"]))
        tile_placement_offset = 0
        for i in percepts["W"]:
            tile_placement_offset -= 1
            if isinstance(self.tile_map[self.robot_location.y][self.robot_location.x + tile_placement_offset], Unknown_Tile):
                self.tile_map[self.robot_location.y][self.robot_location.x + tile_placement_offset] = self.charToTile(i)