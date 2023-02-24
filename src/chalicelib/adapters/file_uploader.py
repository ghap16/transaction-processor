from os.path import join as join_path
import logging
import boto3

from ..config import settings
from ..exceptions import UploadTransactionError


class FileUploader:
    def __init__(self) -> None:
        self.s3_client = boto3.client("s3", region_name=settings.REGION_NAME)

    def upload(self, filename, raw_file) -> None:
        try:
            temp_file = join_path(settings.TMP_PATH, filename)
            with open(temp_file, "wb") as f:
                f.write(raw_file)
            self.s3_client.upload_file(temp_file, settings.BUCKET, filename)
            return
        except Exception as e:
            logging.error("Error occurred during upload %s" % e, exc_info=True)
            raise UploadTransactionError(e)
