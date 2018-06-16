# coding=utf-8
"""

"""

from pick_three.digits_class import Digits
from pick_three.game import Game
from pick_three.ticket import Ticket, BetType, ComboType


def test_check_three_way_box():
    game = Game()
    ticket = Ticket(ComboType.SIMPLE)

    ticket.set_chosen(113)
    ticket.add_bet(BetType.THREE_WAY_BOX, 1)
    assert game.check_ticket(ticket, 311), game.check_ticket(ticket, 311)
    assert game.check_ticket(ticket, 131)
    assert game.check_ticket(ticket, 113)
    ticket.set_chosen(131)
    assert game.check_ticket(ticket, 311)
    assert game.check_ticket(ticket, 131)
    assert game.check_ticket(ticket, 113)
    ticket.set_chosen(311)
    assert game.check_ticket(ticket, 311)
    assert game.check_ticket(ticket, 131)
    assert game.check_ticket(ticket, 113)

    ticket.set_chosen(113)
    assert game.check_ticket(ticket, 111)
    assert game.check_ticket(ticket, 111)
    assert game.check_ticket(ticket, 111)


def test_check_six_way_box():
    game = Game()
    ticket = Ticket(ComboType.SIMPLE)
    ticket.add_bet(BetType.SIX_WAY_BOX, 1)
    winners = [123, 132, 213, 312, 321]
    ticket.set_chosen(123)
    for winner in winners:
        assert game.check_ticket(ticket, winner)
    ticket.set_chosen(321)
    for winner in winners:
        assert game.check_ticket(ticket, winner)
    ticket.set_chosen(213)
    for winner in winners:
        assert game.check_ticket(ticket, winner)

    for winner in winners:
        if winner - 1 < 0 or winner - 1 > 999:
            continue
        ticket.set_chosen(winner - 1)
        if ticket._chosen.chosen in winners:
            continue
        assert not game.check_ticket(ticket, winner), (str(ticket._chosen), winner, game.check_ticket(ticket, winner))


def test_check_front_pair():
    game = Game()
    ticket = Ticket(ComboType.SIMPLE)
    ticket.add_bet(BetType.FRONT_PAIR, 1)
    ticket.set_chosen(123)
    for x in range(0, 10):
        draw = int("12" + str(x))
        assert game.check_ticket(ticket, draw), (ticket._chosen, draw)


def test_check_back_pair():
    game = Game()
    ticket = Ticket(ComboType.SIMPLE)

    ticket.add_bet(BetType.BACK_PAIR, 1)
    ticket.set_chosen(123)
    for x in range(0, 10):
        assert game.check_ticket(ticket, int(str(x) + "23"))


def test_straight():
    game = Game()
    ticket = Ticket(ComboType.SIMPLE)

    ticket.add_bet(BetType.STRAIGHT, 1)

    for winner in range(0, 999):
        ticket.set_chosen(winner)
        assert game.check_ticket(ticket, winner)

    for winner in range(0, 999):
        if winner - 1 < 0 or winner - 1 > 999:
            continue
        ticket.set_chosen(winner -1)
        assert not game.check_ticket(ticket, winner)


def test_three_way_combo():
    game = Game()
    ticket = Ticket(ComboType.THREE_WAY_COMBINATION)
    ticket.set_chosen(113)
    ticket.add_three_way_combo(1)
    for winner in [113, 311, 131]:
        ticket.set_chosen(winner)
        assert game.check_ticket(ticket, winner)


def test_six_way_combo():
    game = Game()
    ticket = Ticket(ComboType.SIX_WAY_COMBINATION)
    ticket.set_chosen(123)
    ticket.add_six_way_combo(0.5)
    six_winners = [123, 132, 213, 231, 312, 321]
    for winner in six_winners:
        ticket.set_chosen(winner)
        assert game.check_ticket(ticket, winner)
