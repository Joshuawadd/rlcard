''' Whist rule models
'''

import numpy as np

import rlcard
from rlcard.models.model import Model
from rlcard.utils.utils import rank2int

class WhistRuleAgentV1(object):
    ''' Whist Rule agent version 1
    '''

    def __init__(self):
        self.use_raw = True

    def step(self, state):
        ''' Predict the action given raw state. A naive rule. Choose the color
            that appears least in the hand from legal actions. Try to keep wild
            cards as long as it can.

        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        '''

        legal_actions = state['raw_legal_actions']
        state = state['raw_obs']

        hand = state['hand']

        played_cards = state['played_cards']

        player_position = state['player_position']

        trump = state['trump_suit']

        highest_card = None

        winnable_cards = []


        lowest_card = None

        if player_position == 0:
            for card in hand:
                #print(card)
                if highest_card == None:
                    highest_card = card                 
                elif rank2int(card[0]) > rank2int(highest_card[0]):
                    highest_card = card
            action = highest_card
        else:
            for card in legal_actions:
                if self.can_win(played_cards, card, trump, state['lead_card'][1]):
                    winnable_cards.append(card)
            #print(winnable_cards)
            if winnable_cards:
                action = np.random.choice(winnable_cards)
            else:
                for card in legal_actions:
                    if lowest_card == None:
                        lowest_card = card
                    elif rank2int(card[0]) < rank2int(lowest_card[0]):
                        lowest_card = card
                    action = lowest_card

        #print(legal_actions, winnable_cards, action)
        #print(action)
        return action

    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state), []

    @staticmethod
    def can_win(played_cards, card, trump, lead_suit):
        played_cards.append(card)
        winning_card = None
        for card in played_cards:
            if winning_card == None:
                winning_card = card
            elif card[1] == trump:
                if winning_card[1] == trump:
                    if rank2int(card[0]) > rank2int(winning_card[0]):
                        winning_card = card
                else:
                    winning_card = card
            elif card[1] == lead_suit:
                if winning_card[1] == lead_suit:
                    if rank2int(card[0]) > rank2int(winning_card[0]):
                        winning_card = card

        if winning_card == card:
            return True
        else:
            return False

class WhistRuleModelV1(Model):
    ''' Whist Rule Model version 1
    '''

    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard.make('whist')

        rule_agent = WhistRuleAgentV1()
        self.rule_agents = [rule_agent for _ in range(env.player_num)]

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.rule_agents

    @property
    def use_raw(self):
        ''' Indicate whether use raw state and action

        Returns:
            use_raw (boolean): True if using raw state and action
        '''
        return True



