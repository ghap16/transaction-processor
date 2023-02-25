from decimal import Decimal
from typing import List

from ..config import settings
from .transaction import Transaction
from .transaction_type import TransactionType


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
