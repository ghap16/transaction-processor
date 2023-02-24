from typing import List

from ..adapters import ReadCSVFile, TransactionParse
from ..config import settings
from ..models import (Account, Transaction, TransactionManager,
                      TransactionSummaryByMonth)
from ..services import SESEmailMessage, SESEmailSender


class TransactionProcessor:
    def __init__(self) -> None:
        self.tp = TransactionParse()
        self.tm = TransactionManager()
        self.email_sender = SESEmailSender()

    def read_csv_file(self, filename) -> List[dict]:
        return ReadCSVFile().read(filename=filename)

    def transactions_parse(self, transaction_data: List[dict]) -> List[Transaction]:
        return [self.tp.parse(item) for item in transaction_data]

    def send_email(
        self, account: Account, summary_by_month: List[TransactionSummaryByMonth]
    ):
        subject = f"Transaction summary for account {account.id}"
        email_data = {
            "title": subject,
            "summary_by_month": summary_by_month,
            "summary": account.get_summary(),
        }
        message = SESEmailMessage("transaction_summary.html", email_data)
        self.email_sender.send(
            to_emails=[settings.EMAIL_TO], subject=subject, message=message
        )

    def process(self, filename: str):
        # Read csv file
        transaction_data = self.read_csv_file(filename=filename)
        # Get List of Transactions
        transactions = self.transactions_parse(transaction_data=transaction_data)
        # Build Account
        account = Account(id=filename, transactions=transactions)
        # Get summary by month of the year
        summary_by_month = [
            account.get_summary_by_month(month) for month in range(1, 13)
        ]
        # send Email
        self.send_email(account=account, summary_by_month=summary_by_month)

        # Reponse
        return {
            "message": f"The transaction summary for the account {account.id} was sent by email"
        }
