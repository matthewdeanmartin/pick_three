# coding=utf-8

import random

class Bank(object):
    """
    AFAIK, no such bank exist
    """
    def __init__(self):
        self.actual = []

    def withdraw(self, amount):
        """
        Simulate how much you'd have to gamble to get x dollars back out of a fair game.
        :type amount: int|float
        :return:
        """
        while sum(self.actual) < amount:
            while random.randint(0, 1000) != 1:
                self.actual.append(-1)
            self.actual.append(999)
        print(self.actual)

if __name__ == "__main__":
    bank = Bank()
    bank.withdraw(500)
    print(len(bank.actual))
