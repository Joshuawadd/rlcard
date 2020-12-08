from rlcard.core import Round
from rlcard.utils.utils import init_standard_deck, elegent_form
import numpy as np

class WhistRound(Round):

    def __init__(self, dealer, num_players, np_random, judger, trump_suit):
        ''' When the game starts, round id should be 1
        '''

        self.np_random = np_random
        self.dealer = dealer
        self.target = None
        self.current_player = 0
        self.num_players = num_players
        self.played_cards = []
        self.old_cards = []
        self.is_over = False
        self.winner = None
        self.lead_player = 0
        self.lead_suit = None
        self.round_winner = None
        self.judger = judger
        self.trump_suit = trump_suit

    def start_new_round (self, players):

        winning_card = self.judger.judge_round(self.trump_suit, self.lead_suit, self.played_cards)
        self.round_winner = (self.current_player + winning_card) % self.num_players
        players[self.round_winner].tricks +=1
        self.old_cards.append(self.played_cards)
        self.played_cards = []
        self.current_player = self.round_winner
        self.lead_player =  self.current_player
        if not players[self.current_player].hand:
            self.is_over = True
            self.winner = self.judger.judge_game(players)


    def proceed_round(self, players, action):
        ''' Call other Classes's functions to keep the game running
        '''

        player = players[self.current_player]
        #print(action)
        suit = action.suit
        rank = action.rank

        # for actions in player.hand:
        #        print(actions)

        for index, card in enumerate(player.hand):
                if suit == card.suit and rank == card.rank:
                    remove_index = index
                    break

        card = player.hand.pop(remove_index)
        self.played_cards.append(card)
        self.current_player = (self.current_player + 1) % self.num_players
        print("current player", self.current_player, self.lead_player)
        if self.current_player == self.lead_player:
            self.start_new_round(players)


    def get_legal_actions(self, players, player_id, lead_player, lead_suit):
        legal_actions = []
        wild_4_actions = []
        hand = players[player_id].hand
        target = self.target
        lead_suit_cards = []

        if player_id == lead_player:
            for card in hand:
                #print('hi', card.__str__()[0])
                #x = card.__str__()
                #legal_actions.append(x)
                legal_actions.append(card)
        else:
            for card in hand:
                if card.suit == lead_suit:
                    #x = card.__str__()
                    #legal_actions.append(x)
                    legal_actions.append(card)
        if not lead_suit_cards:
            for card in hand:
                #x = card.__str__()
                #legal_actions.append(x)
                legal_actions.append(card)
        else:
            for card in lead_suit_cards:
                #x = card.__str__()
                #legal_actions.append(x)
                legal_actions.append(card)
        
        #print('hi', legal_actions)
        return legal_actions

    def get_state(self, players, player_id):
        ''' Get player's state

        Args:
            players (list): The list of UnoPlayer
            player_id (int): The id of the player
        '''
        state = {}
        player = players[player_id]
        state['hand'] = player.hand
        state['played_cards'] = self.played_cards
        others_hand = []
        for player in players:
            if player.player_id != player_id:
                others_hand.extend(player.hand)
        state['others_hand'] = others_hand
        state['legal_actions'] = self.get_legal_actions(players, player_id, self.lead_player, self.lead_suit)
        state['card_num'] = []
        for player in players:
            state['card_num'].append(len(player.hand))
        return state