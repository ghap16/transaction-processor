from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from chalicelib.models import Transaction, TransactionManager, TransactionType


class TestTransaction(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transaction_manager = TransactionManager()
        cls.transactions = [
            Transaction(id=0, date=datetime(2023, 7, 15), amount=Decimal("60.5")),
            Transaction(id=1, date=datetime(2023, 7, 28), amount=Decimal("-10.3")),
            Transaction(id=2, date=datetime(2023, 8, 2), amount=Decimal("-20.46")),
            Transaction(id=3, date=datetime(2023, 8, 13), amount=Decimal("10")),
        ]

    def test_balance(self):
        self.assertEqual(
            self.transaction_manager.balance(self.transactions), Decimal("39.74")
        )

    def test_total(self):
        self.assertEqual(self.transaction_manager.total(self.transactions), 4)

    def test_average(self):
        self.assertEqual(
            self.transaction_manager.average(self.transactions), Decimal("9.94")
        )

    def test_filter_by_month(self):
        self.assertListEqual(
            self.transaction_manager.filter_by_month(7, self.transactions),
            [self.transactions[0], self.transactions[1]],
        )

    def test_filter_by_type(self):
        self.assertListEqual(
            self.transaction_manager.filter_by_type(
                TransactionType.DEBIT, self.transactions
            ),
            [self.transactions[1], self.transactions[2]],
        )
