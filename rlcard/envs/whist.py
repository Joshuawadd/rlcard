import numpy as np
from rlcard.envs import Env
from rlcard.games.whist import Game
from rlcard.games.whist.utils import encode_hand, encode_target
from rlcard.games.whist.utils import ACTION_SPACE, ACTION_LIST
from rlcard.games.whist.utils import cards2list

class WhistEnv(Env):

    def __init__(self, config):
        self.name = 'whist'
        self.game = Game()
        super().__init__(config)
        self.state_shape = [3, 4, 13]

    def _get_legal_actions(self):
        legal_actions = self.game.get_legal_actions()
        legal_ids = [ACTION_SPACE[action] for action in legal_actions]
        return legal_ids

    def get_payoffs(self):

        return np.array(self.game.get_payoffs())

    def _extract_state(self, state):
        obs = np.zeros((3, 4, 13), dtype=int)
        encode_hand(obs[0], state['hand'])
        encode_target(obs[1], state['lead_card'])
        encode_hand(obs[2], state['others_hand'])
        legal_action_id = self._get_legal_actions()
        extracted_state = {'obs': obs, 'legal_actions': legal_action_id}
        if self.allow_raw_data:
            extracted_state['raw_obs'] = state
            extracted_state['raw_legal_actions'] = [
                a for a in state['legal_actions']]
        if self.record_action:
            extracted_state['action_record'] = self.action_recorder
        return extracted_state

    def _decode_action(self, action_id):
        legal_ids = self._get_legal_actions()
        if action_id in legal_ids:
            return ACTION_LIST[action_id]
        # if (len(self.game.dealer.deck) + len(self.game.round.played_cards)) > 17:
        #    return ACTION_LIST[60]
        return ACTION_LIST[np.random.choice(legal_ids)]

    def get_perfect_information(self):
        ''' Get the perfect information of the current state

        Returns:
            (dict): A dictionary of all the perfect information of the current state
        '''
        state = {}
        state['player_num'] = self.game.get_player_num()
        state['hand_cards'] = [cards2list(player.hand)
                               for player in self.game.players]
        state['played_cards'] = cards2list(self.game.round.played_cards)
        state['target'] = self.game.round.target.str
        state['current_player'] = self.game.round.current_player
        state['trump_suit'] = self.game.trump_suit
        state['legal_actions'] = self.game.round.get_legal_actions(
            self.game.players, state['current_player'])
        if self.game.round.lead_card:
            state['lead_card'] = self.game.round.lead_card.__str__()
        else:
            state['lead_card'] = self.game.round.lead_card
        state['lead_player'] = self.game.round.lead_player
        return state    
    