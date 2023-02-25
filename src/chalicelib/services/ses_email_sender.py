import logging
from typing import List

import boto3
from botocore.exceptions import ClientError

from ..config import settings
from ..exceptions import EmailSenderError
from ..interfaces import EmailSenderInterface
from .ses_email_message import SESEmailMessage


class SESEmailSender(EmailSenderInterface):
    charset = "UTF-8"

    def __init__(self) -> None:
        self.ses_client = boto3.client("ses", region_name=settings.REGION_NAME)

    def send(
        self, to_emails: List[str], subject: str, message: SESEmailMessage
    ) -> None:
        try:
            self.ses_client.send_email(
                Destination={"ToAddresses": to_emails},
                Message={
                    "Body": {
                        "Html": {
                            "Charset": self.charset,
                            "Data": message.render(),
                        }
                    },
                    "Subject": {
                        "Charset": self.charset,
                        "Data": subject,
                    },
                },
                Source=settings.EMAIL_FROM,
            )
        except ClientError as error:
            logging.error(
                f"Error sending email through aws, {error}",
                exc_info=True,
            )
            raise EmailSenderError(f"Error sending email, {subject}")
