class Config:
    ROWS = 15 # number of rows
    COLS = 2*ROWS # number of cols
    TILE_SIZE = 45 # px
    PADDING = 20 # px
    margin_top = 40
    FPS = 60
    source = "1"
    target = "288"

    button_w = 180 # button width
    button_h = 40 # button height

    showExplorationDelay = 10 # delay between level exploration

    algList = ["BFS", "DFS", "B_FS", "Dijkstra", "A*"]
    currentAlgorithm = "Dijkstra"
