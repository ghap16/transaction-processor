import json
from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

from chalice.test import Client

from app import app
from chalicelib.handlers import TransactionProcessor


class TestProcessCsv(TestCase):
    @patch.object(TransactionProcessor, "read_csv_file")
    @patch.object(TransactionProcessor, "send_email")
    def test_transaction_process_success(self, send_email_mock, read_csv_file_mock):
        account_id = uuid4()
        read_csv_file_mock.return_value = [
            {"id": "0", "date": "7/15", "transaction": "+60.5"},
            {"id": "1", "date": "7/28", "transaction": "-10.3"},
            {"id": "2", "date": "8/2", "transaction": "-20.46"},
            {"id": "3", "date": "8/13", "transaction": "+10"},
        ]
        send_email_mock.return_value = None

        with Client(app, stage_name="dev") as client:
            result = client.http.get(
                f"/{account_id}",
                headers={"Content-Type": "application/json"},
            )
            self.assertDictEqual(
                json.loads(result.body.decode("utf-8")),
                {
                    "message": f"The transaction summary for the account {account_id} was sent by email"
                },
            )
            read_csv_file_mock.assert_called_with(filename=str(account_id))
            send_email_mock.assert_called()
