from uuid import uuid4

from ..adapters import FileUploader
from ..config import settings
from ..models import AccountBase


class TransactionUploader:
    def __init__(self) -> None:
        self.fileid = uuid4()
        self._set_filename()
        self.file_uploader = FileUploader()

    def _set_filename(self) -> None:
        self.filename = f"{settings.PREFIX_FILE}_{self.fileid}.csv"

    def upload(self, raw_file) -> AccountBase:
        self.file_uploader.upload(filename=self.filename, raw_file=raw_file)
        return AccountBase(id=self.fileid)
