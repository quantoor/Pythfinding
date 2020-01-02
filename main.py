# Author: LeL
import pygame, sys
from bean import *
import algorithms


def main():
    pygame.init()
    pygame.font.init()

    SCREEN_W = Config.ROWS * Config.TILE_SIZE # screen width
    SCREEN_H = Config.COLS * Config.TILE_SIZE # screen height

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Pathfinding")

    #menuImage = pygame.image.load("images/menu_t.jpg")
    # background = pygame.Surface(screen.get_size())
    # background = background.convert()
    # background.fill((255,255,255))

    # create tiles
    for y in range(0, screen.get_height(), Config.TILE_SIZE):
        for x in range(0, screen.get_width(), Config.TILE_SIZE):
            Tile(x, y, Config.TILE_SIZE, Config.TILE_SIZE)

    # build neighbors dictionary
    Tile.build_neighbors_dict() # build adjacency list
    Tile.print_neighbors() # for debug

    Tile.shortestPath, Tile.levelDict = algorithms.BFS(Tile.neighborsDict, Config.source, Config.target)
    # print("Shortest path: " + str(shortestPath))
    # print("Level:")
    # for level in levelDict.keys():
    #     print("%s: %d" % (level, levelDict[level]))


    # starting
    while True:
        #screen.blit(background, (0,0))
        for tile in Tile.tilesDict.values():
            tile.draw_tile(screen)
            tile.draw_text(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


        title = "Pathfinding"
        #functions.text_display(screen, title, display_width/2, display_height/5, 80)
        author = "Author: LeL"
        #functions.text_display(screen,author,115,580,15)
        #functions.button(screen,"Play",display_width/2-50,display_height/2-75,100,50,buttonColor,buttonColorBright,"play_game")
        #functions.button(screen,"Keys",display_width/2-50,display_height/2,100,50,buttonColor,buttonColorBright,"legend")
        #functions.button(screen,"Info",display_width/2-50,display_height/2+75,100,50,buttonColor,buttonColorBright,"credits")
        #functions.button(screen,"Quit",display_width/2-50,display_height/2+150,100,50,buttonColor,buttonColorBright,"quit")

        pygame.display.flip() # update the screen
        pygame.time.Clock().tick(Config.FPS) # limit the framerate


if __name__ == '__main__':
    main()




# colors
# backgroundColor = (255, 255, 102)
# buttonColor = (153, 76, 0)
# buttonColorBright = (204, 102, 0)
