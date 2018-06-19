# coding=utf-8
import random
import statistics

from txtble import Txtble


class Bank(object):
    """
    AFAIK, no such bank exist
    """

    def __init__(self, bet, amount, iterations):
        self.actuals = {}
        self.desired = []
        self.iterations = iterations
        self.deposit_amount = bet
        self.withdrawl_amount = amount
        self.stop = 52 * 2 * (82 - 24)
        self.payout_rate = 1000

        self.desired_pattern()
        self.withdraw()
        self.compare_flows()

    def desired_pattern(self):
        """
        For comparing to preferred cash flow pattern
        :param deposit_amount: The amount bet each week/day etc.
        :type deposit_amount: int|float
        :param withdrawl_amount: The amount won at end
        :type withdrawl_amount: int|float
        :rtype: list[int|float]
        """
        for i in range(0, int(self.withdrawl_amount)):
            self.desired.append(self.deposit_amount)
        self.desired.append(self.withdrawl_amount)
        return self.desired

    def withdraw(self):
        """
        Simulate how much you'd have to gamble to get x dollars back out of a fair game.
        :type amount: int|float
        :return:
        """
        for i in range(0, self.iterations):
            actual = []
            self.withdrawl_loop(actual)
            self.actuals[i] = actual

    def withdrawl_loop(self, actual):
        loops = 0
        while sum(actual) < self.withdrawl_amount:
            while random.randint(0, 1000) != 1:
                loops += 1
                actual.append(self.deposit_amount * -1)
                if loops > self.stop:
                    break
            actual.append((self.deposit_amount * self.payout_rate) - self.deposit_amount)
            if loops > self.stop:
                break

    def compare_flows(self):
        print("Assuming a lifetime of tickets is {0} tickets.".format(self.stop))

        for key, value in self.actuals.items():
            compressed = []
            last = -1
            flow_count = 0
            for i in range(0, len(value)):
                #last
                if i == len(value) - 1:
                    compressed.append((flow_count, value[i]))
                    break  # out of inner

                if value[i] == value[i + 1]:
                    flow_count += 1
                else:
                    compressed.append((flow_count, value[i]))

        t = Txtble()
        t.headers = ["iteration", "sum", "count", "mean", "stddev"]
        print(self.actuals)
        for key, value in self.actuals.items():
            row = [key, sum(value), len(value),
                   "{0:.2f}".format(statistics.mean(value)),
                   "{0:.2f}".format(statistics.stdev(value))]
            t.append(row)
        print(t.show())

        # TODO: need stats library here.



if __name__ == "__main__":
    bank = Bank(5, 1000, 20)
