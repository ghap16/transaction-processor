from typing import List
from uuid import UUID

from pydantic import BaseModel

from .transaction import (Transaction, TransactionManager, TransactionSummary,
                          TransactionSummaryByMonth, TransactionType)


class AccountBase(BaseModel):
    id: UUID

    class Config:
        arbitrary_types_allowed = True


class Account(AccountBase):
    transactions: List[Transaction]

    _tm = TransactionManager()

    def get_summary(self) -> TransactionSummary:
        return TransactionSummary(
            total=self._tm.total(self.transactions),
            balance=self._tm.balance(self.transactions),
            average_debit=self._tm.average(
                self._tm.filter_by_type(
                    TransactionType.DEBIT,
                    self.transactions,
                ),
            ),
            average_credit=self._tm.average(
                self._tm.filter_by_type(
                    TransactionType.CREDIT,
                    self.transactions,
                ),
            ),
        )

    def get_summary_by_month(self, month: int) -> TransactionSummaryByMonth:
        transactions_of_month = self._tm.filter_by_month(month, self.transactions)
        return TransactionSummaryByMonth(
            month=month,
            total=self._tm.total(transactions_of_month),
            balance=self._tm.balance(transactions_of_month),
            average_debit=self._tm.average(
                self._tm.filter_by_type(
                    TransactionType.DEBIT,
                    transactions_of_month,
                ),
            ),
            average_credit=self._tm.average(
                self._tm.filter_by_type(
                    TransactionType.CREDIT,
                    transactions_of_month,
                ),
            ),
        )
