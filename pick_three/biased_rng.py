# coding=utf-8
"""
Attempt to creat an RNG that picks numbers like humans

# favors date parts (1-31, 1-12, 19/20, 50-99/00-18)
# seeks/avoids patterns (i.e. 1,2,3,4,5 or 2,22,32,42)
# favors past winning numbers
# favors culturally meaningful numbers, 777, 888, etc.

# http://ww2.amstat.org/publications/jse/v13n2/mecklin.html

Past number strategies
Choosing winning combinations from previous draws
Modifying previous winning combinations (e.g. adding 1 to each number in a previous winning combination)
Choosing “hot” or “cold” numbers (a statistically nonsensical strategy suggested in many of the lay books about lotteries)

"Numerology"
factors of 1, 2, 3, etc., eg. 7, 14, 21, etc
Choosing arithmetic progressions (e.g. 1-2-3-4-5-6 or 2-5-8-11-14-17)
Choosing powers of 2 (e.g. 1-2-4-8-16-32)
Choosing perfect squares (e.g. 1-4-9-16-25-36)
Choosing all prime numbers (e.g. 2-3-5-7-11-13)
Choosing Fibonacci numbers (e.g. 1-2-3-5-8-13)

Dates
Choosing only numbers that are less than or equal to 31; many people choose numbers based on birthdays, anniversaries, etc.
"""
import random
from datetime import date, timedelta
from typing import List


class BiasedRng(object):
    """
    Birthday numbers. Simulate what happens if you only pick birthday numbers.
    Against an unbiased state RNG, you expect a higher risk of capped payouts from
    too many people winning, otherwise no change-- all numbers are just as good as
    any other.

    If you were playing keno with friends (and not the state), one player could exploit the fact that
    the other is using a BiasedRng.
    """

    def __init__(self) -> None:
        self.pick = 3

    def pretty_patterns(self) -> List[str]:
        """
        Repeating digits, etc.
        :return:
        """
        patterned_digits = []
        for i in range(0, 10):
            patterned_digits.append(str(i) * 4)

        for i in range(0, 10):
            if i + 3 > 9:
                break
            patterned_digits.append("{0}{1}{2}{3}"
                                    .format(i, i + 1,
                                            i + 2, i + 3))
        return patterned_digits

    def random_birthday(self) -> date:
        """
        Birthdays for people up to 80 years old.
        :return:
        """
        days = 365 * 80
        oldest_birthday = date.today() - timedelta(days=days)
        days_since_random_birthday = random.randint(0, days)
        return oldest_birthday + timedelta(days=days_since_random_birthday)

    def date_derived(self, value: date) -> List[str]:
        """
        Break date into part and return set of recombined parts with 4 digits
        :param value:
        :return:
        """
        # year
        da = str(value.day).zfill(self.pick)
        mo = str(value.month).zfill(self.pick)
        ye = str(value.year)[0:2]
        ar = str(value.year)[2:4]
        date_derived = {
            value.year,
            # US D/M
            int("{0}{1}".format(da, mo)),
            # Euro M/D
            int("{0}{1}".format(mo, da)),
            int("{0}{1}".format(mo, ar)),
        }

        if da.startswith("0"):
            d = da[1:2]
        else:
            d = ""

        if mo.startswith("0"):
            m = mo[1:2]
        else:
            m = ""

        if d and m:
            date_derived.add(d + m + ar)
            date_derived.add(m + d + ar)

        return list(date_derived)


if __name__ == "__main__":
    rng = BiasedRng()
    bday = rng.random_birthday()
    print(rng.pretty_patterns())
