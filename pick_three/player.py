# coding=utf-8
"""
Represents the person, their bank account, etc.
"""
from pick_three.digits_class import Digits
from pick_three.game import Game
from pick_three.ticket import Ticket


class Strategy(object):
    def __init__(self, maximum_loss=0, sufficient_win=0):
        self.maximum_loss = 0
        self.sufficient_win = 0

class Player(object):
    def __init__(self, bank, strategy):
        """

        :type bank: int|float
        :type strategy: Strategy
        """
        self.bank = 0

        # Gambler's ruin parameters
        self.strategy = strategy

        # For modeling biased number picking
        self.rng = None




    def stop_playing(self):
        if self.bank < (-1 * self.strategy.maximum_loss):
            return True
        if self.bank > self.strategy.sufficient_win:
            return True
        return False
