"""Trnsaction processor APP"""

from chalice import BadRequestError, Chalice
from pydantic import ValidationError

from chalicelib.config import settings
from chalicelib.handlers import TransactionProcessor, TransactionUploader
from chalicelib.models import AccountBase

app = Chalice(app_name="transaction-processor")

app.debug = settings.DEBUG

app.api.binary_types = [
    "text/csv",
]


@app.route("/upload/csv", methods=["POST"], content_types=["application/octet-stream"])
def upload_csv():
    """Endpoint to upload CSV file

    Returns:
        json: -id (uuid)
    """
    account = TransactionUploader().upload(app.current_request.raw_body)
    return account.json()


@app.route("/{account_id}")
def process_csv(account_id):
    """Endpoint to Read csv file, process and send by email

    Args:
        account_id (str): Account ID

    Returns:
        json: -message (str)
    """
    try:
        AccountBase(id=account_id)
    except ValidationError as e:
        raise BadRequestError(e)
    return TransactionProcessor().process(account_id)
