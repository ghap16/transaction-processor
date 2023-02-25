from datetime import datetime
from decimal import Decimal
from unittest import TestCase
from uuid import uuid4

from chalicelib.models import (
    Account,
    Transaction,
    TransactionSummary,
    TransactionSummaryByMonth,
)


class TestTransaction(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transactions = [
            Transaction(id=0, date=datetime(2023, 7, 15), amount=Decimal("60.5")),
            Transaction(id=1, date=datetime(2023, 7, 28), amount=Decimal("-10.3")),
            Transaction(id=2, date=datetime(2023, 8, 2), amount=Decimal("-20.46")),
            Transaction(id=3, date=datetime(2023, 8, 13), amount=Decimal("10")),
        ]
        cls.account = Account(id=uuid4(), transactions=cls.transactions)

    def test_summary(self):
        summary_expected = TransactionSummary(
            total=4,
            balance=Decimal("39.74"),
            average_credit=Decimal("35.25"),
            average_debit=Decimal("-15.38"),
        )
        self.assertEqual(self.account.get_summary(), summary_expected)

    def test_summary_by_month(self):
        summary_expected = TransactionSummaryByMonth(
            total=2,
            balance=Decimal("50.2"),
            average_credit=Decimal("60.50"),
            average_debit=Decimal("-10.30"),
            month=7,
        )
        self.assertEqual(self.account.get_summary_by_month(7), summary_expected)
