"""
create robot vacuum that cleans all the floors of a grid.
main creates an instance of RoboVac (your code) and provides:
- grid size
- loc of robovac
- list of x,y,w,h tuples are instance of rectangluar blocks

goal: visit all tiles
exec will : create instance and in game loop call : nextMove()  ??
"""
import math
import numpy as np
from queue import PriorityQueue


class RoboVac:
    def __init__(self, config_list):
        self.room_width, self.room_height = config_list[0]
        self.room_state = np.zeros((self.room_height, self.room_width))
        self.pos = config_list[1]  # starting position of vacuum
        self.block_list = config_list[2]   # blocks list (x,y,width,ht)
        self.frontier_list = []  # our frontier
        self.explored = []  # tracking where we've been
        self.path = []
        self.furniture_coords = []

        # fill in with your info
        self.name = "James Castle"
        self.id = "29248132"

        # set start position in room
        y, x = self.pos
        self.room_state[x][y] = 1

        # generate goal state
        self.place_furniture()

        # generate starting frontier
        self.build_frontier()

    def place_furniture(self):
        """Method sets value for any furniture in the block list on the
        room_state board. Furniture weighted as 100.
        :return: void function
        """
        self.room_state.astype(int)
        for furniture in self.block_list:
            # get furniture dims
            x, y, width, height = furniture
            # set board pieces in range to 100 (blocked)
            for blocks in range(height):
                for cubes in range(width):
                    # range check for furniture that might be past wall
                    if(((y + blocks) < self.room_height) and
                            (x + cubes < self.room_width)):
                        self.room_state[y + blocks][x + cubes] = 100
                        self.furniture_coords.append((x + cubes,
                                                      y + blocks))

    def get_next_move(self, current_pos):  # called by PyGame code
        """
        Generates the next move for the RoboVac
        :param current_pos: tuple of ints (size 2) representing x, y
        coordinates.
        :return: Integer move choice between 0-3.
        """
        # Return a direction for the vacuum to move

        up = 0
        down = 2
        left = 3
        right = 1

        # check if frontier_list includes anything from blocklist
        if any(item in self.furniture_coords
               for item in self.frontier_list):
            print('ERROR: CORRUPT FRONTIER with furniture in it')

        # Generate our next move
        next_move_coordinate = (-1, -1)  # DEBUG

        # check to see if have a current path, and if not, make one.
        if(not self.path):  # path is empty
            next_move_path = self.next_move_manhat_coord(current_pos)
            self.path.append(next_move_path)

        current_path = self.path[0]

        # Check to see if the root of our path is at the current pos.
        # Pop if so, so next move will get us to a new location.
        if(current_path[0] == current_pos):
            current_path.pop(0)
        if(current_path):
            next_move_coord = current_path.pop(0)
            if(not current_path):
                self.path.pop()
        # subtract tuples from https://www.tutorialspoint.com/
        # how-to-get-subtraction-of-tuples-in-python
        pos_diff = tuple(map(lambda i, j: i - j,
                             next_move_coord, current_pos))

        # position diff will equal some next move (x, y) format
        if(pos_diff == (-1, 0)):
            next_move = left
        elif (pos_diff == (1, 0)):
            next_move = right
        elif (pos_diff == (0, -1)):
            next_move = up
        elif(pos_diff == (0, 1)):
            next_move = down
        else:
            print("ERROR in get_next_move: no move provided")

        # if not in explored list, then pop next_move_coordinate from
        # frontier_list.
        if(not next_move_coord in self.explored):
            frontier_idx = self.frontier_list.index(next_move_coord)
            self.frontier_list.pop(frontier_idx)
            self.explored.append(next_move_coord)

        # if not yet explored, add current pos to explored list
        if(current_pos not in self.explored):
            self.explored.append(current_pos)

        return next_move

    def next_move_manhat_coord(self, current_pos):
        """
        Generates our best move pathway using manhattan search heuristic
        :param current_pos: tuple of ints (size 2) representing x, y
        coordinates.
        :return: list of tuples (size 2, type int) representing x,y
        coordinates that form a path from our current location to the
        closest viable unexplored node.
        """
        viable_paths = PriorityQueue()
        max_viable_path_weight = math.inf
        stop_path_search = False

        # setup local frontier
        frontier_list = self.frontier_list

        # Create list of closest unvisited nodes in frontier
        frontier_dist = PriorityQueue()
        for fr_coords in frontier_list:
            manhattan_dist = self.manhattan_dist(current_pos, fr_coords)
            frontier_dist.put((manhattan_dist, fr_coords))

        # Build a list of all items in the PriorityQueue of lowest cost
        lowest_cost_dest = []
        all_low_cost = False
        if(frontier_dist.not_empty):
            item = frontier_dist.get()
            priority, coordinates = item
            lowest_cost_dest.append(coordinates)
            while((not frontier_dist.empty()) and
                  (all_low_cost == False)):
                next_item = frontier_dist.get()
                next_priority, next_coord = next_item
                if(next_priority == priority):
                    lowest_cost_dest.append(next_coord)
                else:
                    all_low_cost = True

        # Build paths to the lowest cost destination
        while(lowest_cost_dest):
            goal_node = lowest_cost_dest.pop(0)
            # queue = [[current_pos]]  # consider making priorityqueue
            path_queue = PriorityQueue()
            path_queue.put((0, [current_pos]))

            # make a queue, build path, until you get to goal
            while((not path_queue.empty()) and (not stop_path_search)):
                weight, path = path_queue.get()
                vertex = path[len(path) - 1]
                # get child nodes
                child_nodes = self.get_child_nodes(vertex)
                child_priority = PriorityQueue()

                # Put children in PriorityQueue
                for node in child_nodes:
                    node_priority = self.manhattan_dist(node, goal_node)
                    child_priority.put((node_priority, node))

                min_priority = math.inf
                # check if child node is goal node
                while(not child_priority.empty()):
                    alt_path = path
                    priority, node = child_priority.get()
                    if(node == goal_node):
                        manhattan_sum = 0
                        path = (path + [node])
                        # if yes, get path cost + add to priorityQueue
                        for item in path:
                            dist = self.manhattan_dist(item, goal_node)
                            manhattan_sum += dist
                        if(manhattan_sum <= max_viable_path_weight):
                            viable_paths.put((manhattan_sum, path))
                            max_viable_path_weight = manhattan_sum
                        else:
                            stop_path_search = True
                        break
                    else:
                        alt_path = alt_path + [node]
                        manhattan_sum = 0
                        # check for duplicate vaLues in path using set.
                        set_len = len(set(alt_path))
                        if ((len(alt_path)) == set_len):
                            for item in alt_path:
                                dist = self.manhattan_dist(item,
                                                           goal_node)
                                manhattan_sum += dist
                            if(manhattan_sum <= min_priority):
                                if(not viable_paths.empty()):
                                    if(manhattan_sum <
                                            max_viable_path_weight):
                                        min_priority = manhattan_sum
                                        path_queue.put((manhattan_sum,
                                                        alt_path))
                                else:
                                    min_priority = manhattan_sum
                                    path_queue.put(
                                        (manhattan_sum, alt_path))

        # find path with lowest sum (cost)
        cost, lowest_path = viable_paths.get()

        # return lowest cost path
        return lowest_path

    def get_child_nodes(self, start_node):
        """
        Generate a list of child node coordinates based on a given start
        node.
        :param start_node: tuple of 2 ints indicating row,col coords of
        a start note
        :return: a list of tuples for all legal moves.
        """
        up = 0
        down = 2
        left = 3
        right = 1
        child_nodes = []
        # check for legal moves
        legal_moves = self.legal_move_check(start_node)
        start_x, start_y = start_node

        for move in legal_moves:
            # case if up
            if(move == up):
                up_coor = (start_x, (start_y - 1))
                child_nodes.append(up_coor)
            # case if down
            elif(move == down):
                down_coor = (start_x, (start_y + 1))
                child_nodes.append(down_coor)
            # case if left
            elif(move == left):
                left_coor = ((start_x - 1), (start_y))
                child_nodes.append(left_coor)
            # case if right
            elif(move == right):
                right_coor = ((start_x + 1), start_y)
                child_nodes.append(right_coor)
            else:
                print('ERROR: NO LEGAL MOVES!')

        # return list of child nodes
        return child_nodes

    def manhattan_dist(self, current_pos, dest_pos):
        """
        This function calculates the Manhattan Sum based on where we are
        and where we want to go
        :param current_pos: tuple of ints (size 2) representing x, y
        coordinates.
        :param dest_pos: tuple of ints (size 2) representing x, y
        coordinates.
        :return: int representing manhattan distance of the destination
        and current position coordinates.
        """
        manhattan_dist = 0
        curr_x, curr_y = current_pos
        dest_x, dest_y = dest_pos
        if(self.room_state[dest_y][dest_x] == 100):
            manhattan_dist = 100
        else:
            manhattan_dist = (abs(dest_y - curr_y) +
                              abs(dest_x - curr_x))

        return manhattan_dist

    def build_frontier(self):
        """
        Looks at all elements in the starting array that arent blocks
        and builds a frontier list of all unvisited nodes to pop from.
        :return: void method
        """
        room_start = self.room_state

        # get coordinates of all elements in the array whose value is 0.
        # coordinates in row, col format.

        for row_idx, row in enumerate(room_start):
            for col_idx, col in enumerate(row):
                if (col == 0):
                    self.frontier_list.append((col_idx, row_idx))

    def legal_move_check(self, current_pos):
        """
        Check for valid moves.
        :param current_pos: tuple consisting of x,y coordinate position
        of robot.
        :return: a list of legal moves
        """
        legal_moves = []
        x, y = current_pos

        # check for board bounds. NOTE room_state is [row][col] format.
        # Check left
        if((x - 1) >= 0):  # hitting wall?
            if (self.room_state[y][x - 1] != 100):  # hitting furniture?
                legal_moves.append(3)  # add left to legal moves
                # self.room_state[y][x -1] = 55 # test
        # Check right
        if ((x + 1) <= (self.room_width - 1)):  # hitting wall?
            if(self.room_state[y][x + 1] != 100):  # hitting furniture?
                legal_moves.append(1)  # add right to legal moves
                # self.room_state[y][x + 1] = 66  # test
        # check up
        if ((y - 1) >= 0):  # hitting wall?
            if(self.room_state[y - 1][x] != 100):  # hitting furniture?
                legal_moves.append(0)  # add up to legal moves
                # self.room_state[y - 1][x] = 77  # test
        # check down
        if ((y + 1) <= (self.room_height - 1)):  # hitting wall?
            if(self.room_state[y + 1][x] != 100):  # hitting furniture?
                legal_moves.append(2)  # add down to legal moves
                # self.room_state[y + 1][x] = 88  # test

        return legal_moves
