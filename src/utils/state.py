from enum import Enum

#do i really need to do this
class State(Enum):
    START = 0
    STORY = 1
    CHAR = 2
    PLAYING = 3
    LOST = 4
    WON = 5
    PAUSED = 6