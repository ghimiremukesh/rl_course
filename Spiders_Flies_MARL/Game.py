import copy

import numpy as np
from Fly import Fly
from Spider_Base import Spider_Base as Spider


class Game:
    """Game Class for Base Policy"""

    def __init__(self, loc_spiders, loc_flies):
        self.flies = [Fly(loc) for loc in loc_flies]
        self.og_flies = np.copy(self.flies)
        self.spiders = [Spider(loc) for loc in loc_spiders]
        self.flies_loc = loc_flies
        self.spiders_loc = loc_spiders
        self.moves = 0
        self.move_total = [copy.deepcopy(loc_spiders)]
        self.status = [[fly.get_status() for fly in copy.deepcopy(self.flies)]]

    def is_game_over(self):
        return not False in [fly.get_status() for fly in self.flies]

    def start_game(self):
        while (not (self.is_game_over())) and (self.moves < (10 * 10)):
            self.moves += 1
            for spider in self.spiders:
                spider.move_to_fly(self.flies_loc, self.flies)

            sp_copy = copy.deepcopy(self.spiders)
            self.move_total.append([spider.position for spider in sp_copy])
            self.check_capture()

            # print([spider.position for spider in self.spiders])
            # print([fly.get_status() for fly in self.flies])
            f_copy = copy.deepcopy(self.flies)
            self.status.append([fly.get_status() for fly in f_copy])

        return self.moves

    def generate_grid(self):
        pass

    def check_capture(self):
        for spider in self.spiders:
            for fly in self.flies:
                if (spider.position == fly.position).all():
                    fly.set_status(True)
