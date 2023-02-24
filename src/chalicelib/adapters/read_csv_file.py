import csv
from decimal import Decimal
from typing import List

import boto3
import dateutil.parser

from ..config import settings
from ..interfaces import ReadCSVFileInterface, TransactionParseInterface
from ..models.transaction import Transaction


class TransactionParse(TransactionParseInterface):
    def parse(self, transaction_data: dict) -> Transaction:
        return Transaction(
            id=int(transaction_data["id"]),
            date=dateutil.parser.parse(transaction_data["date"]),
            amount=Decimal(transaction_data["transaction"]),
        )


class ReadCSVFile(ReadCSVFileInterface):
    def __init__(self) -> None:
        self.s3_client = boto3.client("s3", region_name=settings.REGION_NAME)

    def read(self, filename: str) -> List[dict]:
        obj = self.s3_client.get_object(
            Bucket=settings.BUCKET, Key=f"{settings.PREFIX_FILE}_{filename}.csv"
        )["Body"]
        csv_reader = csv.DictReader(
            obj.read().decode("utf-8").splitlines(), delimiter=","
        )
        return [
            {key.lower(): value for key, value in row.items()} for row in csv_reader
        ]
