from rlcard.core import Round, Card
from rlcard.utils.utils import init_standard_deck, elegent_form
from rlcard.games.whist.utils import cards2list
import numpy as np
from rlcard.utils.utils import init_standard_deck

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
        self.lead_card = None
        self.round_winner = None
        self.judger = judger
        self.trump_suit = trump_suit
        self.played_card = None
        self.winning_card = None
        self.round_cards = []
        self.last_lead = 0

    def start_new_round (self, players):

        winning_index, self.winning_card = self.judger.judge_round(self.trump_suit, self.lead_card.suit, self.played_cards)
        self.round_winner = (self.current_player + winning_index) % self.num_players
        players[self.round_winner].tricks +=1
        players[(self.round_winner + 2) % self.num_players].tricks += 1
        self.old_cards.extend(self.played_cards)
        # print("")
        # print("Player 0 hand:", cards2list(players[0].hand))
        # print("Player 1 hand:", cards2list(players[1].hand))
        # print("Player 2 hand:", cards2list(players[2].hand))
        # print("Player 3 hand:", cards2list(players[3].hand))
        # print("Lead player:", self.lead_player)
        # print("Trump Suit:", self.trump_suit)
        # print("Played Cards:", cards2list(self.played_cards))
        # print("Winner:", self.round_winner, "Winning card:", winning_card)
        # print("Score:", players[0].tricks, players[1].tricks, players[2].tricks, players[3].tricks)
        self.round_cards = self.played_cards
        self.last_lead = self.lead_player
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
        suit = action[1]
        rank = action[0]

        # for actions in player.hand:
        #        print(actions)

        for index, card in enumerate(player.hand):
            if suit == card.suit and rank == card.rank:
                remove_index = index
                break

        card = player.hand.pop(remove_index)
        self.played_card = card
        self.played_cards.append(card)
        #print(player.get_player_id(), self.lead_player)
        if player.get_player_id() == self.lead_player:    
            self.lead_card = card
        else:
            if card.suit != self.lead_card.suit:
                player.empty_suits.append(card.suit)
        self.current_player = (self.current_player + 1) % self.num_players
        #print("current player", self.current_player, self.lead_player)
        if self.current_player == self.lead_player:
            self.start_new_round(players)


    def get_legal_actions(self, players, player_id, lead_player, lead_card):
        legal_actions = []
        wild_4_actions = []
        hand = players[player_id].hand
        target = self.target
        #print(lead_card)
        if lead_card:
            lead_suit = lead_card.suit
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
                    lead_suit_cards.append(card)
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
        return cards2list(legal_actions)

    def get_state(self, players, player_id):
        ''' Get player's state

        Args:
            players (list): The list of UnoPlayer
            player_id (int): The id of the player
        '''
        state = {}
        player = players[player_id]
        state['hand'] = cards2list(player.hand)
        state['played_cards'] = cards2list(self.played_cards)
        state['old_cards'] = cards2list(self.old_cards)

        others_hand = [[],[],[]]
        for player in players:
            i=0
            if player.player_id != player_id:
                possible_cards = init_standard_deck()
                for card in player.hand:
                    possible_cards.remove(card)
                for card in self.played_cards:
                    possible_cards.remove(card)
                for card in self.old_cards:
                    possible_cards.remove(card)
                for card in possible_cards:
                    if card.suit in player.empty_suits:
                        possible_cards.remove(card)
                others_hand[i].extend(possible_cards)
                i+=1

        #print(cards2list(others_hand[0]))

        state['others_hand_0'] = cards2list(others_hand[0])
        state['others_hand_1'] = cards2list(others_hand[1])
        state['others_hand_2'] = cards2list(others_hand[2])

        # others_hand = []
        # for player in players:
        #     if player.player_id != player_id:
        #         others_hand.extend(player.hand)
        # state['others_hand'] = cards2list(others_hand)
        state['legal_actions'] = self.get_legal_actions(players, player_id, self.lead_player, self.lead_card)
        state['card_num'] = []
        for player in players:
            state['card_num'].append(len(player.hand))
        if self.lead_card:
            state['lead_card'] = self.lead_card.__str__()
        else:
            state['lead_card'] = self.lead_card
        state['lead_player'] = self.lead_player
        return state