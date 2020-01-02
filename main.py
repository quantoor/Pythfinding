# Author: LeL
import pygame, sys
from bean import *

def main():
    pygame.init()
    pygame.font.init()

    ROWS = 3 # number of rows
    COLS = 3 # number of cols
    TILE_SIZE = 100 # px

    SCREEN_W = ROWS * TILE_SIZE # screen width
    SCREEN_H = COLS * TILE_SIZE # screen height

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Pathfinding")

    #menuImage = pygame.image.load("images/menu_t.jpg")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255,255,255))


    # create tiles
    for y in range(0, screen.get_height(), TILE_SIZE):
        for x in range(0, screen.get_width(), TILE_SIZE):
            Tile(x, y, TILE_SIZE, TILE_SIZE)

    # build neighbors dictionary
    Tile.build_neighbors_dict()
    Tile.print_neighbors()

    # starting menu
    while True:
        screen.blit(background, (0,0))
        for tile in Tile.tilesDict.values():
            tile.draw_tile(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


        #screen.fill(backgroundColor)

        title = "Pathfinding"
        #functions.text_display(screen, title, display_width/2, display_height/5, 80)
        author = "Author: LeL"
        #functions.text_display(screen,author,115,580,15)
        #functions.button(screen,"Play",display_width/2-50,display_height/2-75,100,50,buttonColor,buttonColorBright,"play_game")
        #functions.button(screen,"Keys",display_width/2-50,display_height/2,100,50,buttonColor,buttonColorBright,"legend")
        #functions.button(screen,"Info",display_width/2-50,display_height/2+75,100,50,buttonColor,buttonColorBright,"credits")
        #functions.button(screen,"Quit",display_width/2-50,display_height/2+150,100,50,buttonColor,buttonColorBright,"quit")

        pygame.display.flip()


if __name__ == '__main__':
    main()




# colors
# backgroundColor = (255, 255, 102)
# buttonColor = (153, 76, 0)
# buttonColorBright = (204, 102, 0)
