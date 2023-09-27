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

class RoboVac:
    def __init__(self, config_list, clean_set):
        self.room_width, self.room_height = config_list[0]
        self.room_state = np.zeros((self.room_height, self.room_width))
        self.goal_state = np.ones((self.room_height, self.room_width))
        self.pos = config_list[1]  # starting position of vacuum
        self.block_list = config_list[2]   # blocks list (x,y,width,ht)
        self.explored_list = clean_set
        self.unvisited_list = []
        self.start_corner_found = False
        self.last_move = None


        # test purposes - highlight robot position
        y, x = self.pos
        self.room_state[x][y] = 99


        # fill in with your info
        self.name = "James Castle"
        self.id = "29248132"

        # generate goal state
        self.place_furniture()

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

        move_list = self.next_move_manhat(self.room_state)
        next_move = 0


        return next_move



    def next_move_manhat(self, board):
        """
        Method returns ordered list of cleaning steps as a list of
        boards.
        :param board: 2d list of ints containing current game board
        :return: list of game moves to cleaned room.
        """
        possible_moves = PriorityQueue()

        queue = [[board]]

        # Kick off BFS (Manhattan)
        while queue:
            path = queue.pop(0)
            vertex = path[len(path) - 1]

            child_boards = self.get_child_boards_list(vertex, self.pos)

            # need to figure out how best to unpack tuples into a list

            next_node_list = [x for x in child_boards[str(vertex)]
                              if str(x) not in set(str(path))]

            # Create Manhattan Distance Priority Queue
            for node in next_node_list:
                manhattan_sum = self.manhattan_dist(node,
                                                    self.goal_state)
                possible_moves.put((manhattan_sum, node))

            # Visit the Children in our Priority Queue
            while not (possible_moves.empty()):
                priority, next_node = possible_moves.get()

                # Check for victory conditions or append path with node
                if next_node == self.goal_state:
                    return [path + [next_node]]
                else:
                    queue.append(path + [next_node])

    def manhattan_dist(self, board, goal):
        """
        This function calculates the Manhattan Sum for a given board
        based on the variance in tile distance of the current board vs
        the goal board.
        :param board: 2d list of ints containing the board to give a
        Manhattan sum.
        :param goal: 2d list of ints containing goal state game board
        :return: float that is the sum of all Manhattan distances for
        the target board vs goal board
        """
        manhattan_sum = 0.0
        # customizing in-case goal board is not 1, 2, 3, 4...etc.

        # Calculate our Manhattan Sum
        for row_idx, row in enumerate(goal):
            for col_idx, element in enumerate(row):
                current_target = goal[row_idx][col_idx]
                board_coord, goal_coord = self.coordinate_finder(
                    current_target,
                    board, goal)
                x1, y1 = board_coord
                x2, y2 = goal_coord
                manhattan_dist = (abs(x1 - x2) + abs(y1 - y2))
                manhattan_sum += manhattan_dist

        return manhattan_sum

    def coordinate_finder(self, target_val, current_board, goal_board):
        """
        Finds coordinates of a target value (int) in 2 boards:
            1. Current Board
            2. Goal Board
        :param target_val: int to search for in the current and goal boards
        :param current_board: 2d list of ints containing the current board
        :param goal_board: 2d list of ints containing the goal board
        :return: tuple containing 2 ints
        """
        current_board_coords = (-1, -1)
        goal_board_coords = (-1, -1)

        # find current board coordinates for the target value
        for row_idx, row in enumerate(current_board):
            for col_idx, element in enumerate(row):
                if element == target_val:
                    current_board_coords = (row_idx, col_idx)

        # find goal board coordinates for the target value
        for row_idx, row in enumerate(goal_board):
            for col_idx, element in enumerate(row):
                if element == target_val:
                    goal_board_coords = (row_idx, col_idx)

        return current_board_coords, goal_board_coords

    def get_child_boards_list(self, board, current_pos):
        """
        This function gets ALL child boards for a given parent board
        :param board: 2d list of ints - A game board (RxC) matrix
        :param current_pos: tuple consisting of x,y coordinate position
        of robot.
        :return: A list of ALL possible child boards of the parent
        """

        list_of_child_boards = {}
        up = 0
        down = 2
        left = 3
        right = 1
        col, row = current_pos

        # determine if we can move up (Zero not in bottom Row)
        up_board = copy.deepcopy(board)

        # not 1 move up away from a block (edge of board or furniture)
        legal_moves = self.legal_move_check(current_pos)
        if(up in legal_moves):
            up_board[row - 1][col] = 1
            up_tup = (up_board, up)  # to return move with board
            # add up_board to the list of children
            if str(board) in list_of_child_boards.keys():
                list_of_child_boards[str(board)].append(up_tup)
            else:
                list_of_child_boards[str(board)] = up_tup

        # determine if we can move down (Zero not in top row)
        down_board = copy.deepcopy(board)
        if(down in legal_moves):
            down_board[row + 1][col] = 1
            down_tup = (down_board, down)
            # add down_board to the list of children
            if str(board) in list_of_child_boards.keys():
                list_of_child_boards[str(board)].append(down_tup)
            else:
                list_of_child_boards[str(board)] = down_tup

        # determine if we can move left (Zero cannot be in last column)
        left_board = copy.deepcopy(board)
        if(left in legal_moves):
            left_board[row][col - 1] = 1
            left_tup = (left_board, left)
            # add left_board to the list of children
            if str(board) in list_of_child_boards.keys():
                list_of_child_boards[str(board)].append(left_tup)
            else:
                list_of_child_boards[str(board)] = left_tup

        # determine if we can move right (Zero cannot be in first column)
        right_board = copy.deepcopy(board)
        if(right in legal_moves):
            right_board[row][col + 1] = 1
            right_tup = (right_board, right)
            # add right_board to the list of children
            if str(board) in list_of_child_boards.keys():
                list_of_child_boards[str(board)].append(right_tup)
            else:
                list_of_child_boards[str(board)] = right_tup

        return list_of_child_boards

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
            if(self.room_state[x][y + 1] != 100):  # hitting furniture?
                legal_moves.append(0)  # add up to legal moves
        # check down
        if ((y + 1) <= (self.room_height - 1)):  # hitting wall?
            if(self.room_state[x + 1][y] != 100):  # hitting furniture?
                legal_moves.append(2)  # add down to legal moves

        return legal_moves

    def at_corner(self, current_pos):
        """
        Determines if we are at a corner
        :param current_pos: tuple consisting of x,y coordinate position
        of robot.
        :return: bool in_corner. True if already in a corner. False if
        not.
        """
        in_corner = False
        # Possible Corners (x, y)
        top_left = (0, 0)
        top_right = (self.room_width - 1, 0)
        bot_left = (0, self.room_height - 1)
        bot_right = (self.room_width - 1, self.room_height - 1)
        corner_list = [top_left, top_right, bot_left, bot_right]
        for corners in corner_list:
            if corners == current_pos:
                in_corner = True

        return in_corner

    def find_corner(self, current_pos):
        """
        Finds nearest corner when we're not in already in the corner.
        :param current_pos: tuple consisting of x,y coordinate position
        of robot.
        :return: next move
        """

        # Possible Corners (x, y)
        top_left = (0, 0)
        top_right = (self.room_width - 1, 0)
        bot_left = (0, self.room_height - 1)
        bot_right = (self.room_width - 1, self.room_height - 1)
        corner_list = [top_left, top_right, bot_left, bot_right]

        # Use Euclidean Distance to determine nearest corner
        # Corner - Position
        tl_euclid_dist = self.euclidean_distance(top_left, current_pos)
        tr_euclid_dist = self.euclidean_distance(top_right, current_pos)
        bl_euclid_dist = self.euclidean_distance(bot_left, current_pos)
        br_euclid_dist = self.euclidean_distance(bot_right, current_pos)
        possible_corners = [tl_euclid_dist, tr_euclid_dist,
                            bl_euclid_dist, br_euclid_dist]
        closest_corner = math.inf
        # find shortest distance
        corner_idx = 0
        for idx, corners in enumerate(possible_corners):
            if corners < closest_corner:
                closest_corner = corners
                corner_idx = idx

        corner_coord = corner_list[corner_idx]
        # determine x dist, y dist, to sort moves from current pos
        # -> corner.
        moves_needed = tuple(map(lambda i, j: i - j, corner_coord,
                                 current_pos))
        horz_moves, vert_moves = moves_needed

        if (vert_moves < 0):
            vert_move = 0  # go up
        else:
            vert_move = 2  # go down

        if(horz_moves < 0):
            horz_move = 3  # go left
        else:
            horz_move = 1  # go right

        if (vert_moves == 0):
            next_move = horz_move
        elif (horz_moves == 0):
            next_move = vert_move
        else:
            if(abs(vert_moves) < abs(horz_moves)):
                next_move = vert_move
            else:
                next_move = horz_move

        return next_move

    def euclidean_distance(self, ref_coords, current_pos):
        """
        Calculates the Euclidean distance from the corner position to
        the passed in reference position
        :param ref_coords: tuple of x, y coordinates as ints for the
        ref. position (e.g. corner, nearest wall, object, etc.)
        :param current_pos: tuple of x, y ccoordinates as ints.
        :return: Euclidean distance as a float.
        """
        euclid_dist = (((ref_coords[0] - current_pos[0]) ** 2) +
                       ((ref_coords[1] - current_pos[1]) ** 2)) ** 0.5

        return euclid_dist
