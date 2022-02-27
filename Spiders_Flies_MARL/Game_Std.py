import copy

import numpy as np
from Fly import Fly
from Spider_Std import Spider_Std as Spider
from Game import Game as base_policy


def _manhattan(a, b):
    distances = np.abs(a - b)
    return np.sum(distances)


class Game_Std:
    """Game Class for Standard Rollout"""

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
        self.actions = [[]]

    def is_game_over(self):
        return not False in [fly.get_status() for fly in self.flies]

    def start_game(self):
        while (not (self.is_game_over())) and (self.moves < 10*10):
            # start rollout for agents
            self.moves += 1
            if self.is_game_over():
                break
            # get Q-factors
            Q_val = self.get_Q_values()
            # take action corresponding to minimum Q-factor
            action_candidates = list(np.where(Q_val == np.min(Q_val))[0])
            # action = np.argmin(Q_val)
            if len(action_candidates) > 1:  # remove invalid actions
                for actions in action_candidates:
                    action1 = actions // 5
                    action2 = actions % 5
                    if action1 == 0 and self.spiders[0].position[0] == 0:
                        action_candidates.remove(actions)
                    if action2 == 0 and self.spiders[1].position[0] == 0:
                        action_candidates.remove(actions)
                    if action1 == 1 and self.spiders[0].position[0] == 9:
                        action_candidates.remove(actions)
                    if action2 == 1 and self.spiders[1].position[0] == 9:
                        action_candidates.remove(actions)
                    if action1 == 2 and self.spiders[0].position[1] == 9:
                        action_candidates.remove(actions)
                    if action2 == 2 and self.spiders[1].position[1] == 9:
                        action_candidates.remove(actions)
                    if action1 == 3 and self.spiders[0].position[1] == 0:
                        action_candidates.remove(actions)
                    if action2 == 3 and self.spiders[1].position[1] == 0:
                        action_candidates.remove(actions)

                # horizontal priority over vertical
                acts = np.array([[action // 5, action % 5] for action in action_candidates])
                if 0 in acts[:, 0] and 2 in acts[:, 0]:
                    action_candidates.remove(action_candidates[np.where(acts[:, 0] == 0)[0][0]])
                if 0 in acts[:, 0] and 3 in acts[:, 0]:
                    action_candidates.remove(action_candidates[np.where(acts[:, 0] == 0)[0][0]])
                if 1 in acts[:, 0] and 2 in acts[:, 0]:
                    action_candidates.remove(action_candidates[np.where(acts[:, 0] == 1)[0][0]])
                if 1 in acts[:, 0] and 3 in acts[:, 0]:
                    action_candidates.remove(action_candidates[np.where(acts[:, 0] == 1)[0][0]])

                action1 = action_candidates[0] // 5
                action2 = action_candidates[0] % 5
            else:
                action1 = action_candidates[0] // 5
                action2 = actions % 5


            self.actions.append([self.spiders[0].actions[action1], self.spiders[1].actions[action2]])
            # get new position
            new_pos1 = self.spiders[0].take_action(self.spiders[0].actions[action1])
            new_pos_2 = self.spiders[1].take_action(self.spiders[1].actions[action2])
            # update position
            self.spiders[0].position = new_pos1
            self.spiders[1].position = new_pos_2

            # check everything after one move (= one fly at a time)
            sp_copy = copy.deepcopy(self.spiders)
            self.move_total.append([spider.position for spider in sp_copy])

            self.check_capture()

            # print([spider.position for spider in self.spiders])
            # print([fly.get_status() for fly in self.flies])
            f_copy = copy.deepcopy(self.flies)

            self.status.append([fly.get_status() for fly in f_copy])

    def check_capture(self):
        for spider in self.spiders:
            for fly in self.flies:
                if (spider.position == fly.position).all():
                    fly.set_status(True)

    def get_Q_values(self):
        Qfactors = []
        flies = [fly for fly in self.flies if not fly.get_status()]
        flies_loc = np.array([fly.position for fly in flies])
        # Qfactors will be 5*5 = 25

        for action1 in self.spiders[0].actions:
            for action2 in self.spiders[0].actions:
                # one-step look-ahead minimization
                new_pos1 = self.spiders[0].take_action(action1)
                pos = [new_pos1]
                new_pos2 = self.spiders[1].take_action(action2)
                pos.append(new_pos2)
                Qfactors.append(base_policy(copy.deepcopy(pos), flies_loc).start_game())

        return Qfactors


