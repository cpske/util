#!/bin/bash

TESTMODULE="test_bank_account.py"

drawline( ) {
    echo "----------------------------------------------------------------------"
}
runtests( ) {
	for testcase in 0 1 2 3 4 5 6 7; do
        echo ""
        drawline
		case $testcase in
    	0)
			echo "BANK ACCOUNT 0: All methods work according to specification. Tests should PASS."
			/bin/cp bank_correct.py bank_account.py
       		;;
    	*)
			echo "BANK ACCOUNT ${testcase}: Some defect in code. At least one test should FAIL."
			/bin/cp bank_bugs.py bank_account.py
			;;
		esac
        drawline
		export TESTCASE=$testcase
		python3 -m unittest -v $TESTMODULE
		# wait til user presses enter
		#read input
	done
}

runtests
