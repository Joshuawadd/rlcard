from rlcard.utils.utils import init_standard_deck
from rlcard.core import Dealer
import numpy as np

class WhistDealer(Dealer):

    def __init__(self, np_random):

        self.np_random = np_random
        self.deck = init_standard_deck()
        self.start_deck = self.deck
        self.shuffle()
        self.pot = 0
    
    def shuffle(self):
        ''' Shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def choose_trump_suit(self):
        suit_list = ['S', 'H', 'D', 'C']
        return (self.np_random.choice(suit_list))


    def deal_card(self):
        ''' Deal one card from the deck

        Returns:
            (Card): The drawn card from the deck
        '''
        return self.deck.pop()