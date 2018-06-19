# coding=utf-8
"""

Which bet type is worst? Straight, front pair, end pair, etc.

I predict combo bets are worst & straight/front pair/end pair are
equally least bad.
"""
from txtble import Txtble

from pick_three.game import Game
from pick_three.ticket import BetType, Ticket, ComboType


def which_is_worst(rounds=100):
    worst_data = []
    for combo in ComboType:
        if combo == ComboType.SIMPLE:
            continue
        game = Game()
        winnings = 0
        gambled = 0

        # sample ticket needs a number with a double or 3-way box's don't happen
        game_count = 0
        win_count = 0

        for i in range(0, rounds):
            ticket = Ticket(combo)
            if combo == ComboType.THREE_WAY_COMBINATION:
                ticket.set_chosen(113)
                ticket.add_three_way_combo(0.5)
            elif combo == ComboType.SIX_WAY_COMBINATION:
                ticket.set_chosen(123)
                ticket.add_six_way_combo(0.5)
            elif combo == ComboType.STRAIGHT_BOX_SIX_WAY:
                ticket.set_chosen(123)
                ticket.add_six_way_box_combo(0.5)
            elif combo == ComboType.STRAIGHT_BOX_THREE_WAY:
                ticket.set_chosen(113)
                ticket.add_three_way_box_combo(0.5)
            else:
                raise TypeError("Don't have this compo yet.")
            game_count += 1

            for bet in ticket.bets:
                gambled += bet.amount
            drawing = game.draw_winner()

            if game.check_ticket(ticket, drawing):
                win_count += 1
                prize = 0
                for bet in ticket.bets:
                    prize += ticket.payoffs(ticket.state, bet.bet_type, bet.amount)
                if isinstance(prize, list):
                    winnings += prize[1]
                else:
                    winnings += prize
            net = winnings - gambled

        try:
            percent_won = winnings / gambled
        except ZeroDivisionError:
            percent_won = "N/A"

        try:
            percent_by_count = win_count/game_count
        except ZeroDivisionError:
            percent_by_count= "N/A"

        try:
            odds = game_count / win_count
        except ZeroDivisionError:
            odds = "N/A"

        worst_data.append([
            combo,

            winnings,
            gambled,
            gambled - winnings,
            "{0:.4f}".format(percent_won),
            "{0:.4f}".format(percent_by_count),
            "{0:.2f}".format(odds)
        ])

    for bet_type in [BetType.STRAIGHT,
                     BetType.THREE_WAY_BOX,
                     BetType.SIX_WAY_BOX,
                     BetType.FRONT_PAIR,
                     BetType.BACK_PAIR]:
        ticket = Ticket(ComboType.SIMPLE)
        game = Game()

        winnings = 0
        gambled = 0

        # sample ticket needs a number with a double or 3-way box's don't happen
        game_count = 0
        win_count = 0
        ticket.add_bet(bet_type, 1)
        for i in range(0, rounds):

            game_count += 1
            if bet_type in (BetType.THREE_WAY_BOX,):
                ticket.set_chosen(113)
            if bet_type in (BetType.SIX_WAY_BOX,):
                ticket.set_chosen(123)

            for bet in ticket.bets:
                gambled += bet.amount
            drawing = game.draw_winner()


            if game.check_ticket(ticket, drawing):
                win_count += 1
                prize = 0
                for bet in ticket.bets:
                    prize += ticket.payoffs(ticket.state, bet.bet_type, bet.amount)
                if isinstance(prize, list):
                    winnings += prize[1]
                else:
                    winnings += prize
            net = winnings - gambled

        try:
            percent_won = winnings / gambled
        except ZeroDivisionError:
            percent_won = "N/A"

        try:
            percent_by_count = win_count/game_count
        except ZeroDivisionError:
            percent_by_count= "N/A"

        try:
            odds = game_count / win_count
        except ZeroDivisionError:
            odds = "N/A"

        worst_data.append([
            bet_type,
            winnings,
            gambled,
            gambled - winnings,
            "{0:.4f}".format(percent_won),
            "{0:.4f}".format(percent_by_count),
            "{0:.2f}".format(odds)
        ])

    t = Txtble()
    t.headers = ["bet type", "winnigs", "gambled", "lost", "percent_won", "percent by count", "odds"]

    for row in worst_data:
        t.append(row)
    print(t.show())


if __name__ == "__main__":
    life_time_of_gambing = 2 * 52 * (82 - 21)
    which_is_worst(rounds=life_time_of_gambing)
