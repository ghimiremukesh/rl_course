# Main for Base Policy spider and flies game

from Game import Game
import numpy as np
import pygame
import sys

def main():
    flies_loc = np.array([[3, 2], [7, 1], [6, 4], [8, 8], [2, 8]])
    agent_loc = np.array([[0, 6], [0, 6]])
    spider_and_flies = Game(num_spiders=2, num_flies=5, loc_spiders=agent_loc, loc_flies=flies_loc)

    #start the game
    spider_and_flies.start_game()

    move_history = {'moves': spider_and_flies.move_total,
                    'status': spider_and_flies.status}

    print("Total Moves: %d" %(spider_and_flies.moves-1))

    pgame(np.flip(flies_loc), move_history, max=spider_and_flies.moves)


def pgame(flies_loc, move_history, max):
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)
    idx = 0
    while True:
        status = move_history['status'][idx]
        moves = move_history['moves'][idx]
        drawGrid()
        drawFlies(flies_loc, np.flip(status))
        drawMoves(moves)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        pygame.time.wait(500)
        idx += 1
        if idx >= max:
            idx = max

        # moves = move_history['moves']
        # status = move_history['status']
        # for move in moves:
        #     drawMoves(move, flies_loc)
        #     pygame.display.update()
        #     pygame.time.wait(100)



def drawGrid():
    blockSize = 40  # Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)




def drawFlies(flies_loc, status):
    fly = pygame.image.load('fly.png')
    fly = pygame.transform.scale(fly, (40, 40))
    spider = pygame.image.load('spider.png')
    spider = pygame.transform.scale(spider, (25, 25))
    for i in range(len(flies_loc)):
        rect1 = fly.get_rect()
        rect1.center = 40 *(flies_loc[i])
        SCREEN.blit(fly, rect1.center)
        if status[i]:
            rect = pygame.Rect(40*flies_loc[i][0], 40*flies_loc[i][1], 40, 40)
            pygame.draw.rect(SCREEN, RED, rect, 1)

    # for i in range(len(agent_loc)):
    #     rect2 = spider.get_rect()
    #     rect2.center = 40*(agent_loc[i]) + 15*i
    #     SCREEN.blit(spider, rect2.center)


def drawMoves(moves):
    spider = pygame.image.load('spider.png')
    spider = pygame.transform.scale(spider, (25, 25))

    for i in range(len(moves)):
        rect2 = spider.get_rect()
        rect2.center = 40*(np.flip(moves[i])) + 15*i
        SCREEN.blit(spider, rect2.center)
        pygame.display.update()

if __name__=="__main__":
    # try visualization
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    RED = (250, 0, 0)
    WINDOW_HEIGHT = 400
    WINDOW_WIDTH = 400

    main()




