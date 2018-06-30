# coding=utf-8
"""

Game with competing agents. MA & NJ have pari-mutuel betting where X% of revenue is
shared among the winners.

This results in payouts different from the simple expected value.

"""
from pick_three.game import Game, Digits
from pick_three.player import Player, Strategy
from pick_three.ticket import Ticket, ComboType, BetType


def go():
    players = []
    strategy = Strategy(maximum_loss=100, sufficient_win=500)
    for _ in range(0, 10):
        players.append(Player(100, strategy))

    game = Game()
    ticket = Ticket(ComboType.SIMPLE)
    ticket.add_bet(BetType.STRAIGHT, 5)

    # x days of play
    for _ in range(0,10):
        winning_number = game.draw_winner()


        for player in players:
            game.record_play(player, ticket, winning_number )
            player.stop_playing()

