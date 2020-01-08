# Author: LeL
import pygame, sys, algorithms, time, random
from bean import *
from config import Config


def main():
    random.seed(42)
    pygame.init()

    map_w = Config.COLS * Config.TILE_SIZE # map width
    map_h = Config.ROWS * Config.TILE_SIZE # map height

    screen_w = map_w + 2*Config.PADDING # screen width
    screen_h = map_h + 2*Config.PADDING + Config.margin_top # screen height

    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Pythinding")


    Font.set_font() # initialize fonts

    # initialize tiles
    GameController.load_map() # load blocked tiles

    # create tiles
    for y in range(0, map_h, Config.TILE_SIZE):
        for x in range(0, map_w, Config.TILE_SIZE):
            Tile(x, y, Config.TILE_SIZE, Config.TILE_SIZE)

    # build neighbors dictionary
    Tile.build_neighbors_dict() # build adjacency list

    # search shortest path with BFS
    GameController.execute_current_algorithm()

    # create buttons
    Button(0*Config.button_w, 0, Config.button_w, Config.button_h, "Show Exploration", "show_exploration")
    Button(Config.button_w, 0, Config.button_w, Config.button_h, "Alg: " + Config.currentAlgorithm, "switch_alg")
    Button(screen_w-100, 0, 100, Config.button_h, "Save Map", "save_map")


    # starting game
    while True:
        draw_game(screen)
        handle_events()

        if GameController.isShowingExploration:
            GameController.show_exploration()

        pygame.display.flip() # update the screen
        pygame.time.Clock().tick(Config.FPS)


def draw_game(screen):
    screen.blit(Image.backgroundImage, (0, Config.margin_top)) # padding background

    for tile in Tile.tilesDict.values():
        tile.draw_tile(screen)
        tile.draw_shortest_path(screen)
        tile.draw_text(screen)

    for btn in Button.buttonDict.values():
        btn.draw_button(screen)


def handle_events():
    for event in pygame.event.get():
        ### quit game
        if (event.type == pygame.QUIT) or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        ### clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            ### click buttons
            if event.button==1 or event.button==3:
                for btn in Button.buttonDict.values():
                    btn.check_if_click(event.pos, event.button)

            ### click tile
            # ctrl + click to set tile walkable/blocked
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                GameController.set_walkable(event.button)
                return

            # if weights, shift + click to change tile cost
            if Config.currentAlgorithm == "Dijkstra" or Config.currentAlgorithm == "B_FS" or Config.currentAlgorithm == "A*":
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    GameController.edit_tile_cost(event.button)
                    return

            GameController.set_target_source(event.button)


if __name__ == '__main__':
    main()
