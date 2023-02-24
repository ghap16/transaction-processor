import abc
from typing import AnyStr, List
from pydantic import EmailStr


class ReadCSVFileInterface(abc.ABC):
    @abc.abstractmethod
    def read(self, filename: str) -> List[dict]:
        ...


class TransactionParseInterface(abc.ABC):
    @abc.abstractmethod
    def parse(self, transaction_data: dict):
        ...


class EmailMessageInterface(abc.ABC):
    @abc.abstractmethod
    def get_template(self) -> AnyStr:
        ...

    @abc.abstractmethod
    def render(self) -> None:
        ...


class EmailSenderInterface(abc.ABC):
    @abc.abstractmethod
    def send(
        self, to_emails: List[str], subject: str, message: EmailMessageInterface
    ) -> None:
        ...


class EmailVerifierInterface(abc.ABC):
    @abc.abstractmethod
    def verify(self, email: EmailStr) -> None:
        ...
