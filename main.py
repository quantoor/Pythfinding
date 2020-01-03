# Author: LeL
import pygame, sys, algorithms
from bean import *
from config import Config
import time


def main():
    pygame.init()

    SCREEN_W = Config.COLS * Config.TILE_SIZE # screen width
    SCREEN_H = Config.ROWS * Config.TILE_SIZE # screen height

    screen = pygame.display.set_mode((SCREEN_W + 2*Config.BORDER, SCREEN_H + 2*Config.BORDER))
    pygame.display.set_caption("Pathfinding")


    Font.set_font() # initialize fonts

    # initialize tiles
    GameController.load_map() # load blocked tiles

    # create tiles
    for y in range(0, SCREEN_H, Config.TILE_SIZE):
        for x in range(0, SCREEN_W, Config.TILE_SIZE):
            Tile(x, y, Config.TILE_SIZE, Config.TILE_SIZE)

    # build neighbors dictionary
    Tile.build_neighbors_dict() # build adjacency list
    Tile.shortestPathList, Tile.idToLevelDict, Tile.levelToIdDict = algorithms.BFS(Tile.neighborsDict, Config.source, Config.target)
    Tile.explored_tiles = Tile.idToLevelDict.keys()

    # create buttons
    Button(50, 0, Config.button_w, Config.button_h, "Set Target/Source", "set_target_source")
    Button(50 + Config.button_w, 0, Config.button_w, Config.button_h, "Set Walkable/Blocked", "set_walkable")
    Button(50 + 2*Config.button_w, 0, Config.button_w, Config.button_h, "Show Exploration", "show_exploration")
    Button(50 + 3*Config.button_w, 0, Config.button_w, Config.button_h, "Save Map", "save_map")


    # starting game
    while True:
        draw_game(screen)
        handle_events()

        if GameController.isShowingExploration:
            GameController.show_exploration()

        pygame.display.flip() # update the screen
        pygame.time.Clock().tick(Config.FPS)


def draw_game(screen):
    #screen.blit(background, (0,0))
    for tile in Tile.tilesDict.values():
        tile.draw_tile(screen)
        tile.draw_shortest_path(screen)
        tile.draw_text(screen)

    for btn in Button.buttonDict.values():
        btn.draw_button(screen)


def handle_events():
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # click buttons
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # buttons are clickable only with left click
                # check buttons
                for btn in Button.buttonDict.values():
                    btn.check_if_click(event.pos)

            # click tile
            if Button.buttonDict["set_target_source"].active:
                if event.button == 1: # lect click
                    GameController.setNewTarget()
                elif event.button == 3: # right click
                    GameController.setNewSource()

            elif Button.buttonDict["set_walkable"].active:
                if event.button == 1:
                    GameController.setWalkable(0)
                elif event.button == 3:
                    GameController.setWalkable(1)


if __name__ == '__main__':
    main()
