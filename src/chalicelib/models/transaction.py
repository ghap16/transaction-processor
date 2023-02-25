from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from .transaction_type import TransactionType


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
