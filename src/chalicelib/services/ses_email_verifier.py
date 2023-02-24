from pydantic import EmailStr
import boto3
import logging

from botocore.exceptions import ClientError
from ..config import settings
from ..exceptions import EmailVerifierError
from ..interfaces import EmailVerifierInterface


class SESEmailVerifier(EmailVerifierInterface):
    charset = "UTF-8"

    def __init__(self) -> None:
        self.ses_client = boto3.client("ses", region_name=settings.REGION_NAME)

    def verify(self, email: EmailStr):
        try:
            return self.ses_client.verify_email_identity(EmailAddress=email)
        except ClientError as error:
            logging.error(
                f"Error verifying email through aws, {error}",
                exc_info=True,
            )
            raise EmailVerifierError(f'Error verifying email, {email}')
