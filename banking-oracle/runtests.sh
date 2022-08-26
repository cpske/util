#!/bin/bash

TESTMODULE="test_bank_account.py"

if [ ! -f $TESTMODULE ]; then
	echo "No tests code $TESTMODULE"
	exit 9
fi

# arrays to record results. Elements are appended in runtests()
expect=("")
actual=("")

drawline( ) {
    echo "----------------------------------------------------------------------"
}
runtests( ) {
	for testcase in 1 2 3 4 5 6 7 8 9; do
        echo ""
        drawline
        # append new element to expect. All testcases should fail except one.
        expect+=("FAIL")
		case $testcase in
    	8)
			echo "BANK ACCOUNT 8: All methods work according to specification. Tests should PASS."
			/bin/cp bank_correct.py bank_account.py
			# this case should pass all tests
			expect[8]="OK"
       		;;
    	*)
			echo "BANK ACCOUNT ${testcase}: Some defect in code. At least one test should FAIL."
			/bin/cp bank_bugs.py bank_account.py
			;;
		esac
        drawline
		export TESTCASE=$testcase
		python3 -m unittest -v $TESTMODULE
		# record status
		if [ $? -eq 0 ]; then
			actual+=("OK")
		else
			actual+=("FAIL")
		fi
		# wait til user presses enter
		#read input
	done
}

showresults() {
    drawline
    echo "Results of Testing All Bank Account Codes"
    drawline
    echo "OK=all tests pass, FAIL=some tests fail"
    echo ""
    echo "Auction#  Expect  Actual"
    failures=0
    
	for testcase in ${!expect[@]}; do
        # didn't use element 0
        if [ $testcase -eq 0 ]; then continue; fi
        printf "%5d      %-4s     %s\n" ${testcase} ${expect[$testcase]} ${actual[$testcase]}
        if [ ${expect[$testcase]} != ${actual[$testcase]} ]; then
			failures=$(($failures+1))
		fi
	done
    correct=$((8-$failures))
	echo "$correct Correct  $failures Incorrect"
    exit $failures
}

runtests
showresults
