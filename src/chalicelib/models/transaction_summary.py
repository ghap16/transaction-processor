from decimal import Decimal

from pydantic import BaseModel


class TransactionSummary(BaseModel):
    total: int
    balance: Decimal
    average_debit: Decimal
    average_credit: Decimal
