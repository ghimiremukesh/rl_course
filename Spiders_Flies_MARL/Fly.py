import numpy as np


class Fly:
    """Base Class for a fly"""

    def __init__(self, position, move_random=False):
        self.position = position
        self.move_random = move_random
        self.captured = False

    # DO NOT NEED THIS FOR GAME 1
    def move_random(self):
        if self.move_random:
            pass

    def is_captured(self, spider_pos):
        self.captured = (spider_pos == self.position).all()

    def get_status(self):
        return self.captured

    def set_status(self, status):
        self.captured = status
