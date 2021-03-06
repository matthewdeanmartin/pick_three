# coding=utf-8
"""
Represents a pick 3 or pick 4 or pick-n
"""

class DigitsException(Exception):
    pass

class Digits(object):
    """
    Handles zero filling, common property checks.
    """
    def __init__(self, chosen, pick):
        """
        Initialize with some values that we'll need later on
        :type chosen: str, int
        :type pick: int
        """
        try:
            numeric_chosen = int(chosen)
        except:
            raise DigitsException("Chosen must be valid int")

        if pick < 0:
            raise DigitsException("Need positive digits")
        if numeric_chosen < 0:
            raise DigitsException("Need positive chosen")
        if int(chosen) > pow(10, pick):
            raise DigitsException("Chosen too big for pick, max {0}".format(pow(10, pick)))
        if not self.in_range(numeric_chosen, pick):
            # dupe check?
            raise DigitsException("Not numeric or out of range")

        self.pick = pick
        self.chosen = str(numeric_chosen).zfill(self.pick)
        self._dist = None

    def in_range(self, number, pick):
        """
        Verify if the number is the right length and is a number
        :type number: int|str
        :type pick: int
        :rtype: bool
        """
        if len(str(number).zfill(pick)) != pick:
            return False
        for char in str(number):
            if char not in "0123456789":
                return False
        return True

    def get_dist(self):
        """
        Count of each digit occurance in the number
        :return:
        """
        if self._dist is None:
            self._dist = {}
            for char in self.chosen:
                if char in self._dist:
                    self._dist[char] += 1
                else:
                    self._dist[char] = 1
        return self._dist

    def has_double(self):
        """
        Does it have a double digit.
        :return:
        """
        has_double = False
        doubled = None
        for digit, count in self.get_dist().items():
            if count >= 2:
                has_double = True
                doubled = digit
        return has_double, doubled

    def all_different(self):
        """
        Hell if I remember what I was doing here.
        :return:
        """
        has_double = False
        doubled = None
        for digit, count in self.get_dist().items():
            if count >= 2:
                has_double = True
                doubled = digit
        return has_double, doubled

    def all_unique(self):
        """
        Check if all digits are unique
        :return:
        """
        return len(set(self.chosen)) == self.pick

    def six_ways(self):
        """
        Generate the six ways given a suitable number
        :return:
        """
        if not self.all_unique():
            raise DigitsException("Can't do a 6 way unless all digits different, have {0}".format(self.chosen))

        ways = set()

        # TODO: support pick 4?
        for char in self.chosen:
            for char2 in self.chosen:
                for char3 in self.chosen:
                    if len({char, char2, char3}) == self.pick:
                        ways.add(char + char2 + char3)

        # ugh, I hate this.
        # first = self.chosen[0]
        # middle = self.chosen[1]
        # last = self.chosen[1]
        # ways = [
        #     first + middle + last,
        #     first + last + middle,
        #     middle + first + last,
        #     middle + last + first,
        #     last + first + middle,
        #     last + middle + first
        # ]
        if len(ways) != 6:
            raise DigitsException("Six way expected to have six ways.")

        return [Digits(value, self.pick) for value in ways]

    def three_ways(self):
        """
        Generate the 3 ways give a suitable number.
        :return:
        """
        if not self.has_double():
            raise DigitsException("Can't do a 3 way if no doubled digit.")

        ways = set()
        has_double, doubled = self.has_double()

        not_doubled = None
        for char in self.chosen:
            if char == doubled:
                continue
            else:
                not_doubled = char
                break

        # I hate this code too.
        ways = [
            not_doubled + doubled + doubled,
            doubled + not_doubled + doubled,
            doubled + doubled + not_doubled,
            ]


        if len(ways) != 3:
            raise DigitsException("Three way expected to have three ways.")
        return [Digits(value, self.pick) for value in ways]


    def __str__(self):
        """
        This class is a fance wrapper around a string version of a number.
        :return:
        """
        return self.chosen

    def __eq__(self, other):
        """
        Just compare the string value. It is almost a value type.
        :type other: Digits
        :rtype: bool
        """
        return self.chosen == other.chosen