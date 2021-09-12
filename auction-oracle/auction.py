"""
A unit testing problem that requires testing of behavior
according to a specification, not just testing methods..
"""
import os
import re

class Auction:
    """An auction where people can submit bids for an item.
       One Auction instance is for bidding on a single item.

       The rules on an auction are:
       1. a person can submit one or more bids with any price > 0
          and at least the best bid so far plus a minimum increment
          (min_increment, default is 1).
          If a bid is <= 0 then a ValueError is raised.
          If a bid is > 0 but too low then an AuctionError is raised.
       2. New bids must exceed the current best bid by a minimum
          increment, such as 1 or 0.01.
          This is specified as a parameter in the constructor.
       3. The application must call auction.start() to enable bidding,
          and auction.stop() to disable bidding.
          start() and stop() can be called multiple times.
          auction.is_active() tests if bidding is enabled.
       4. Bids are allowed only when auction is active.
          If bid() is called when auction is inactive (stopped),
          an AuctionError is thrown.
       5. At any time, best_bid() can be called to get best bid so far,
          and winner() to find name of top bidder.

       Example:
       >>> auction = Auction("TDD with Python, 2nd Edition")
       >>> print("Minimum bid increment is", auction.increment)
       Minimum bid increment is 1
       >>> auction.start()
       >>> auction.bid("Jim", 250)
       >>> auction.bid("Harry", 300)
       >>> auction.bid(" biRd ", 400)
       >>> auction.best_bid()
       400
       >>> auction.winner()
       'Bird'
       >>> auction.bid("Jim", 400.1)
       Traceback (most recent call last):
         ...
       auction.AuctionError: Bid is too low
       >>> auction.bid("", 1000)
       Traceback (most recent call last):
         ...
       ValueError: Missing bidder name
       >>> auction.is_active()
       True
       >>> auction.stop()
       >>> auction.bid("Jim", 1000)
       Traceback (most recent call last):
         ...
       auction.AuctionError: Bidding not allowed now
       >>> auction.start()
       >>> auction.bid("mai", 402.50)
       >>> auction.best_bid()
       402.5
       >>> auction.winner()
       'Mai'
    """

    def __init__(self, auction_name, min_increment=1):
        """Create a new auction with given auction name.

           min_increment is the minimum amount that a new bid must
           exceed the current best bid.
        """
        if min_increment <= 0:
            # This isn't in the spec, so students shouldn't test it.
            # But some people did, anyway.
            raise ValueError("bidding increment must be positive")
        self.name = auction_name
        self.bids = {"no bids": 0}
        self.last_bidder = "no bids"
        self.increment = min_increment
        self.active = False
        # get testcase from the environment
        Auction.testcase = config('TESTCASE', default=0, cast=int)

    def start(self):
        """Enable bidding."""
        self.active = True

    def stop(self):
        """Disable bidding."""
        self.active = False

    def is_active(self):
        """Query if bidding is enabled. Returns True if bidding enabled."""
        return self.active or Auction.testcase == 6

    def bid(self, bidder_name, amount):
        """ Submit a bid to this auction.

            Args:
            bidder_name: name of bidder, a non-empty non-blank string.
                   Names are converted to Title Case, and excess space
                   inside and surrounding the string is removed.
                   " harry   haCkeR " is normalized to "Harry Hacker"
            amount: amount (int or float) of this bid. Must be positive
                   and greater than previous best bid by at least a
                   minimum bid increment, as described in class docstring.

            Raises:
            TypeError if bidder_name or amount are incorrect data types.
            ValueError if bidder_name or amount are have invalid values.
            AuctionError if bidding disabled or amount is too low
        """
        if not isinstance(bidder_name, str):
            raise TypeError("Bidder name must be a non-empty string")
        if not isinstance(amount, (int, float)):
            raise TypeError('Amount must be a number')
        if len(bidder_name) < 1:
            raise ValueError("Missing bidder name")
        # fix case of letters and remove whitespace
        bidder_name = Auction.normalize(bidder_name)
        # bug: should test non-empty bidder name AFTER normalization
        if Auction.testcase != 7 and len(bidder_name) < 1:
            raise ValueError("Bidder name may not be blank")
        if not self.accept_bid(bidder_name, amount):
            return
        # Accept the bid!
        self.bids[bidder_name] = amount

    def best_bid(self):
        """Return the highest bid so far."""
        return max(self.bids.values())

    def winner(self):
        """Return name of person who placed the highest bid."""
        # BUG: auction always uses last bidder as winner
        if Auction.testcase == 7: 
            return self.last_bidder
        best = self.best_bid()
        for (bidder, bid) in self.bids.items():
            if bid == best: return bidder
        # never reached
        return None

    @classmethod
    def normalize(cls, name):
        """Convert a name to title case, with excess spaces removed
           and surrounding whitespace removed.
        """
        namewords = re.split("\\s+", name.strip())
        name = " ".join(namewords)
        return name.title()

    def __str__(self):
        """Return a string describing this auction."""
        return f'Auction for {self.name}'

    def __repr__(self):
        if self.increment == 1:
            return f'Auction("{self.name}")'
        else:
            return f'Auction("{self.name}", min_increment={self.increment})'

    def accept_bid(self, bidder_name, amount):
        """ Test if
            - bid is valid (> 0)
            - bid is acceptable
            - bidding is allowed
            Return true if acceptable,
            throw AuctionError if auction is stopped (maybe),
            throw AuctionError if amount is too low (maybe),
            throw ValueError if amount <= 0,
            return false if bid unacceptable (maybe)
        """
        self.last_bidder = bidder_name
        if Auction.testcase == 2:
            # reject bids where amount == best_bid()+increment
            if not self.active:
                raise AuctionError("Bidding not allowed now")
            if amount <= 0:
                raise ValueError('Amount is invalid')
            # BUG:
            if amount <= self.best_bid() + self.increment:
                raise AuctionError("Bid is too low")
            return True
        if Auction.testcase == 3:
            # accept any bid > best_bid()
            if not self.active:
                raise AuctionError("Bidding not allowed now")
            if amount < 0:
                raise ValueError('Amount is invalid')
            # BUG:
            if amount <= self.best_bid():
                raise AuctionError("Bid is too low")
            return True
        if Auction.testcase == 4:
            # accept bids even when auction stopped
            #if not self.active:
            #    raise AuctionError("Bidding not allowed now")
            if amount < 0:
                raise ValueError('Amount is invalid')
            if amount < self.best_bid() + self.increment:
                raise AuctionError("Bid is too low")
            return True
        if Auction.testcase == 5:
            # quietly reject too low bids w/o raising exception
            if not self.active:
                raise AuctionError("Bidding not allowed now")
            if amount < 0:
                return False
            if amount < self.best_bid() + self.increment:
                return False
            return True
        # Otherwise run the default case (all behavior correct)
        # Auction.testcase == 1:
        if not self.active:
            raise AuctionError("Bidding not allowed now")
        if amount <= 0:
            raise ValueError('Amount is invalid')
        # check if this is best bid so far
        if amount < self.best_bid() + self.increment:
            raise AuctionError("Bid is too low")
        return True


class AuctionError(Exception):
    """Exception to throw when an invalid Auction action is performed"""
    # Superclass provides all the behavior we need, so nothing to add here.
    pass


def config(envvar, default="", cast=None):
    """Like decouple.config, read a variable from the environment, 
    with optional casting.  This is so we don't require the decouple package.
    """
    value = os.getenv(envvar)
    if not value and default:
        value = default
    if value and cast:
        return cast(value)
    return value


def test_config():
    """Test the config method."""
    n = config('TESTCASE', default=9, cast=int)
    print('n is', type(n), ' n =', n)


# This doesn't work.
def run_tests():
    """Run the unit tests for 7 scenarios using this class."""
    import unittest
    for testcase in range(1, 8):
        print('#'*30, f"Test Case {testcase}", '#'*30)
        Auction.testcase = testcase
        unittest.main(module=auction_test, exit=False, verbosity=2)
        input('Press ENTER...')
