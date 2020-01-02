# Author: LeL
import pygame, sys, algorithms
from bean import *
from config import Config
import time

def main():
    pygame.init()
    pygame.font.init()

    SCREEN_W = Config.COLS * Config.TILE_SIZE # screen width
    SCREEN_H = Config.ROWS * Config.TILE_SIZE # screen height

    screen = pygame.display.set_mode((SCREEN_W + 2*Config.BORDER, SCREEN_H + 2*Config.BORDER))
    pygame.display.set_caption("Pathfinding")

    #menuImage = pygame.image.load("images/menu_t.jpg")
    # background = pygame.Surface(screen.get_size())
    # background = background.convert()
    # background.fill((255,255,255))

    # create tiles
    for y in range(0, SCREEN_H, Config.TILE_SIZE):
        for x in range(0, SCREEN_W, Config.TILE_SIZE):
            Tile(x, y, Config.TILE_SIZE, Config.TILE_SIZE)

    # build neighbors dictionary
    Tile.build_neighbors_dict() # build adjacency list
    #Tile.print_neighbors() # for debug

    start_time = int(round(time.time() * 1000))
    Tile.shortestPathList, Tile.levelDict = algorithms.BFS(Tile.neighborsDict, Config.source, Config.target)
    end_time = int(round(time.time() * 1000))
    bfs_time = end_time-start_time
    print("BFS time: " + str(bfs_time))
    # print("Shortest path: " + str(shortestPath))
    # print("Level:")
    # for level in levelDict.keys():
    #     print("%s: %d" % (level, levelDict[level]))


    # starting
    while True:
        draw_game(screen)
        handle_events()

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

def draw_game(screen):
    #screen.blit(background, (0,0))
    for tile in Tile.tilesDict.values():
        tile.draw_tile(screen)
        tile.draw_shortest_path(screen)
        tile.draw_text(screen)

def handle_events():
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # click
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()
            m_x = (m_pos[0] - Config.BORDER) // Config.TILE_SIZE
            m_y = (m_pos[1] - Config.BORDER) // Config.TILE_SIZE

            try:
                new_target_id = Tile.coordToIdDict[(m_x, m_y)]
                Config.target = new_target_id
                start_time = int(round(time.time() * 1000))
                Tile.shortestPathList, Tile.levelDict = algorithms.BFS(Tile.neighborsDict, Config.source, Config.target)
                end_time = int(round(time.time() * 1000))
                bfs_time = end_time-start_time
                print("BFS time: " + str(bfs_time))
                print("(%d, %d) is the new target" % (m_x, m_y))
            except:
                pass

if __name__ == '__main__':
    main()


# colors
# backgroundColor = (255, 255, 102)
# buttonColor = (153, 76, 0)
# buttonColorBright = (204, 102, 0)
