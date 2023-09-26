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
        return random.choice([0,1,2,3])

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


