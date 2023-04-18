from enum import Enum

# This enum is used for updating and tracking the current phase the game
# is in
# Is this separation useful? Maybe future-proofing
class State(Enum):
    START = 0
    STORY = 1
    CHAR = 2
    PLAYING = 3
    LOST = 4
    WON = 5
    PAUSED = 6