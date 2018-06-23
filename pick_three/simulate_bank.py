# coding=utf-8
"""
Someone somewhere suggested that the poor use pick 3 as a sort of self imposed forced savings with
a big handling fee. In otherwords, pick 3 is a weird bank.

So let's see how it performs.
"""
import random
import statistics
import numpy as np

from txtble import Txtble


class Bank(object):
    """
    AFAIK, no such bank exist
    """

    def __init__(self,
                 bet, amount, iterations,
                 include_irr=False,
                 npv_rate=.01):
        self.actuals = {}
        self.desired = []
        self.iterations = iterations
        self.deposit_amount = bet
        self.withdrawl_amount = amount
        self.stop = 52 * 2 * (82 - 24)
        self.include_irr = include_irr

        if include_irr:
            self.stop = 400
        self.payout_rate = 1000
        self.npv_rate= npv_rate
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
        t.headers = ["iteration", "win count", "sum", "count", "mean", "stddev", "npv", "pb period"]
        if self.include_irr:
            t.headers.append("irr")
        for key, value in self.actuals.items():
            pay_back_period = self.calculate_pay_back_period(value)

            try:
                stdev ="{0:.2f}".format(statistics.stdev(value))
            except statistics.StatisticsError:
                stdev = "N/A"
            row = [key,
                   sum([1 for x in value if x >0]),
                   sum(value), len(value),
                   "{0:.2f}".format(statistics.mean(value)),
                   stdev,
                   "{0:.1f}".format(np.npv(self.npv_rate, value)),
                   pay_back_period
                   ]
            if self.include_irr:
                row.append(round(np.irr(value), 5))

            t.append(row)
        print(t.show())

        # TODO: need stats library here.

    def calculate_pay_back_period(self, value):
        pay_back_period = 0
        net = 0
        for flow in value:
            pay_back_period += 1
            net += flow
            if net == 0:
                break
        return pay_back_period


if __name__ == "__main__":
    bank = Bank(bet=250,
                amount=25000,
                iterations=20,
                include_irr=True,
                npv_rate=0.001)
