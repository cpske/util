import os
from money import Money
from check import Check

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

		Arguments:
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
	
	@property
	def balance(self) -> float:
		"""Balance in this account (float), as a read-only property"""
		return self.__balance
	
	@property
	def available(self) -> float:
		"""Available balance in this account (float), as a read-only property.
		
		Available balance is the maximum that can be withdrawn without either:
		(a) balance becoming less than min_balance, or
		(b) balance being less than the value of uncleared checks.
		"""
		sum_holds = sum(check.value for check in self.__pending_checks)
		# the held-back amount is max of min_balance or sum of uncleared checkes
		avail = self.balance - max(self.min_balance, sum_holds)
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
		
		Arguments:
			money - Money or Check object with a positive value.
		Throws:
			ValueError if value of money parameter is not positive.
		"""
		if money.value <= 0:
			raise ValueError("Cannot deposit a negative amount")
		# if it is a check, verify the check was not already deposited
		if isinstance(money, Check):
			# looks like a check
			if money in self.__deposited_checks:
				raise ValueError("Check already deposited")
			# add to list of checks waiting to clear
			self.__pending_checks.append(money)
			self.__deposited_checks.append(money)
		# both cash and checks contribute to the balance
		self.__balance += money.value

	def clear_check(self, check: Check):
		"""Mark a check as cleared so it is available for withdraw.

		Arguments:
			check - reference to a previously deposited check.
		
		Throws:
			ValueError if the check isn't in the list of checks waiting to clear
		"""
		if check in self.__pending_checks:
			self.__pending_checks.remove(check)
		else:
			raise ValueError(f"Check {check.check_number} is not an uncleared check")
	
	def withdraw(self, amount: float) -> Money:
		"""
		Withdraw an amount from the account. 

		Arguments:
			amount - (number) the amount to withdraw, at most the available balance
		Returns:
			a Money object for the amount requested.
		Throws:
			 ValueError if amount exceeds available balance or is not positive.
		"""
		if amount <= 0:
			raise ValueError("Amount to withdraw must be positive") 
		if amount > self.available:
			raise ValueError("Amount exceeds available balance")
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
