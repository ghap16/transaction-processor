from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from chalicelib.adapters import TransactionParse
from chalicelib.models import Transaction


class TestTransactionParseCsv(TestCase):
    def test_transaction_parse_success(self):
        current_year = datetime.now().year
        transaction_data = {"id": "0", "date": "7/15", "transaction": "+60.5"}
        response_expect = Transaction(
            id=0, date=datetime(current_year, 7, 15), amount=Decimal("60.5")
        )

        parse_response = TransactionParse().parse(transaction_data=transaction_data)

        self.assertEqual(parse_response, response_expect)
        self.assertDictEqual(parse_response.dict(), response_expect.dict())
