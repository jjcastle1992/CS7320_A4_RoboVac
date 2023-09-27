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

class RoboVac:
    def __init__(self, config_list, clean_set):
        self.room_width, self.room_height = config_list[0]
        self.pos = config_list[1]   # starting position of vacuum
        self.block_list = config_list[2]   # blocks list (x,y,width,ht)
        self.explored_list = clean_set
        self.unvisited_list = []
        self.start_corner_found = False
        self.last_move = None

        # fill in with your info
        self.name = "James Castle"
        self.id = "29248132"

    def get_next_move(self, current_pos):  # called by PyGame code
        # Return a direction for the vacuum to move
        # random walk 0=north # 1=east 2=south 3=west
        next_move = None

        up = 0
        down = 2
        left = 3
        right = 1

        # What the vacuum knows
        # 1. Room dimensions
        # 2. Starting Position
        # 3. Block lists

        # V1.0 Strat
        # Goal: Simply get 100% Coverage in <= 400 moves
        # Plan:
        # Start basic (can we solve a room?)
        # 0. Check to see if we're already in the corner. If yes, skip
        #    to step 3.
        in_the_corner = self.at_corner(current_pos)
        if((in_the_corner) and (self.start_corner_found == False)):
            self.start_corner_found = True
        # 1. Find closest wall (vertical or horz), go there.
        # 2. Find closest perp wall (corner)
        if(not self.start_corner_found):
            next_move = self.find_corner(current_pos)
        # 3. Once in corner, pick 1 of 2 legal directions.
        #    For later: pick a path that has the longest path of
        #    Unvisited nodes (weight closest to 0)
        legal_moves = self.legal_move_check(current_pos)
        if(self.last_move in legal_moves):
            next_move = self.last_move
        # 4. Proceed until you hit boundary.
        elif(self.last_move):
            print('BUMP!')
            # pick next best move
            repeat_moves = self.visited_before(current_pos, legal_moves)
            if(not next_move):
                for move in legal_moves:
                    if(move not in repeat_moves):
                        next_move = move

            if(next_move in repeat_moves):  # check if corner in moves
                # find a move that isn't repeated
                for moves in legal_moves:
                    if not next_move:
                        if(moves not in repeat_moves):
                            next_move = moves
                            break

        # 5. Pick legal move that does not retrace steps, and move once.
        # 7. Invert direction from Step 4.
        # 8. Move until hit next wall.
        # 9. Repeat Step 5.
        # 11.Invert direction from Step 7. (repeat step 7ish)
        # 12. Repeat Step 5, 11ish until board clean.

        # Problems to solve:
        # 1. Track where we've been (to avoid retracing steps):
        #    1.1. Weight visited nodes to discentivize (but not block)
        #    travel to already visit nodes.
        # 2. Consider dividing room into smaller sections
        #    2.1. Clean closest quadrant first.
        #    2.2. Pick next closest quadrant, clean
        #    2.3. Repeat until all quadrants clean
        # 3. For RoboVac 0, we know there is no furniture, so can borrow
        #    real vac logic such as a back and forth pattern snake
        #    pattern

        # Strategies to consider
        # 1. Shortest path to nearest unvisited node using Manhattan
        #    distance.
        # 2. Strategies to avoid getting stuck on furniture
        if(next_move):
            self.last_move = next_move

        return next_move

    def start_state(self):
        """
        Numpy array start state w/ 0 (uncleaned) and 100(obtacle) values
        :return:
        """
        pass

    def goal_state(self):
        """
        Numpy array goal state with 1 (cleaned) and 100 (obstacle)values
        :return:
        """
        pass

    def priority_queue(self):
        #  0 = unexplored;
        #  1 = explored
        #  100 = blocked
        pass


    def manhattan_dist(self):
        pass

    def room_state_tracker_np(self):
        room_state = np.zeros((self.room_height, self.room_width))
        # look at coordinate pairs in clean list and set clean = 1
        # find obstacle coordinates and set equal to 10.
        # define goal board (1s everywhere except obstacle)

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
        if((x - 1) >= 0):
            legal_moves.append(3)  # add left to legal moves

        # Check right
        if ((x + 1) <= (self.room_width - 1)):
            legal_moves.append(1)  # add right to legal moves
        # check up
        if ((y - 1) >= 0):
            legal_moves.append(0)  # add up to legal moves
        # check down
        if ((y + 1) <= (self.room_height - 1)):
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
