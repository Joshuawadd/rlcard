import numpy as np
from rlcard.envs import Env
from rlcard.games.whist import Game

class WhistEnv(Env):

    def __init__(self, config):
        self.name = 'whist'
        self.game = Game()
        super().__init__(config)

    def _get_legal_actions(self):
        return self.game.get_legal_actions()

    def get_payoffs(self):

        return np.array(self.game.get_payoffs())
    
    