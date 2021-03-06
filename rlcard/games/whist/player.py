from rlcard.core import Player

class WhistPlayer(Player):

    def __init__(self, player_id, np_random):
        self.np_random = np_random
        self.hand = []
        self.tricks = 0
        self.player_id = player_id
        self.empty_suits = []
    
    def get_player_id(self):
        ''' Return the id of the player
        '''
        return self.player_id