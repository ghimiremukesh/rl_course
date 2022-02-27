import pygame
import numpy as np
import os

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (250, 0, 0)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400


class Sim_Draw:
    def __init__(self):
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.SCREEN.fill(WHITE)
        self.output_dir = "std_frames/"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)


    def drawGrid(self):
        blockSize = 40  # Set the size of the grid block
        for x in range(0, WINDOW_WIDTH, blockSize):
            for y in range(0, WINDOW_HEIGHT, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.SCREEN, BLACK, rect, 1)

    def drawFlies(self, flies_loc, status, fly_img):
        fly = pygame.image.load(fly_img)
        fly = pygame.transform.scale(fly, (40, 40))
        for i in range(len(flies_loc)):
            rect1 = fly.get_rect()
            rect1.center = 40 * (flies_loc[i])
            self.SCREEN.blit(fly, rect1.center)
            if status[i]:
                rect = pygame.Rect(40 * flies_loc[i][0], 40 * flies_loc[i][1], 40, 40)
                pygame.draw.rect(self.SCREEN, RED, rect, 1)

    def drawMoves(self, moves, spider):
        spider = pygame.image.load(spider)
        spider = pygame.transform.scale(spider, (25, 25))
        for i in range(len(moves)):
            rect2 = spider.get_rect()
            rect2.center = 40 * (np.flip(moves[i])) + 15 * i
            self.SCREEN.blit(spider, rect2.center)


    def drawFrame(self, flies_loc, status, fly_img, moves, spider_img, idx):
        self.drawGrid()
        self.drawFlies(flies_loc, status, fly_img)
        self.drawMoves(moves, spider_img)
        pygame.display.update()
        pygame.image.save(self.SCREEN, "%simg%03d.jpeg" % (self.output_dir, idx))
        self.SCREEN.fill(WHITE)
        pygame.time.wait(500)

    def reset_frame(self, flies_loc, status):
        self.drawGrid()
        self.drawFlies(flies_loc, status)
