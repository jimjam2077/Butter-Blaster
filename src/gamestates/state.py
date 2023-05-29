from src.utils.audio_loader import AudioLoader


class State():
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def update(self, delta_time):
        pass
    def render(self, surface):
        pass

    def restart(self):
        self.game.state_stack.clear()
        self.game.state_stack.append(self)
    
    def reset_game(self):
        while len(self.game.state_stack) > 3:
            self.game.state_stack.pop()
        self.game.state_stack.append(self)
                    
    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()