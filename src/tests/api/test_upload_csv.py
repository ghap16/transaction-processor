import json
from io import BytesIO
from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

from chalice.test import Client

from app import app
from chalicelib.handlers import TransactionUploader
from chalicelib.models import AccountBase


class TestUploadCsv(TestCase):
    @patch.object(TransactionUploader, "upload")
    def test_upload_csv_success(self, upload_mock):
        account_id = uuid4()
        upload_mock.return_value = AccountBase(id=account_id)
        csv_mock = BytesIO()
        with open("tests/fixtures/transactions.csv", "rb") as csv_file:
            csv_mock.write(csv_file.read())

        with Client(app, stage_name="dev") as client:
            result = client.http.post(
                "/upload/csv",
                headers={"Content-Type": "application/octet-stream"},
                body=csv_mock.getvalue(),
            )
            self.assertDictEqual(
                json.loads(result.body.decode("utf-8")), {"id": str(account_id)}
            )
            upload_mock.assert_called()
