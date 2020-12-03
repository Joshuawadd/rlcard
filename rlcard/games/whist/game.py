from rlcard.utils.utils import init_standard_deck
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
        self.payoffs = [0 for _ in range(self.num_players)]

        # Initialize a dealer that can deal cards
        self.dealer = Dealer(self.np_random)

        # Initialize players to play the game
        self.players = [Player(i, self.np_random) for i in range(self.num_players)]

        # Deal 13 cards to each player to prepare for the game
        for _ in range(13):
            for player in self.players:
                player.hand.append(self.dealer.deal_card(player))

        self.round = Round(self.dealer, self.num_players, self.np_random)

        self.trump_suit = self.dealer.choose_trump_suit()

        player_id = self.round.current_player
        state = self.get_state(player_id=current_player_id)
        return state, player_id

    def step(self, action):
        ''' Perform one draw of the game and return next player number, and the state for next player
        '''

        self.round.proceed_round(self.players, action)
        player_id = self.round.current_player
        state = self.get_state(player_id)
        return state, player_id
        raise NotImplementedError

    def step_back(self):
        ''' Takes one step backward and restore to the last state
        '''
        raise NotImplementedError

    def get_player_num(self):
        ''' Retrun the number of players in the game
        '''
        raise NotImplementedError

    def get_action_num(self):
        ''' Return the number of possible actions in the game
        '''
        raise NotImplementedError

    def get_player_id(self):
        ''' Return the current player that will take actions soon
        '''
        raise NotImplementedError

    def get_state(self, player_id: int):

    def is_over(self):
        ''' Return whether the current game is over
        '''
        raise NotImplementedError