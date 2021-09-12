## Auction class for evaluating unit tests

This Auction class can selectable introduce defects in the auction code,
for evaluating sensitivity of unit test code:

There are 6 scenarios:

1. Correct. All methods work according to documentation.
2. Reject bid if `bid == best_bid()+increment`. Otherwise correct.
3. Accept any bid greater than `best_bid()`. It should require a min increment.
4. Accept bid when auction is stopped.  It should throw AuctionError.
5. If bid is too low then silently reject it, don't raise an exception.
6. a) Bidding works correctly, but winner is always last person to bid, even
   if his bid is invalid. And, b) allows bidder name to be spaces "  ".

Use an environment variable TESTCASE to select the variant to use:

export TESTCASE=1
python3 -m unittest -v auction_test.py
