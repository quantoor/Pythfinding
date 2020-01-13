class Config:
    ROWS = 15 # number of rows
    COLS = 2*ROWS # number of columns
    TILE_SIZE = 45 # px
    PADDING = 20 # px
    margin_top = 40 # px
    FPS = 60 # max frames per second
    source = "1"
    target = "288"

    button_w = 180 # button width
    button_h = 40 # button height

    showExplorationDelay = 100 # delay between level exploration in milliseconds

    algList = ["BFS", "DFS", "B_FS", "Dijkstra", "A*"]
    currentAlgorithm = "Dijkstra"
