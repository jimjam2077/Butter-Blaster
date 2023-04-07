from enum import Enum

class State(Enum):
    START = 0
    PLAYING = 1
    LOST = 2
    WON = 3
    PAUSED = 4