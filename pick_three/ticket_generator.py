# coding=utf-8
"""
Generate random tickets
"""

import random

from pick_three.ticket import Ticket, ComboType, BetType


def make_ticket(minimum_amount, maximum_amount, minimum_to_win):
    ticket = Ticket(ComboType.SIMPLE)
    ranges = ticket.ticket_ranges
    # for key, value in ranges.items():
    combo_types = ranges["combo_type"]
    bet_types = ranges["bet_type"]

    combo_type = combo_types[random.randint(0, len(combo_types) + 1)]
    random_ticket = Ticket(combo_type)

    amount = [1, 0.5][random.randint(0, 2)]
    if combo_type == ComboType.SIMPLE:
        bet_type = bet_types[random.randint(0, len(bet_types) + 1)]
        if bet_type == BetType.STRAIGHT:
            random_ticket.add_bet(bet_type, 1)
    elif combo_type == ComboType.THREE_WAY_COMBINATION:
        random_ticket.add_three_way_combo(1)
    elif combo_type == ComboType.SIX_WAY_COMBINATION:
        random_ticket.add_six_way_combo(1)
    elif combo_type == ComboType.STRAIGHT_BOX_THREE_WAY:
        random_ticket.add_three_way_box_combo(0.5)
    elif combo_type == ComboType.STRAIGHT_BOX_SIX_WAY:
        random_ticket.add_six_way_box_combo(0.5)
