from rlcard.core import Round
from rlcard.utils.utils import init_standard_deck
import numpy as np

class WhistRound(Round):

    def __init__(self, dealer, num_players, np_random):
        ''' When the game starts, round id should be 1
        '''

        self.np_random = np_random
        self.dealer = dealer
        self.target = None
        self.current_player = 0
        self.num_players = num_players
        self.played_cards = []
        self.is_over = False
        self.winner = None
        self.lead_player = 0
        self.lead_suit = None

    def start_new_round (self, game_pointer, raised=None):



    def proceed_round(self, players, action):
        ''' Call other Classes's functions to keep the game running
        '''

        player = players[self.current_player]
        suit = action[0]
        rank = action[1]

        for index, card in enumerate(player.hand):
                if suit == card.suit and rank == card.rank:
                    remove_index = index
                    break

        card = player.hand.pop(remove_index)
        self.played_cards.append(card)
        self.current_player = (self.current_player + self.direction) % self.num_players


    def get_legal_actions(self, players, player_id, lead_player, lead_suit):
        legal_actions = []
        wild_4_actions = []
        hand = players[player_id].hand
        target = self.target
        lead_suit_cards = []

        if player_id == lead_player:
            legal_actions.append(hand)
        else
            for card in hand:
                if card.suit == lead_suit:
                    lead_suit_cards.append(card)
        if not lead_suit_cards:
            for card in hand:
                legal_actions.append(card)
        else:
            for card in lead_suit_cards:
                legal_actions.append(card)
        
        return legal_actions