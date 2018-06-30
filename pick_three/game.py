# coding=utf-8
"""
Roughly represents the state that runs the lottery.

Does the drawing, interacts with players, keep track of state's bank account.
"""

import random

from pick_three.digits_class import Digits
from pick_three.player import Player
from pick_three.ticket import BetType, Ticket


class WinLose(object):
    def __init__(self):
        self.bets_won = []


    def winnings(self, state):
        won = 0
        for bet in self.bets_won:
            payoff = self.pay_off_lookup(state, bet.bet_type)
            won += bet.amount * payoff
        return won

    def pay_off_lookup(self, state, bet_type):
        chart = {
            "MD":{
                BetType.STRAIGHT: 500,  # 1 in 1000
                BetType.THREE_WAY_BOX: 160,  # 3 in 1000
                BetType.SIX_WAY_BOX: 80,  # 6? in 1000
                BetType.FRONT_PAIR: 50,  # 10 in 1000 -- same as pick 2?
                BetType.BACK_PAIR: 50,  # 10 in 1000 -- same as pick 2?
            },
            # DC is same as MD
            "DC":{
                BetType.STRAIGHT: 500,  # 1 in 1000
                BetType.THREE_WAY_BOX: 160,  # 3 in 1000
                BetType.SIX_WAY_BOX: 80,  # 6? in 1000
                BetType.FRONT_PAIR: 50,  # 10 in 1000 -- same as pick 2?
                BetType.BACK_PAIR: 50,  # 10 in 1000 -- same as pick 2?
            },
            "VA":{
                BetType.STRAIGHT: 500,  # 1 in 1000
                BetType.THREE_WAY_BOX: 160,  # 3 in 1000
                BetType.SIX_WAY_BOX: 80,  # 6? in 1000
                BetType.FRONT_PAIR: 50,  # 10 in 1000 -- same as pick 2?
                BetType.BACK_PAIR: 50,  # 10 in 1000 -- same as pick 2?
            },
            "NY": {
                BetType.STRAIGHT: 500,  # 1 in 1000
                BetType.THREE_WAY_BOX: 160,  # 3 in 1000
                BetType.SIX_WAY_BOX: 80,  # 6? in 1000
                BetType.FRONT_PAIR: 50,  # 10 in 1000 -- same as pick 2?
                BetType.BACK_PAIR: 50,  # 10 in 1000 -- same as pick 2?
            },
        }
        # NYC variation
        sum_of_numbers = {
            0:500,
            1:166,
            2:83,
            3:50,
            4:33,
            5:23.50,
            6:17.50,
            7:13.50,
            8:11,
            9:2,
            10:7.50,
            11:7,
            12:6.5,
            13:6.50,
            14:6.50,
            15:6.50,
            16:7,
            17:7.50,
            18:9,
            19:11,
            20:13.50,
            21:17.50,
            22:23.50,
            23:33,
            24:50,
            25:83,
            26:166,
            27:500
        }
        return chart[state][bet_type]





class Game(object):
    """
    Represents State Lottery Commision. The House.
    """

    def __init__(self):
        pass

    def record_play(self, player: Player, ticket:Ticket, winning_number: Digits):
        winning_bets = self.check_ticket(ticket, winning_number)

        for bet in winning_bets:
            wl = WinLose()
            winnings = wl.winnings(ticket.state)
            player.bank += winnings

    def check_ticket(self, ticket, draw):
        """
        Return complex object which CAN be evaluated as bool, but if you do, you
        might think all bets won when only some won.
        :type ticket: Ticket
        :type draw: Digits|int
        :return:
        """

        if isinstance(draw, int):
            draw = Digits(draw, ticket.pick)

        if ticket.pick != 3:
            raise TypeError("Pick 2, 4+ not implemented")

        if not ticket.bets:
            raise TypeError("Can't evaluate, ticket has no bets")



        winnig_bets =[]
        for bet in ticket.bets:
            chosen = bet.chosen

            if bet.bet_type == BetType.STRAIGHT:
                if chosen == draw:
                    winnig_bets.append(bet)
            elif bet.bet_type == BetType.THREE_WAY_BOX:
                if self.three_way_box(chosen, draw):
                    winnig_bets.append(bet)
            elif bet.bet_type == BetType.SIX_WAY_BOX:
                if self.six_way_box(chosen, draw, ticket):
                    winnig_bets.append(bet)
            elif bet.bet_type == BetType.FRONT_PAIR:
                if chosen.chosen[0:2] == draw.chosen[0:2]:
                    winnig_bets.append(bet)
            elif bet.bet_type == BetType.BACK_PAIR:
                if chosen.chosen[1:] == draw.chosen[1:]:
                    winnig_bets.append(bet)
            elif bet.bet_type == BetType.THREE_WAY_COMBINATION:

                # uh - oh... does this have 2 win pay offs?
                # A way to make 3 bets.
                # if players doesn't have double, something was wrong with ticket
                has_double, doubled = chosen.has_double()
                draw_has_double, draw_doubled = draw.has_double()
                if has_double and draw_has_double:
                    if set(chosen.chosen) == set(draw.chosen):
                        winnig_bets.append(bet)
            elif bet.bet_type == BetType.SIX_WAY_COMBINATION:
                # a six dollar bet.
                if len(set(chosen.chosen)) == 3 and len(set(draw.chosen)) == 3:
                    if set(chosen.chosen) == set(draw.chosen):
                        winnig_bets.append(bet)
            elif bet.bet_type == BetType.STRAIGHT_BOX_THREE_WAY:
                if self.three_way_box(chosen, draw) or chosen == draw:
                    winnig_bets.append(bet)
            elif bet.bet_type == BetType.STRAIGHT_BOX_SIX_WAY:
                if self.six_way_box(chosen, draw, ticket) or chosen == draw:
                    winnig_bets.append(bet)
            else:
                raise TypeError("Don't know that bet type. {0}".format(bet.bet_type))
        return winnig_bets

    def six_way_box(self, chosen, draw, ticket):
        """

        :type chosen: Digits
        :type draw: Digits
        :type  ticket: Ticket
        :return:
        """
        if not chosen.all_different() or not draw.all_different():
            return False
        if not draw.all_unique():
            return False
        six_way_possibilities = draw.six_ways()

        for digits in six_way_possibilities:
            if digits == chosen:
                return True
        return False

    def three_way_box(self, chosen, draw):
        """

        :type chosen: Digits
        :type draw: Digits
        :return:
        """
        if not draw.has_double():
            return False
        has_double, doubled = chosen.has_double()
        draw_has_double, draw_doubled = draw.has_double()
        if has_double and draw_doubled and doubled == draw_doubled:
            missing_count = 0
            for d_char in str(draw.chosen):
                if d_char not in str(chosen):
                    missing_count += 1
            return missing_count == 0
        return False

    def draw_winner(self):
        return random.randint(0, 999)
