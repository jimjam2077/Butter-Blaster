from enum import Enum

class State(Enum):
    GAME_START = 0
    GAME_RUNNING = 1
    GAME_OVER = 2
    GAME_WON = 3
    GAME_PAUSED = 4