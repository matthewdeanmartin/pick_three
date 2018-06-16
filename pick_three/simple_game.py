# coding=utf-8
"""
Simulate pick 3 losses over a life time of daily/weekly playing.

Only models straight bets, so can't be used to compare bet types.
"""


import random

class Game(object):
    """
    Represents State Lottery Commision. The House.
    """

    def __init__(self):
        # does house start out with 0, causing initial jackpots to be low
        self.house = 0
        self.out = []
        self.type = "fair_game"  # or jackpot, or lotto
        self.house_type = "no_pockets"  # or deep pockets
        self.payoff = 500

        # state will stop selling a popular number if a payout would break the bank
        self.house_limits_per_number = 50

    def draw_winner(self):
        return random.randint(0, 999)

    def go(self):
        # essentially how long can you play before you can't continue.
        # if this was modeling a worker with income each year, not a constraint
        years = (82 - 18) / 2
        # self.initial = years * 365 # makes sense for modeling, say 5% annual income
        self.initial = 2000
        players = {

        }
        for p in range(0, 5):
            players[p] = {
                "bank": self.initial,
                "pick": self.draw_winner()
            }

        i = 0
        print("check : " + str(self.house + sum([x["bank"] for x in players.values()])))
        while True:
            i = self.round_and_around(i, players)
            players_standing = sum([1 for x in players.values() if x["bank"] > 0])
            if players_standing == 0:
                print()
                print("No one standing, Game over, house has {0}".format(self.house))
                print("check : " + str(self.house + sum([x["bank"] for x in players.values()])))
                self.summarize(players)
                break
            if players_standing == 1:
                print()
                player_standing = [key for key, value in players.items() if value["bank"] > 0][0]
                print(
                    "Only a single player standing, {0}. Game over, house has {1}".format(players_standing, self.house))
                print("check : " + str(self.house + sum([x["bank"] for x in players.values()])))
                self.summarize(players)
                break

            if i == 52 * years * 2:
                print("{0} years of bi-weekly drawings over, house holding {1}.".format(years, self.house))
                print("check : " + str(self.house + sum([x["bank"] for x in players.values()])))
                self.summarize(players)
                break

    def summarize(self, players):
        for id, player in players.items():
            print("=== player {0} ===".format(id))
            # play would like this to be 0
            net = player["bank"] - self.initial
            percent = net / self.initial
            print("Net {0}, {1:.2f}%".format(net, percent * 100))
        print("House has  {0}".format(self.house))

    def round_and_around(self, i, players):
        drawing = self.draw_winner()
        i += 1
        total = sum([x["bank"] for x in players.values()])

        for key, player in players.items():
            if player["bank"] <= 0:
                continue

            # buy ticket
            self.house += 1
            player["bank"] = player["bank"] - 1

            if player["bank"] <= 0:
                if key not in self.out:
                    print("player {0} ran out of money in {1} rounds".format(key, i))
                    self.out.append(key)

            if player["pick"] == drawing:
                if self.type == "jackpot":
                    print("round {0}:  player {1} won, jackpot of {2}".format(i, key, self.house))
                    player["bank"] = player["bank"] + self.house
                    self.house = 0
                else:
                    fixed = self.payoff
                    if self.house_type == "no_pockets" and self.house < fixed:
                        fixed = self.house

                    print("round {0}:  player {1} won, prize of {2}".format(i, key, fixed))
                    player["bank"] = player["bank"] + fixed
                    self.house = self.house - fixed
                break  # can't win twice on one game!
            if player["bank"] == (total + self.house):
                print("player {0} has all the money".format(key))
                print("rounds {0}".format(i))
                exit()
        return i

if __name__ == "__main__":
    game = Game()
    game.go()
