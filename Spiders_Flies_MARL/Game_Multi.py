import copy

import numpy as np
from Fly import Fly
from Spider_Multi import Spider_Multi as Spider
from Game import Game as base_policy


def _manhattan(a, b):
    distances = np.abs(a - b)
    return np.sum(distances)


class Game_Multi:
    """Game Class for Multi-Agent Rollout"""

    def __init__(self, loc_spiders, loc_flies):
        self.grid_size = 10
        self.flies = [Fly(loc) for loc in loc_flies]
        self.og_flies = np.copy(self.flies)
        self.spiders = [Spider(loc) for loc in loc_spiders]
        self.flies_loc = loc_flies
        self.spiders_loc = loc_spiders
        self.moves = 0
        self.move_total = [copy.deepcopy(loc_spiders)]
        self.status = [[fly.get_status() for fly in copy.deepcopy(self.flies)]]
        self.actions = [[] for _ in range(len(self.spiders))]

    def is_game_over(self):
        return not False in [fly.get_status() for fly in self.flies]

    def start_game(self):
        while (not (self.is_game_over())) and (self.moves < 10*10):
            # start rollout for agents
            for i in range(len(self.spiders)):
                if self.is_game_over():
                    break
                self.moves += 1
                # get Q-factors
                Q_val = self.get_Q_values(i)
                # take action corresponding to minimum Q-factor
                action_candidates = list(np.where(Q_val == np.min(Q_val))[0])
                # action = np.argmin(Q_val)
                if len(action_candidates) > 1: # remove invalid actions
                    if 0 in action_candidates and self.spiders[i].position[0] == 0:
                        action_candidates.remove(0)
                    if 1 in action_candidates and self.spiders[i].position[0] == 9:
                        action_candidates.remove(1)
                    if 2 in action_candidates and self.spiders[i].position[1] == 9:
                        action_candidates.remove(2)
                    if 3 in action_candidates and self.spiders[i].position[1] == 0:
                        action_candidates.remove(3)

                        # horizontal priority over vertical
                if 0 in action_candidates and 2 in action_candidates:
                    action_candidates.remove(0)
                if 0 in action_candidates and 3 in action_candidates:
                    action_candidates.remove(0)
                if 1 in action_candidates and 2 in action_candidates:
                    action_candidates.remove(1)
                if 1 in action_candidates and 3 in action_candidates:
                    action_candidates.remove(1)

                action = action_candidates[0]

                    # action = action_candidates[0]
                #     if 0 in action_candidates and 2 in acion
                #
                # if self.spiders[i].position[0] == 0 and action_candidates[0] == 0:
                #     action = 4
                # if self.spiders[i].position[0] == 9 and action_candidates[0] == 1:
                #     action = 4
                # if self.spiders[i].position[1] == 0 and action_candidates[0] == 3:
                #     action = 4
                # if self.spiders[i].position[1] == 9 and action_candidates[0] == 2:
                #     action = 4
                # else:
                #     action = np.argmin(Q_val)

                self.actions[i].append(self.spiders[i].actions[action])
                # get new position
                new_pos = self.spiders[i].take_action(self.spiders[i].actions[action])
                # update position
                self.spiders[i].position = new_pos

                # check everything after one move (= one fly at a time)
                sp_copy = copy.deepcopy(self.spiders)
                self.move_total.append([spider.position for spider in sp_copy])

                self.check_capture()

                # print([spider.position for spider in self.spiders])
                # print([fly.get_status() for fly in self.flies])
                f_copy = copy.deepcopy(self.flies)

                self.status.append([fly.get_status() for fly in f_copy])

    def generate_grid(self):
        pass

    def check_capture(self):
        for spider in self.spiders:
            for fly in self.flies:
                if (spider.position == fly.position).all():
                    fly.set_status(True)

    def get_Q_values(self, current_spider):
        Qfactors = []
        flies = [fly for fly in self.flies if not fly.get_status()]
        flies_loc = np.array([fly.position for fly in flies])
        for action in self.spiders[current_spider].actions:
            # move to the location:
            current_action = action
            new_pos = self.spiders[current_spider].take_action(current_action)
            pos = [new_pos]
            # assuming all other spiders move to nearest fly in that stage
            if current_spider < len(self.spiders)-1:
                for i in range(current_spider+1, len(self.spiders)):
                    next_pos = self.spiders[i].get_nearest_move(flies)
                    pos.append(next_pos)
                Qfactors.append(base_policy(copy.deepcopy(pos), flies_loc).start_game())
            else:
                for i in range(current_spider):
                    pos.append(self.spiders[i].position)
                Qfactors.append(base_policy(copy.deepcopy(pos), flies_loc).start_game())
        return Qfactors


