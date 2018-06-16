# coding=utf-8
"""
Just build each type of ticket.
"""

from pick_three.game import Game
from pick_three.player import Player
from pick_three.ticket import BetType, Ticket, ComboType, Bet

def test_straight_build():
    game = Game()
    ticket = Ticket(ComboType.SIMPLE)
    ticket.add_bet(BetType.STRAIGHT, 1)
    price = ticket.price()
    ticket.check_valid()
    game.check_ticket(ticket, ticket._chosen)



def test_3_way_box_build():
    game = Game()
    ticket = Ticket(ComboType.SIMPLE)
    ticket.add_bet(BetType.THREE_WAY_BOX, 1)
    price = ticket.price()
    ticket.check_valid()
    game.check_ticket(ticket, ticket._chosen)


def test_straight_3_way_box_combo():
    game = Game()
    ticket = Ticket(ComboType.SIMPLE)
    ticket.set_chosen(344)
    ticket.add_three_way_box_combo(0.5)
    price = ticket.price()
    ticket.check_valid()
    result = game.check_ticket(ticket, ticket._chosen)
    print(result)

def test_straight_6_way_box_combo():
    game = Game()
    ticket = Ticket(ComboType.SIMPLE)
    ticket.set_chosen(987)
    ticket.add_bet(BetType.SIX_WAY_BOX, .5)
    ticket.add_bet(BetType.STRAIGHT, 0.5)
    price = ticket.price()
    ticket.check_valid()
    result = game.check_ticket(ticket, ticket._chosen)
    print(result)