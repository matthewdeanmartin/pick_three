# coding=utf-8
"""
Classes to represent a bet.
"""

from enum import Enum, unique

from pick_three.digits_class import Digits


@unique
class BetType(Enum):
    """
    All the simple, non-combo bets
    """
    STRAIGHT = 1
    THREE_WAY_BOX = 2
    SIX_WAY_BOX = 3
    FRONT_PAIR = 4
    BACK_PAIR = 5


@unique
class ComboType(Enum):
    """
    The combination bets, all made of 2+ simple bets
    """
    SIMPLE = 1
    THREE_WAY_COMBINATION = 2
    SIX_WAY_COMBINATION = 3
    STRAIGHT_BOX_THREE_WAY = 4
    STRAIGHT_BOX_SIX_WAY = 5


class Bet(object):
    """
    Represents a bet type and an amount. Can only represent a simple bet.
    """
    def __init__(self, pick, bet_type, amount, chosen):
        """

        :type pick: int
        :type bet_type: BetType
        :type amount: int|float
        :type chosen: Digits
        """
        self.pick = pick
        if self.pick != 3:
            raise NotImplementedError("Haven't implemented pick 4")
        self.bet_type = bet_type
        self.amount = amount
        self.chosen = chosen

    def validate(self):
        """
        Is this an screwed up bet?
        :return:
        """
        if self.bet_type == BetType.THREE_WAY_BOX:
            if not self.chosen.has_double():
                raise TypeError("Three way box demands a bet with at at least a pair")
        elif self.bet_type == BetType.SIX_WAY_BOX:
            if not self.chosen.all_different():
                raise TypeError("Six way box demands a bet with all different digits")

    def price_multiplier(self):
        """
        What does this ticket costs.

        Right now assumes minimum of $1. Actual minimum is $0.50 for some bets
        :return:
        """
        if self.bet_type == BetType.STRAIGHT:
            return 1
        elif self.bet_type == BetType.THREE_WAY_BOX:
            return 3
        elif self.bet_type == BetType.SIX_WAY_BOX:
            return 3
        elif self.bet_type == BetType.FRONT_PAIR:
            return 1
        elif self.bet_type == BetType.BACK_PAIR:
            return 1
        # elif self.bet_type == BetType.THREE_WAY_COMBINATION:
        #     return 3
        # elif self.bet_type == BetType.SIX_WAY_COMBINATION:
        #     return 6
        # elif self.bet_type == BetType.STRAIGHT_BOX_THREE_WAY:
        #     return 1
        # elif self.bet_type == BetType.STRAIGHT_BOX_SIX_WAY:
        #     return 1
        else:
            raise TypeError("Don't know that bet type. {0}".format(self.bet_type))


class SheetOfTickets(object):
    """
    For modeling 5 tickets per sheet, multiple drawings, mulitple days, etc.
    """

    def __init__(self):
        self.tickets = []

    def add_ticket(self, ticket):
        """

        :type ticket:Ticket
        :return:
        """
        self.tickets.append(ticket)

    def resolve_tickets(self):
        raise NotImplementedError()


