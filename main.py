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

    Tile.shortestPathList, Tile.levelDict = algorithms.BFS(Tile.neighborsDict, Config.source, Config.target)
    # print("Shortest path: " + str(shortestPath))
    # print("Level:")
    # for level in levelDict.keys():
    #     print("%s: %d" % (level, levelDict[level]))


    # starting
    while True:
        draw_game(screen)
        handle_events()

        pygame.display.flip() # update the screen
        pygame.time.Clock().tick(Config.FPS) # limit the framerate

def draw_game(screen):
    #screen.blit(background, (0,0))
    for tile in Tile.tilesDict.values():
        tile.draw_tile(screen)
        tile.draw_shortest_path(screen)
        tile.draw_text(screen)

    # buttons
    button(screen,"Set Target/Source",0,0,200,50,"set_target_source")
    button(screen,"Set Walkable/Block",300,0,200,50,"set_walkable")

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
        click = pygame.mouse.get_pressed()
        if click != (0,0,0) and GameController.isSettingTargetSource:
            if click[0]:
                GameController.setNewTarget()
            elif click[2]:
                GameController.setNewSource()

        elif click!= (0,0,0) and GameController.isSettingWalkable:
            if click[0]:
                GameController.setWalkable(0)
            elif click[2]:
                GameController.setWalkable(1)

def button(screen, msg, x, y, w, h, action=None):
    # ic: inactive color
    # ac: active color
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x+w and y < mouse[1] < y+h:
        # draw highlighted button
        pygame.draw.rect(screen, Color.button_ac, (x,y,w,h))
        if click[0] == 1 and action == "set_target_source":
            GameController.isSettingTargetSourceMode()

        elif click[0] == 1 and action == "set_walkable":
            GameController.isSettingWalkableMode()

    else:
        # draw normal button
        pygame.draw.rect(screen, Color.button_ic, (x,y,w,h))

    buttonText = pygame.font.Font("freesansbold.ttf", 15)
    textSurf, textRect = text_objects(msg, buttonText)
    textRect.center = (x+(w)/2, y+(h/2))
    screen.blit(textSurf,textRect)

def text_objects(text, font):
	textSurface = font.render(text,True,(0,0,0))
	return textSurface, textSurface.get_rect()




if __name__ == '__main__':
    main()
