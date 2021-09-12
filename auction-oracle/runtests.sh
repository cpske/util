#!/bin/bash

TESTMODULE="auction_test.py"
#TESTMODULE="test_auction2.py"

drawline( ) {
    echo "----------------------------------------------------------------------"
}
runtests( ) {
	for testcase in 1 2 3 4 5 6 7; do
        drawline
		case $testcase in
    	1)
			echo "AUCTION CODE 1: All methods work according to specification. Your tests should PASS."
       		;;
    	2 | 3 | 4)
			echo "AUCTION CODE ${testcase}: Some error in auction. At least one test should FAIL."
			;;
		5)
			echo "AUCTION CODE 5: Some problem is silently ignored. At least one test should FAIL."
			;;
		6)
			echo "AUCTION CODE 6: Some error in auction control. At least one test should FAIL."
			;;
		7)
			echo "AUCTION CODE 7: Two errors in Auction. Do your tests detect BOTH defects?"
		esac
        drawline
		export TESTCASE=$testcase
		python3 -m unittest -v $TESTMODULE
		# wait til user presses enter
		#read input
	done
}

runtests
