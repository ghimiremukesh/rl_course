import copy

import numpy as np


class Spider_Multi:
    "Base Class for spider agent with base policy"

    def __init__(self, position):
        self.position = position
        self.actions = ['N', 'S', 'E', 'W', '0']  # up down right left stay


    def take_action(self, action):
        position = copy.deepcopy(self.position)
        if action == 'N':
            if position[0] - 1 >= 0:
                position[0] -= 1
        if action == 'S':
            if position[0] + 1 <= 9:
                position[0] += 1
        if action == 'E':
            if position[1] + 1 <= 9:
                position[1] += 1
        if action == 'W':
            if position[1] - 1 >= 0:
                position[1] -= 1

        return position


    def get_nearest_move(self, flies):
        position = copy.deepcopy(self.position)
        flies = [fly for fly in flies if not fly.get_status()]
        flies_loc = np.array([fly.position for fly in flies])
        nearest_fly = self._get_nearest_fly(flies_loc)
        move_axis = np.argmax(np.abs(position - flies[nearest_fly].position))
        # move 1-unit to the maximum distance axis
        position[move_axis] -= 1 * np.sign((position - flies[nearest_fly].position)[move_axis])

        if position[1] >= 9:
            position[1] == 9
        if position[1] <= 0:
            position[1] == 0
        if position[0] <= 0:
           position[0] = 0
        if position[0] >= 9:
           position[0] = 9

        return position

    # def move_to_fly(self, flies):
    #     flies = [fly for fly in flies if not fly.get_status()]
    #     flies_loc = np.array([fly.position for fly in flies])
    #     nearest_fly = self._get_nearest_fly(flies_loc)
    #     move_axis = np.argmax(np.abs(self.position - flies[nearest_fly].position))
    #     # move 1-unit to the maximum distance axis
    #     self.position[move_axis] -= 1 * np.sign((self.position - flies[nearest_fly].position)[move_axis])
    #
    #     if self.position[1] >= 9:
    #         self.position[1] == 9
    #     if self.position[1] <= 0:
    #         self.position[1] == 0
    #     if self.position[0] <= 0:
    #         self.position[0] = 0
    #     if self.position[0] >= 9:
    #         self.position[0] = 9

    def _get_nearest_fly(self, flies_loc):
        distances = np.abs(flies_loc - self.position)
        sums = np.sum(distances, axis=1)
        close = np.min(sums)
        diff = sums - close
        idx = np.where(diff == 0)
        if len(idx) == 1:
            return idx[0][0]
        else:
            h_min = distances[idx[0][0]][0]
            min_idx = None
            for i in range(1, len(idx[0])):
                if distances[idx[0][i]][0] < h_min:
                    h_min = distances[idx[0][i]][0]
                    min_idx = idx[0][i]
            return min_idx

    # def get_Q_values(self, flies):
    #     Qfactors = []
    #     for action in self.actions:
    #         # get one-step lookahead action :: go towards nearest fly
    #         self.move_to_fly(flies)
    #         Qfactors =