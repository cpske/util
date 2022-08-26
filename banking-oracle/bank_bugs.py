"""Buggy bank account.  

Select a bug using environment variable TESTCASE with value 0 ... 7.
"""
import os
from money import Money
from check import Check

# Constants for errors

# available computed incorrectly when check is on hold
BUG_AVAILABLE_BALANCE = 1
# cannot withdraw exactly available amount
BUG_CANT_WITHDRAW_AVAILABLE = 2
# can clear any check (no exception raised)
BUG_CLEAR_ANY_CHECK = 3
# can deposit money with value 0
BUG_DEPOSIT_ZERO = 4
# can deposit a check more than once
BUG_DUPLICATE_CHECK = 5
# withdraw an amount too large returns None instead of raise exception
BUG_WITHDRAW_FAILS_SILENTLY = 6
# value of uncleared checks not included in balance
BUG_BALANCE_EXCLUDES_HOLDS = 7
# the minimum balance requirement is not enforced  
BUG_MINIMUM_IS_IGNORED = 9

class BankAccount:
	"""
	A BankAccount with a minimum required balance (default is 0)
	that accepts deposit of Money or Checks.  The balance is always the
	total of deposits minus withdraws, but the value of a check is not 
	available for withdraw until `clear_check(check)` is called.

	The available balance (`available` property) is the amount that can
	be withdrawn so that a) no not-yet-clear checks are withdrawn, and
	b) the balance after withdraw is at least the minimum balance. 

	>>> acct = BankAccount("Taksin Shinawat",1000)  # min required balance is 1,000
	>>> acct.balance
	0.0
	>>> acct.available
	0.0
	>>> acct.min_balance
	1000.0
	>>> acct.deposit( Money(10000) )   # deposit 10,000 cash
	>>> acct.balance
	10000.0
	>>> acct.available
	9000.0
	>>> c = Check(40000)
	>>> acct.deposit(c)				# deposit check for 40,000
	>>> acct.balance
	50000.0
	>>> acct.withdraw(30000)		   # try to withdraw 30,000
	Traceback (most recent call last):
	   ...
	ValueError: Amount exceeds available balance
	>>> acct.clear_check(c)
	>>> acct.available
	49000.0
	>>> acct.withdraw(30000)		   # try to withdraw 30,000
	Money(30000)
	>>> acct.balance
	20000.0
	>>> acct.withdraw(20000)		   # try to withdraw EVERYTHING
	Traceback (most recent call last):
	   ...
	ValueError: Amount exceeds available balance
	>>> acct.withdraw(15000)
	Money(15000)
	>>> acct.balance
	5000.0
	"""

	def __init__(self, name: str, min_balance: float = 0.0):
		"""Create a new account with given name.

		Args:
			name - the name for this account
			min_balance - the minimum required balance, a non-negative number.
				Default min balance is zero.
		"""
		# you don't need to test min_balance < 0. It's too trivial.
		assert min_balance >= 0, "min balance parameter must not be negative"
		self.__name = name
		self.__balance = 0.0
		self.__min_balance = float(min_balance)
		# checks deposited and waiting to be cleared
		self.__pending_checks = []
		self.__deposited_checks = []
		# variable for which bug to use
		self.bug = int(os.getenv('TESTCASE','0'))
	
	@property
	def balance(self) -> float:
		"""Balance in this account (float), as a read-only property"""
		if self.bug == BUG_BALANCE_EXCLUDES_HOLDS:
			hold_amount = sum([chk.value for chk in self.__pending_checks])
		else:
			hold_amount = 0
		return self.__balance - hold_amount
	
	@property
	def available(self) -> float:
		"""Available balance in this account (float), as a read-only property.
		
		Available balance is the maximum that can be withdrawn without either:
		(a) balance becoming less than min_balance, or
		(b) balance being less than the value of uncleared checks.
		"""
		sum_holds = sum(check.value for check in self.__pending_checks)
		# the held-back amount is max of min_balance or sum of uncleared checkes
		if self.bug == BUG_AVAILABLE_BALANCE:
            # available balance computed incorrectly
			avail = self.__balance - self.min_balance - sum_holds
		elif self.bug == BUG_MINIMUM_IS_IGNORED:
            # no minimum balance requirement
			avail = self.__balance - sum_holds
		else:
			avail = self.__balance - max(self.min_balance, sum_holds)
		return avail if (avail>0) else 0.0
	
	@property
	def min_balance(self) -> float:
		"""Minimum required balance for this account, as read-only property"""
		return self.__min_balance
	
	@property
	def account_name(self):
		"""The account name. Read-only."""
		return self.__name
	
	def deposit(self, money: Money):
		"""Deposit money or check into the account. 
		
		Args:
			money - Money or Check object with a positive value.
		Raises:
			ValueError if value of money parameter is not positive.
		"""
		if money.value < 0:
			raise ValueError("Value to deposit must be positive.")
		if money.value == 0 and self.bug != BUG_DEPOSIT_ZERO:
			raise ValueError("Value to deposit must be positive.")
		elif money.value == 0:
			print(f"Allow deposit of 0 due to defect {self.bug}")
		# if it is a check, verify the check was not already deposited
		if isinstance(money, Check):
			# looks like a check
			if money in self.__deposited_checks:
				if self.bug != BUG_DUPLICATE_CHECK:
					raise ValueError("Check already deposited")
			# add to list of checking waiting to clear
			self.__pending_checks.append(money)
			self.__deposited_checks.append(money)
		# both cash and checks contribute to the balance
		self.__balance += money.value

	def clear_check(self, check: Check):
		"""Mark a check as cleared so it is available for withdraw.

		Args:
			check - reference to a previously deposited check.
		
		Raises:
			ValueError if the check isn't in the list of checks waiting to clear
		"""
		if check in self.__pending_checks:
			self.__pending_checks.remove(check)
		elif self.bug != BUG_CLEAR_ANY_CHECK:
			raise ValueError(f"Check {check.check_number} is not an uncleared check")
		
	
	def withdraw(self, amount: float) -> Money:
		"""
		Withdraw an amount from the account. 

		Args:
			amount - (number) the amount to withdraw, at most the available balance
		Returns:
			a Money object for the amount requested.
		Raises:
			 ValueError if amount exceeds available balance or is not positive.
		"""
		if amount <= 0:
			raise ValueError("Amount to withdraw must be positive") 
		if amount > self.available:
			if self.bug == BUG_WITHDRAW_FAILS_SILENTLY:
				return None
			raise ValueError(f"Amount exceeds available balance")
		if amount == self.available and self.bug == BUG_CANT_WITHDRAW_AVAILABLE:
			# bug: you cannot withdraw exactly the available balance 
			raise ValueError(f"Amount exceeds available balance")
		# try to create the money before deducting from balance,
		# in case Money throws an exception.
		m = Money(amount)
		self.__balance -= amount
		return m 
	
	def __str__(self):
		"""String representation of the bank account.
		   Includes the acct name but not the balance.
		"""
		return f"{self.account_name} Account"


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

