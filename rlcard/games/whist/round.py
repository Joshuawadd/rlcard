from rlcard.core import Round

class WhistRound(Round):

    def __init__(self):
        ''' When the game starts, round id should be 1
        '''

        raise NotImplementedError

    


    def proceed_round(self, **kwargs):
        ''' Call other Classes's functions to keep the game running
        '''
        raise NotImplementedError