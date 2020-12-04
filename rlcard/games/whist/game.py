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
        
        # Initalize payoffs
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
        if winner is not None and len(winner) == 1:
            self.payoffs[winner[0]] = 1
            self.payoffs[1 - winner[0]] = -1
        return self.payoffs

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

        state = self.round.get_state(self.players, player_id)
        state['player_num'] = self.get_player_num()
        state['current_player'] = self.round.current_player
        return state

    def get_legal_actions(self):
        ''' Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        '''

        return self.round.get_legal_actions(self.players, self.round.current_player, sealf.lead_player, self.lead_suit)

    def is_over(self):
        ''' Return whether the current game is over
        '''
        raise NotImplementedError