from gamestates.state import State
from config import Config
from utils.asset_loader import AssetLoader


class MainLevel(State):
    def __init__(self, game, pilot):
        super().__init__(game)
        self.name = pilot
       
    
    def update(self, delta_time):
        pass

    def render(self, display):
        pass
        
        