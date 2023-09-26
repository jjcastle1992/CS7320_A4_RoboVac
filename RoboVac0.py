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
    def __init__(self, config_list):
        self.room_width, self.room_height = config_list[0]
        self.pos = config_list[1]   # starting position of vacuum
        self.block_list = config_list[2]   # blocks list (x,y,width,ht)

        # fill in with your info
        self.name = "James Castle"
        self.id = "29248132"


    def get_next_move(self, current_pos):  # called by PyGame code
        # Return a direction for the vacuum to move
        # random walk 0=north # 1=east 2=south 3=west

        # What the vacuum knows
        # 1. Room dimensions
        # 2. Starting Position
        # 3. Block lists

        # V1.0 Strat
        # Goal: Simply get 100% Coverage in <= 400 moves
        # Plan:
        # Start basic (can we solve a room?)
        # 1. Find closest wall (vertical or horz), go there.
        # 2. Find closest perp wall (corner)
        wall_move, corner_move = self.find_corner(current_pos)
        # 3. Once in corner, pick 1 of 2 legal directions.
        #    For later: pick a path that has the longest path of
        #    Unvisited nodes (weight closest to 0)
        # 4. Proceed until you hit boundary.
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

        return random.choice([0,1,2,3])

    def find_corner(self, current_pos):
        """
        Finds nearest wall, and then nearest corner.
        :param current_pos: tuple consisting of x,y coordinate position
        of robot.
        :return: ordered moveset to get robot to nearest corner.
        """
        first_move = -1
        second_move = -1

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
        corner_coord = (-100, -100)
        # find shortest distance
        for count, corners in enumerate(possible_corners):
            if corners < closest_corner:
                closest_corner = corners
                count += 1
                corner_coord = corner_list[count]
        # determine x dist, y dist, to sort moves from current pos
        # -> corner.
        moves_needed = corner_coord - current_pos
        horz_moves, vert_moves = moves_needed
        if(abs(horz_moves) < abs(vert_moves)):
            if (horz_moves < 0):
                first_move = 3  # go left
                second_move
            else:
                first_move = 1  # go right
        else:
            if(vert_moves < 0):
                first_move = 2  # go down
            else:
                first_move = 0  # go up




        return 1, 0  # bogus for now

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
