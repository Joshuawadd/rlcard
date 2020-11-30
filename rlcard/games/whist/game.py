from rlcard.utils.utils import init_standard_deck
from rlcard.core import Game
from rlcard.core import Dealer
from rlcard.core import Judger
from rlcard.core import Player
from rlcard.core import Round

class WhistGame(Game):


class WhistDealer(Dealer):

    def __init__(self, np_random):

        self.np_random = np_random
        self.deck = init_standard_deck()
        self.shuffle()
        self.pot = 0
    
    def shuffle(self):
        ''' Shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def deal_card(self):
        ''' Deal one card from the deck

        Returns:
            (Card): The drawn card from the deck
        '''
        return self.deck.pop()

class WhistPlayer(Player):

    def __init__(self, player_id, np_random):
        self.np_random = np_random
        self.hand = []
        self.tricks = 0
    
    def get_player_id(self):
        ''' Return the id of the player
        '''
        return self.player_id

class WhistRound(Round):


class WhistJudger(Judger):

    def __init__(self, np_random):
        ''' Initialize a judger class
        '''
        self.np_random = np_random

    def judge_round(self, trick):

    def judge_game(self):