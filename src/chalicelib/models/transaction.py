from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List
import calendar

from pydantic import BaseModel

from ..config import settings


class TransactionType(Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    UNKNOWN = "UNKNOWN"


class Transaction(BaseModel):
    id: int
    date: date
    amount: Decimal

    @property
    def type(self) -> TransactionType:
        if self.is_debit():
            return TransactionType.DEBIT
        elif self.is_credit():
            return TransactionType.CREDIT
        return TransactionType.UNKNOWN

    def is_debit(self) -> bool:
        return self.amount < 0

    def is_credit(self) -> bool:
        return self.amount > 0


class TransactionManager:
    def _get_amounts(self, transactions: List[Transaction]) -> List[Decimal]:
        return [transaction.amount for transaction in transactions]

    def balance(self, transactions: List[Transaction]) -> Decimal:
        return sum(self._get_amounts(transactions))

    def total(self, transactions: List[Transaction]) -> int:
        return len(transactions)

    def average(self, transactions: List[Transaction]) -> Decimal:
        transaction_total = self.total(transactions)
        if transaction_total == 0:
            return Decimal("0.00")
        return round(
            self.balance(transactions) / transaction_total, settings.DECIMAL_PRECISION
        )

    def filter_by_month(self, month: int, transactions: List[Transaction]):
        return [
            transaction
            for transaction in transactions
            if transaction.date.month == month
        ]

    def filter_by_type(
        self, type: TransactionType, transactions: List[Transaction]
    ) -> List[Transaction]:
        return [transaction for transaction in transactions if transaction.type == type]


class TransactionSummary(BaseModel):
    total: int
    balance: Decimal
    average_debit: Decimal
    average_credit: Decimal


class TransactionSummaryByMonth(TransactionSummary):
    month: int
    total: int
    balance: Decimal
    average_debit: Decimal
    average_credit: Decimal

    def get_month_name(self):
        return calendar.month_name[self.month]
