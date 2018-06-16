# coding=utf-8

import random

class Bank(object):
    """
    AFAIK, no such bank exist
    """
    def __init__(self):
        self.actual = []

    def withdraw(self, amount):
        while sum(self.actual)<amount:
            while random.randint(0, 1000) != 1:
                self.actual.append(-1)
            self.actual.append(999)
        print(self.actual)

#if __name__ == "__main__":
    # bank = Bank()
    # bank.withdraw(500)
    # print(len(bank.actual))

import random
def withdraw(amount=500):
    history = []
    while sum(history)<amount:
        while random.randint(0, 1000) != 1:
            history.append(-1)
        history.append(999)
    print(len(history), history)
for _ in range(0,100):
    withdraw()