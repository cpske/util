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
			echo "CASE 1: All methods work according to documentation. Your tests should PASS."
       		;;
    	2)
			echo "CASE 2: Some error in bidding. At least one test should FAIL."
			;;
		3) 
			echo "CASE 3: Some error in bidding. At least one test should FAIL."
			;;
		4)
			echo "CASE 4. Some error in auction control. At least one test should FAIL."
			;;
		5)
			echo "CASE 5. Some problem is silently ignored. At least one test should FAIL."
			;;
		6)
			echo "CASE 6. Some error in auction control. At least one test should FAIL."
			;;
		7)
			echo "CASE 7. Two errors in Auction. Do your tests detect BOTH defects?"
		esac
        drawline
		export TESTCASE=$testcase
		python3 -m unittest -v $TESTMODULE
		# wait til user presses enter
		read input
	done
}

runtests
