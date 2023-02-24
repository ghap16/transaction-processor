import logging
from typing import AnyStr

import boto3
from botocore.exceptions import ClientError
from jinja2 import Environment, TemplateError

from ..config import settings
from ..exceptions import EmailMessageError
from ..interfaces import EmailMessageInterface


class SESEmailMessage(EmailMessageInterface):
    charset = "UTF-8"

    def __init__(self, template_name: str, email_data: dict) -> None:
        self.client = boto3.client("s3")
        self.env = Environment()
        self.template_name = template_name
        self.email_data = email_data | {}

    def get_template(self) -> AnyStr:
        try:
            obj = self.client.get_object(Bucket=settings.BUCKET, Key=self.template_name)
            return obj["Body"].read().decode("utf-8")
        except ClientError as error:
            logging.error(
                f"Error reading {self.template_name} object from AWS: {error}",
                exc_info=True,
            )
            raise EmailMessageError(
                f"Error reading {self.template_name} object from AWS",
            )

    def render(self) -> AnyStr:
        try:
            return self.env.from_string(self.get_template()).render(**self.email_data)
        except TemplateError as error:
            logging.error(
                f"Error rendering {self.template_name} object: {error}",
                exc_info=True,
            )
            raise EmailMessageError(
                f"Error rendering {self.template_name} object",
            )
