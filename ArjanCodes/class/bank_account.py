from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"


@dataclass
class Transaction:
    type: TransactionType
    timestamp: datetime
    amount: float


class InsufficientBalanceError(Exception):
    """Raised when an account does not have enough funds."""
    pass


class BankAccount:
    def __init__(self, initial_balance: float = 0.0) -> None:
        self._balance = initial_balance
        self._transaction_history: list[Transaction] = []

    def _has_sufficient_balance(self, amount: float) -> bool:
        return amount <= self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        self._transaction_history.append(Transaction(TransactionType.DEPOSIT, datetime.now(), amount))

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if not self._has_sufficient_balance(amount):
            raise InsufficientBalanceError("Insufficient balance for withdrawal.")
        self._balance -= amount
        self._transaction_history.append(Transaction(TransactionType.WITHDRAWAL, datetime.now(), -amount))

    def transfer(self, target_account: BankAccount, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if not self._has_sufficient_balance(amount):
            raise InsufficientBalanceError("Insufficient balance for transfer.")

        timestamp = datetime.now()
        self._balance -= amount
        target_account._balance += amount
        self._transaction_history.append(Transaction(TransactionType.TRANSFER, timestamp, -amount))
        target_account._transaction_history.append(Transaction(TransactionType.TRANSFER, timestamp, amount))

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def transaction_history(self) -> list[Transaction]:
        return self._transaction_history


def main() -> None:
    account_1 = BankAccount(1000)
    account_2 = BankAccount(500)

    account_1.withdraw(200)
    account_2.deposit(300)
    account_1.transfer(account_2, 400)

    print(f"Account 1 balance: ${account_1.balance}")
    print(f"Account 2 balance: ${account_2.balance}")

    print("\nAccount 1 Transactions:")
    for t in account_1.transaction_history:
        print(f"- {t.timestamp:%Y-%m-%d %H:%M:%S} | {t.type.value:<10} | {t.amount:>8.2f}")

    print("\nAccount 2 Transactions:")
    for t in account_2.transaction_history:
        print(f"- {t.timestamp:%Y-%m-%d %H:%M:%S} | {t.type.value:<10} | {t.amount:>8.2f}")


if __name__ == "__main__":
    main()
