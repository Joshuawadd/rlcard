from rlcard.utils.utils import init_standard_deck
from rlcard.core import Game
from rlcard.core import Dealer
from rlcard.core import Judger
from rlcard.core import Player
from rlcard.core import Round

class WhistGame(Game):

    def __init__(self, allow_step_back=False):
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = 2
        self.payoffs = [0 for _ in range(self.num_players)]

    def init_game(self):
        self.payoffs = [0 for _ in range(self.num_players)]

        # Initialize a dealer that can deal cards
        self.dealer = Dealer(self.np_random)

        # Initialize four players to play the game
        self.players = [Player(i, self.np_random) for i in range(self.num_players)]

        # Deal 7 cards to each player to prepare for the game
        for i in range(13):
            for player in self.players:
                player.hand.append(self.dealer.deal_card(player))

        self.round = Round(self.dealer, self.num_players, self.np_random)

        trump_suit = self.dealer.choose_trump_suit()

        player_id = self.round.current_player
        state = self.get_state(player_id)
        return state, player_id

    def step(self, action):
        ''' Perform one draw of the game and return next player number, and the state for next player
        '''
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

    def is_over(self):
        ''' Return whether the current game is over
        '''
        raise NotImplementedError