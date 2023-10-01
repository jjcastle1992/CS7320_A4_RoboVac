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
import copy
from collections import defaultdict

class RoboVac:
    def __init__(self, config_list, clean_set):
        self.room_width, self.room_height = config_list[0]
        self.room_state = np.zeros((self.room_height, self.room_width))
        self.goal_state = np.ones((self.room_height, self.room_width))
        self.pos = config_list[1]  # starting position of vacuum
        self.block_list = config_list[2]   # blocks list (x,y,width,ht)
        self.explored_list = clean_set
        self.frontier_list = []  # our frontier
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
        self.pos = current_pos
        # next_move = self.next_move_manhat(self.room_state)

        next_move_path = self.next_move_manhat_coord(current_pos)
        next_move_coord = next_move_path.pop(1)   # 1 = next move
        pos_diff = current_pos - next_move_coord  # row, col

        # position diff will equal some next move (0, 1) = up
        if(pos_diff == (0, 1)):
            next_move = up
        print('woot')

        return next_move


    def next_move_manhat_coord(self, current_pos):

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
            while(frontier_dist.not_empty and all_low_cost == False):
                next_item = frontier_dist.get()
                next_priority, next_coord = next_item
                if(next_priority == priority):
                    lowest_cost_dest.append(next_coord)
                else:
                    all_low_cost = True

        # what's the path to get to the lowest cost items?
        while(lowest_cost_dest):
            goal_node = lowest_cost_dest.pop(0)
            queue = [[current_pos]]

            # make a queue, build path, until you get to destination(goal)
            while(queue):
                path = queue.pop(0)
                vertex = path[len(path) - 1]
                # get child nodes
                child_nodes = self.get_child_nodes(vertex)
                print('child nodes generated')

                # check if child node is goal node
                    # if yes, return path + current coords
                    # else, append path + current_coords to queue


        # find path with lowest sum (cost)

        # return first move in that path

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
        start_row, start_col = start_node

        for move in legal_moves:
            # case if up
            if(move == up):
                up_coor = ((start_row - 1), start_col)
                child_nodes.append(up_coor)
            # case if down
            elif(move == down):
                down_coor = ((start_row + 1), start_col)
                child_nodes.append(down_coor)
            # case if left
            elif(move == left):
                left_coor = (start_row, (start_col - 1))
                child_nodes.append(left_coor)
            # case if right
            elif(move == right):
                right_coor = (start_row, (start_col + 1))
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

        curr_row, curr_col = current_pos
        dest_row, dest_col = dest_pos

        manhattan_dist = (abs(dest_row - curr_row) + abs(dest_col -
                                                         curr_col))

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
                    self.frontier_list.append((row_idx, col_idx))

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
        # check for board bounds
        # Check left
        if((x - 1) >= 0):  # hitting wall?
            if (self.room_state[x - 1][y] != 100):  # hitting furniture?
                legal_moves.append(3)  # add left to legal moves

        # Check right
        if ((x + 1) <= (self.room_width - 1)):  # hitting wall?
            if(self.room_state[x + 1][y] != 100):  # hitting furniture?
                legal_moves.append(1)  # add right to legal moves
        # check up
        if ((y - 1) >= 0):  # hitting wall?
            if(self.room_state[x][y - 1] != 100):  # hitting furniture?
                legal_moves.append(0)  # add up to legal moves
        # check down
        if ((y + 1) <= (self.room_height - 1)):  # hitting wall?
            if(self.room_state[x][y + 1] != 100):  # hitting furniture?
                legal_moves.append(2)  # add down to legal moves

        return legal_moves
