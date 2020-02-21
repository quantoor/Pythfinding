#################################

# Author: LeL

#################################


import pygame, sys, algorithms, time, random
from classes import *


def main():
    random.seed(42)
    pygame.init()

    screen = pygame.display.set_mode((Config.screen_w, Config.screen_h))
    pygame.display.set_caption("Pythinding")


    Font.set_font() # initialize fonts

    # initialize tiles
    # GameController.load_map() # load map

    # create tiles
    for y in range(0, Config.map_h, Config.TILE_SIZE):
        for x in range(0, Config.map_w, Config.TILE_SIZE):
            Tile(x, y, Config.TILE_SIZE, Config.TILE_SIZE)

    GameController.load_map()

    # build neighbors dictionary
    Tile.build_neighbors_dict() # build adjacency list

    # search shortest path with BFS
    GameController.execute_current_algorithm()

    # create buttons
    button_margin = (Config.margin_top+Config.PADDING-Config.button_h)/2
    Button(Config.PADDING, button_margin, Config.button_w, Config.button_h, "Show Exploration", "show_exploration")
    Button(Config.PADDING+Config.button_w+button_margin, button_margin, Config.button_w, Config.button_h, "Alg: " + Config.currentAlgorithm, "switch_alg")
    Button(Config.PADDING+2*Config.button_w+2*button_margin, button_margin, 100, Config.button_h, "Save Map", "save_map")


    # starting game
    while True:
        draw_game(screen)
        handle_events()

        if GameController.isShowingExploration:
            GameController.show_exploration()

        pygame.display.flip() # update the screen
        pygame.time.Clock().tick(Config.FPS) # limit framerate


def draw_game(screen):
    screen.blit(Image.backgroundImage, (0, 0)) # padding background

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
            if Config.currentAlgorithm in ["Dijkstra", "B_FS", "A*"]:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    GameController.edit_tile_cost(event.button)
                    return

            GameController.set_target_source(event.button)


if __name__ == '__main__':
    main()
