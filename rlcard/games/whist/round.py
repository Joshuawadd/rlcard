from rlcard.core import Round
from rlcard.utils.utils import init_standard_deck
import numpy as np

class WhistRound(Round):

    def __init__(self):
        ''' When the game starts, round id should be 1
        '''

        raise NotImplementedError

    def start_new_round (self, game_pointer, raised=None):
        


    def proceed_round(self, players, action):
        ''' Call other Classes's functions to keep the game running
        '''

        player = players[self.current_player]
        card_info = action.split('-')
        color = card_info[0]
        trait = card_info[1]
        raise NotImplementedError