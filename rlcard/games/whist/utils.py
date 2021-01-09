import os
import json
import numpy as np
from collections import OrderedDict

import rlcard

from rlcard.core import Card

ROOT_PATH = rlcard.__path__[0]

with open(os.path.join(ROOT_PATH, 'games/whist/jsondata/action_space.json'), 'r') as file:
    ACTION_SPACE = json.load(file, object_pairs_hook=OrderedDict)
    ACTION_LIST = list(ACTION_SPACE.keys())

SUIT_MAP = {'H': 0, 'S': 1, 'D': 2, 'C': 3}

RANK_MAP = {'A': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
             '9': 8, 'T': 9, 'J': 10, 'Q': 11, 'K': 12}

def cards2list(cards):
    ''' Get the corresponding string representation of cards

    Args:
        cards (list): list of UnoCards objects

    Returns:
        (string): string representation of cards
    '''
    cards_list = []
    for card in cards:
        cards_list.append(card.__str__())
    return cards_list

def encode_hand(plane, hand):
    ''' Encode hand and represerve it into plane

    Args:
        plane (array): 3*4*15 numpy array
        hand (list): list of string of hand's card

    Returns:
        (array): 3*4*15 numpy array
    '''
    # plane = np.zeros((3, 4, 15), dtype=int)
    for card in hand:
        #print(card)
        rank = card[0]
        suit = card[1]
        rank = RANK_MAP[rank]
        suit = SUIT_MAP[suit]
        plane[suit][rank] = 1
    return plane

def encode_target(plane, target):
    ''' Encode target and represerve it into plane

    Args:
        plane (array): 1*4*15 numpy array
        target(str): string of target card

    Returns:
        (array): 1*4*15 numpy array
    '''
    if target:
        #print(target)
        rank = target[0]
        suit = target[1]
        rank = RANK_MAP[rank]
        suit = SUIT_MAP[suit]
        plane[suit][rank] = 1
    return plane