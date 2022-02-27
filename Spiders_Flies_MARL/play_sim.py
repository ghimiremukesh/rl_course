from Sim_Draw import Sim_Draw
import numpy as np
from Game import Game
from Game_Multi import Game_Multi
from Game_Std import Game_Std
import pygame
import sys
import os

class Main:

    def __init__(self):
        self.capture = True
        self.sim_draw = Sim_Draw()
        self.flies_loc = np.array([[3, 2], [7, 1], [6, 4], [8, 8], [2, 8]])
        self.agent_loc = np.array([[0, 6], [0, 6]])

        # self.spider_and_flies = Game_Multi(loc_spiders=self.agent_loc, loc_flies=self.flies_loc)

        # self.spider_and_flies = Game(loc_spiders=self.agent_loc, loc_flies=self.flies_loc)

        self.spider_and_flies = Game_Std(loc_spiders=self.agent_loc, loc_flies=self.flies_loc)

        # start the game
        self.spider_and_flies.start_game()

        self.move_history = {'moves': self.spider_and_flies.move_total,
                             'status': self.spider_and_flies.status}

        print("Total Moves: %d" % (self.spider_and_flies.moves))
        # print("Player 1's actions: ", self.spider_and_flies.actions[0])
        # print("Player 2's actions: ", self.spider_and_flies.actions[1])

        idx = 0
        while idx <= self.spider_and_flies.moves:
            self.status = self.move_history['status'][idx]
            self.moves = self.move_history['moves'][idx]
            self.sim_draw.drawFrame(np.flip(self.flies_loc), np.flip(self.status), 'fly.png', self.moves, 'spider.png', idx)
            idx += 1
            # if idx >= 25:
            #     idx = 25
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    Main()
