from rlcard.core import Judger
from rlcard.utils.utils import rank2int

class WhistJudger(Judger):

    def __init__(self, np_random):
        ''' Initialize a judger class
        '''
        self.np_random = np_random

    def judge_round(self, trump, lead_suit, played_cards):
        winning_card = None
        for card in played_cards:
            if winning_card == None:
                winning_card = card
            elif card.suit == trump:
                if winning_card.suit == trump:
                    if rank2int(card.rank) > rank2int(winning_card.rank):
                        winning_card = card
                else:
                    winning_card = card
            elif card.suit == lead_suit:
                if winning_card.suit == lead_suit:
                    if rank2int(card.rank) > rank2int(winning_card.rank):
                        winning_card = card

        return played_cards.index(winning_card)

    def judge_game(self, players):
        winner = None
        for player in players:
            if not winner:
                winner = players.index(player)
            else:
                if player.tricks > players[winner].tricks:
                    
                    winner = players.index(player)
        
        return winner