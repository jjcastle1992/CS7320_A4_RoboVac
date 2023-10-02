'''
create robot vacuum that cleans all the floors of a grid.
main creates an instance of RoboVac (your code) and provides:
- grid size
- loc of robovac
- list of x,y,w,h tuples are instance of rectangluar blocks

goal: visit all tiles
exec will : create instance and in game loop call : nextMove()  ??
'''
import random
import math
import numpy as np
from queue import PriorityQueue

class RoboVac:
    def __init__(self, config_list):
        self.room_width, self.room_height = config_list[0]
        self.room_state = np.zeros((self.room_height, self.room_width))
        self.goal_state = np.ones((self.room_height, self.room_width))
        self.pos = config_list[1]  # starting position of vacuum
        self.block_list = config_list[2]   # blocks list (x,y,width,ht)
        self.frontier_list = []  # our frontier
        self.explored = []  # testing purposes
        self.start_corner_found = False
        self.last_move = None
        self.move_list = []
        self.path = []


        # # test purposes - highlight robot position
        y, x = self.pos
        self.room_state[x][y] = 1


        # fill in with your info
        self.name = "James Castle"
        self.id = "29248132"

        # generate goal state
        self.place_furniture()

        # generate starting frontier
        self.build_frontier()

    def place_furniture(self):
        """Method sets value for any furniture in the block list on the
        room_state and goal_state boards. Furniture weighted as 100.
        :return: void function
        """
        self.room_state.astype(int)
        for furniture in self.block_list:
            # get furniture dims
            x, y, width, height = furniture
            # set board pieces in range to 100 (blocked)
            self.room_state[x][y] = 100
            for blocks in range(width):
                for cubes in range(height):
                    self.room_state[x + cubes][y + blocks] = 100

        self.goal_state.astype(int)
        for furniture in self.block_list:
            # get furniture dims
            x, y, width, height = furniture
            # set board pieces in range to 100 (blocked)
            self.goal_state[x][y] = 100
            for blocks in range(width):
                for cubes in range(height):
                    self.goal_state[x + cubes][y + blocks] = 100

        print('Furniture placed')

    def get_next_move(self, current_pos):  # called by PyGame code
        # Return a direction for the vacuum to move
        # random walk 0=north # 1=east 2=south 3=west

        up = 0
        down = 2
        left = 3
        right = 1

 # **** NEED TO FIX (X, Y) INTERP (Current I'm looking for (R, C), but needs to be written for X, Y)
        # next_move = self.next_move_manhat(self.room_state)

        next_move_path = self.next_move_manhat_coord(current_pos)
        next_move_coord = next_move_path.pop(1)   # 1 = next move
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
        # frontier_list
        if(not next_move_coord in self.explored):
            frontier_idx = self.frontier_list.index(next_move_coord)
            self.frontier_list.pop(frontier_idx)
            self.explored.append(next_move_coord)
        if(current_pos not in self.explored):
            self.explored.append(current_pos)

        return next_move


    def next_move_manhat_coord(self, current_pos):
        viable_paths = PriorityQueue()
        # where we are

        # what is our frontier
        frontier_list = self.frontier_list

        # what's the closest unvisited node in frontier?
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

        # what's the path to get to the lowest cost items?
        while(lowest_cost_dest):
            goal_node = lowest_cost_dest.pop(0)
            # queue = [[current_pos]]  # consider making priorityqueue
            path_queue = PriorityQueue()
            path_queue.put((0, [current_pos]))

            # make a queue, build path, until you get to destination(goal)
            while(not path_queue.empty()):
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
                        viable_paths.put((manhattan_sum, path))
                        break
                    else:
                        # put logic in to only include paths with low min sums
                        alt_path = alt_path + [node]
                        manhattan_sum = 0
                        for item in alt_path:
                            dist = self.manhattan_dist(item, goal_node)
                            manhattan_sum += dist
                        if(manhattan_sum < min_priority):
                            min_priority = manhattan_sum
                            path_queue.put((manhattan_sum, alt_path))



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
        """

        curr_x, curr_y = current_pos
        dest_x, dest_y = dest_pos

        manhattan_dist = (abs(dest_y - curr_y) + abs(dest_x - curr_x))

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
                    self.frontier_list.append((col_idx, row_idx)) # x, y

    def visited_before(self, current_position, legal_moves):
        """
        Checks to see which legal moves result in re-tracing of steps
        :param current_position:
        :param legal_moves:
        :return: A list of moves that result in step retracing.
        """
        x, y = current_position
        up = (x, y - 1)
        down = (x, y + 1)
        left = (x - 1, y)
        right = (x + 1, y)
        repeat_moves = []
        if(0 in legal_moves):  # check if Up has been visited
            if(up in self.explored_list):
                repeat_moves.append(0)
        if(2 in legal_moves):  # check if Down has been visited
            if(down in self.explored_list):
                repeat_moves.append(2)
        if(3 in legal_moves):  # check if Left has been visited
            if(left in self.explored_list):
                repeat_moves.append(3)
        if(1 in legal_moves):  # check if Right has been visited
            if(right in self.explored_list):
                repeat_moves.append(1)

        return repeat_moves

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
            # if (self.room_state[y][x - 1] != 100):  # hitting furniture?
            legal_moves.append(3)  # add left to legal moves
        # Check right
        if ((x + 1) <= (self.room_width - 1)):  # hitting wall?
            # if(self.room_state[y][x + 1] != 100):  # hitting furniture?
            legal_moves.append(1)  # add right to legal moves
        # check up
        if ((y - 1) >= 0):  # hitting wall?
            # if(self.room_state[y - 1][x] != 100):  # hitting furniture?
            legal_moves.append(0)  # add up to legal moves
        # check down
        if ((y + 1) <= (self.room_height - 1)):  # hitting wall?
            # if(self.room_state[y + 1][x] != 100):  # hitting furniture?
            legal_moves.append(2)  # add down to legal moves

        return legal_moves
