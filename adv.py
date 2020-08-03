from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


class Stack():
    def __init__(self):
        self.stack = []

    def __str__(self):
        return str(self.stack)

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


class Graph:
    def __init__(self):
        self.visited = {}
        self.reverse_path = Stack()
        self.reverse_directions = {
            'n': 's',
            'w': 'e',
            'e': 'w',
            's': 'n'
        }

    def add_room(self, room_id):
        self.visited[room_id] = {}

    def add_direction(self, room_id, direction, destination_room=None):
        if destination_room is None:
            destination_room = '?'
        self.visited[room_id][direction] = destination_room

    def get_unvisited_exits(self, room_id):
        unvisited = []
        exits = self.visited[room_id]

        for direction, exit in exits.items():
            if exit == '?':
                unvisited.append(direction)

        return unvisited

    def dft(self, direction=None, previous_room=None):
        # If we've visited all rooms, stop recursing
        if len(self.visited) == len(room_graph):
            return

        # If a direction was passed in
        if direction is not None:
            # Travel in that direction
            player.travel(direction)
            # Add the direction to the path
            traversal_path.append(direction)

            # Add the reverse direction to the reverse path
            self.reverse_path.push(self.reverse_directions[direction])

        # Get the current room
        current_room = player.current_room

        # If the current room was not visited
        if current_room.id not in self.visited:
            # Add the room to self.visited
            self.add_room(current_room.id)

            # Get the exits of the current room
            exits = current_room.get_exits()

            # Add the exits as edges in self.visited
            for exit in exits:
                self.add_direction(current_room.id, exit)

        # If we left a room
        if previous_room is not None:
            # Update the exit of the previous room to the current room
            self.add_direction(previous_room.id,
                               direction,
                               current_room.id)
            # Update the exit of the current room to the previous room
            self.add_direction(current_room.id,
                               self.reverse_directions[direction],
                               previous_room.id)

        # Get the unvisited exits of the current room
        unvisited_exits = self.get_unvisited_exits(current_room.id)

        # If there are unvisited exits
        if len(unvisited_exits) > 0:
            # Recurse through the unvisited exits
            for exit in unvisited_exits:
                self.dft(exit, current_room)

        # When there are no unvisited exits
        # Pop off the latest the reverse direction
        reverse_step = self.reverse_path.pop()

        # Move in that direction
        player.travel(reverse_step)

        # Append the step to the path
        traversal_path.append(reverse_step)


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

world_graph = Graph()
world_graph.dft()

# print(world_graph.visited)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
