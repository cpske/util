#!/bin/bash

TESTMODULE="auction_test.py"
#TESTMODULE="test_auction2.py"

drawline( ) {
    echo "----------------------------------------------------------------------"
}
runtests( ) {
	for testcase in 1 2 3 4 5 6; do
        drawline
		case $testcase in
    	1)
			echo "CASE 1: All methods work according to documentation"
       		;;
    	2)
			echo "CASE 2: Rejects bids where bid == best_bid()+increment"
			;;
		3) 
			echo "CASE 3: Accept any bid > best_bid()"
			;;
		4)
			echo "CASE 4. Accept bid when auction is stopped [should throw AuctionError]"
			;;
		5)
			echo "CASE 5. If bid is too low it don't do anything (no exception)"
			;;
		6)
			echo "CASE 6. Last bidder is winner, even if bid is rejected."
			echo "        Allow bidder name to be whitespace."
		esac
        drawline
		export TESTCASE=$testcase
		python3 -m unittest -v $TESTMODULE
		# wait til user presses enter
		read input
	done
}

runtests