# TODO: model splits, actual MD payoff chart
class Ticket(object):
    """
    Represents a single bet (including combo bets)
    """

    def __init__(self, combo_type):
        """
        Can reprsent a simple or combo bet.
        :type combo_type:
        """
        self.state = "MD"
        self.pick = 3
        self._chosen = None

        self.combo_type = combo_type
        self.bets = []

        self.ticket_ranges = {
            "bet_type": [
                BetType.STRAIGHT,
                BetType.THREE_WAY_BOX,
                BetType.SIX_WAY_BOX,
                BetType.FRONT_PAIR,
                BetType.BACK_PAIR,

            ],
            "combo_type": [
                ComboType.SIMPLE,
                ComboType.THREE_WAY_COMBINATION,
                ComboType.SIX_WAY_COMBINATION,

                ComboType.STRAIGHT_BOX_THREE_WAY,
                ComboType.STRAIGHT_BOX_SIX_WAY,
            ],
            "bet_descriptions": ["straight",
                                 "3-way box",
                                 "6-way box",
                                 "front pair",
                                 "back pair"],

            "combo_descriptions": ["simple",
                                   "3-way combination",
                                   "6-way-combination",
                                   "straight/box 3-way",
                                   "straight/box 6-way"]
        }

        # Set a default
        self.set_chosen(123)

    def set_chosen(self, digits):
        """

        :type digits: int
        :return:
        """

        self._chosen = Digits(digits, pick=self.pick)
        for bet in self.bets:
            bet.chosen = self._chosen

    def add_bet(self, bet_type, amount):
        """
        Bets added to a list. Do not manipulate that list directly.
        :type bet_type: BetType
        :type amount: int|float
        :return:
        """
        if amount != .5 and amount != 1:
            raise TypeError("Expected bet amounts of $1 or $0.50")
        bet = Bet(self.pick, bet_type, amount, self._chosen)
        self.bets.append(bet)

    def add_six_way_combo(self, amount):
        """
        Configure a six way combo correctly (six straight bets, costs $3 or $6
        :type amount: int|float
        :return:
        """

        for digit in self._chosen.six_ways():
            bet = Bet(self.pick, BetType.STRAIGHT, amount, digit)
            self.bets.append(bet)
        if len(self.bets) != 6:
            raise TypeError("Expected 3 bets in a 3 way.")

    def add_three_way_box_combo(self, amount):
        """
        Add the two simple bets to make a three way box combo
        :type amount: int|float
        :return:
        """
        self.add_bet(BetType.THREE_WAY_BOX, amount)
        self.add_bet(BetType.STRAIGHT, amount)

    def add_six_way_box_combo(self, amount):
        """
        Add the two simple bets to make a six way box combo
        :type amount: int|float
        :return:
        """
        self.add_bet(BetType.SIX_WAY_BOX, amount)
        self.add_bet(BetType.STRAIGHT, amount)

    def add_three_way_combo(self, amount):
        """
        Add three bets on three different numbers. Two will be losers.
        :type amount: int|float
        :return:
        """
        has_double, doubled = self._chosen.has_double()
        if not has_double:
            raise TypeError("Not a valid ticket, need doubled digit " + str(self._chosen))
        for digit in self._chosen.three_ways():
            bet = Bet(self.pick, BetType.STRAIGHT, amount, digit)
            self.bets.append(bet)
        if len(self.bets) != 3:
            raise TypeError("Expected 3 bets in a 3 way.")

    def chart(self, state):
        """
        Payoff charts, which vary by state
        :type state: str
        :return:
        """
        chart = {
            BetType.STRAIGHT: 500,  # 1 in 1000
            BetType.THREE_WAY_BOX: 160,  # 3 in 1000
            BetType.SIX_WAY_BOX: 80,  # 6? in 1000
            BetType.FRONT_PAIR: 50,  # 10 in 1000 -- same as pick 2?
            BetType.BACK_PAIR: 50,  # 10 in 1000 -- same as pick 2?
            # BetType.THREE_WAY_COMBINATION: 500,  # but cost $3
            # BetType.SIX_WAY_COMBINATION: 500,  # but costs $6
            #
            # BetType.STRAIGHT_BOX_THREE_WAY: [330, 80],  # straight/box -- box only
            # BetType.STRAIGHT_BOX_SIX_WAY: [290, 40]  # straight/box -- box only
        }
        if state == "MD":
            return chart

    def payoffs(self, state, bet_type, amount):
        """
        Payoff chart. Varies by state.
        :type state: str
        :type bet_type: BetType
        :rtype: int|float
        """
        chart = {
            BetType.STRAIGHT: 500,  # 1 in 1000
            BetType.THREE_WAY_BOX: 160,  # 3 in 1000
            BetType.SIX_WAY_BOX: 80,  # 6? in 1000
            BetType.FRONT_PAIR: 50,  # 10 in 1000 -- same as pick 2?
            BetType.BACK_PAIR: 50,  # 10 in 1000 -- same as pick 2?
            # BetType.THREE_WAY_COMBINATION: 500,  # but cost $3
            # BetType.SIX_WAY_COMBINATION: 500,  # but costs $6
            #
            # BetType.STRAIGHT_BOX_THREE_WAY: [330, 80],  # straight/box -- box only
            # BetType.STRAIGHT_BOX_SIX_WAY: [290, 40]  # straight/box -- box only
        }
        if state == "MD":
            return self.chart(state)[bet_type] * amount
        else:
            raise TypeError("Haven't implemented game for {0}".format(state))

    def combo_payoff(self, state, combo_type):
        raise NotImplementedError()

    def price(self):
        """

        :type: int|float
        """
        total = 0
        for bet in self.bets:
            total += bet.amount
        if total == 0:
            raise TypeError("These tickets aren't free dude.")
        return total

    def check_valid(self):
        """
        Does this Ticket have problems?
        :rtype: bool
        """

        if len(self.bets) < 1:
            raise TypeError("Need at least one bet")
        if len(self.bets) > 2:
            raise TypeError("Should only need 1 or 2 bets to model everything")
