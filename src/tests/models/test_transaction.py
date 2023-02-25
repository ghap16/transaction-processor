from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from chalicelib.models import Transaction, TransactionType


class TestTransaction(TestCase):
    def test_is_debit_transaction(self):
        transaction = Transaction(
            id=1, date=datetime(2023, 1, 15), amount=Decimal("-9.54")
        )

        self.assertTrue(transaction.is_debit())
        self.assertEqual(transaction.type, TransactionType.DEBIT)

    def test_is_not_debit_transaction(self):
        transaction = Transaction(
            id=1, date=datetime(2023, 1, 15), amount=Decimal("20")
        )

        self.assertFalse(transaction.is_debit())
        self.assertNotEqual(transaction.type, TransactionType.DEBIT)

    def test_is_credit_transaction(self):
        transaction = Transaction(
            id=1, date=datetime(2023, 1, 15), amount=Decimal("9.54")
        )

        self.assertTrue(transaction.is_credit())
        self.assertEqual(transaction.type, TransactionType.CREDIT)

    def test_is_not_credit_transaction(self):
        transaction = Transaction(
            id=1, date=datetime(2023, 1, 15), amount=Decimal("-20")
        )

        self.assertFalse(transaction.is_credit())
        self.assertNotEqual(transaction.type, TransactionType.CREDIT)

    def test_is_unknown_transaction(self):
        transaction = Transaction(id=1, date=datetime(2023, 1, 15), amount=Decimal("0"))

        self.assertFalse(transaction.is_credit())
        self.assertFalse(transaction.is_debit())
        self.assertEqual(transaction.type, TransactionType.UNKNOWN)
