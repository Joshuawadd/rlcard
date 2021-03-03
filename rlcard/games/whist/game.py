from rlcard.utils.utils import init_standard_deck, elegent_form
import numpy as np

from rlcard.core import Game
from rlcard.games.whist import Dealer
from rlcard.games.whist import Judger
from rlcard.games.whist import Player
from rlcard.games.whist import Round

class WhistGame(Game):

    def __init__(self, allow_step_back=False):
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = 4
        self.payoffs = [0 for _ in range(self.num_players)]

    def init_game(self):
        
        # Initalize payoffs
        self.payoffs = [0 for _ in range(self.num_players)]

        # Initialize a dealer that can deal cards
        self.dealer = Dealer(self.np_random)

        self.judger = Judger(self.np_random)

        # Initialize players to play the game
        self.players = [Player(i, self.np_random) for i in range(self.num_players)]

        # Deal 13 cards to each player to prepare for the game
        for _ in range(13):
            for player in self.players:
                player.hand.append(self.dealer.deal_card())

        self.trump_suit = self.dealer.choose_trump_suit()    

        self.round = Round(self.dealer, self.num_players, self.np_random, self.judger, self.trump_suit)   

        # Save the hisory for stepping back to the last state.
        self.history = []

        player_id = self.round.current_player
        state = self.get_state(player_id)
        return state, player_id

    def step(self, action):
        ''' Perform one draw of the game and return next player number, and the state for next player
        '''

        if self.allow_step_back:
            # First snapshot the current state
            his_dealer = deepcopy(self.dealer)
            his_round = deepcopy(self.round)
            his_players = deepcopy(self.players)
            self.history.append((his_dealer, his_players, his_round))

        self.round.proceed_round(self.players, action)
        player_id = self.round.current_player
        state = self.get_state(player_id)
        return state, player_id

    def step_back(self):
        ''' Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        '''
        if not self.history:
            return False
        self.dealer, self.players, self.round = self.history.pop()
        return True

    def get_payoffs(self):
        ''' Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        '''
        winner = self.round.winner
        tricks = []
        for player in self.players:
            tricks.append(player.tricks)
        for i in range(0,self.num_players):
            tricks_lost = 13 - tricks[i]
            self.payoffs[i] = tricks[i]*3 - tricks_lost
            #print(tricks[i], self.payoffs[i])
        return self.payoffs

    def get_player_num(self):
        ''' Retrun the number of players in the game
        '''
        return self.num_players

    def get_action_num(self):
        ''' Return the number of possible actions in the game
        '''
        return 52

    def get_player_id(self):
        ''' Return the current player that will take actions soon
        '''
        return self.round.current_player

    def get_state(self, player_id: int):

        state = self.round.get_state(self.players, player_id)
        state['player_num'] = self.get_player_num()
        state['current_player'] = self.round.current_player
        state['trump_suit'] = self.trump_suit
        return state

    def get_legal_actions(self):
        ''' Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        '''

        return self.round.get_legal_actions(self.players, self.round.current_player, self.round.lead_player, self.round.lead_card)

    def is_over(self):
        ''' Return whether the current game is over
        '''
        return self.round.is_over

# # For test
# if __name__ == '__main__':
#    #import time
#    #random.seed(0)
#    #start = time.time()
#    game = WhistGame()
#    for _ in range(1):
#        state, button = game.init_game()
#        print(button, str(state))
#        i = 0
#        while not game.is_over():
#             i += 1
#             legal_actions = game.get_legal_actions()
#             print('legal_actions', legal_actions)
#             # for actions in legal_actions:
#             #     print(actions)
#             action = np.random.choice(legal_actions)
#             print('action', action)
#             print()
#             state, button = game.step(action)
#             print(button, state)
#        print(game.get_payoffs())
#    print('step', i)