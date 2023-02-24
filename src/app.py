
from chalice import Chalice, ChaliceViewError

from chalicelib.config import settings
from chalicelib.exceptions import UploadTransactionError
from chalicelib.handlers import TransactionProcessor, TransactionUploader, EmailVerifier

app = Chalice(app_name="transaction-processor")

app.debug = settings.DEBUG

app.api.binary_types = [
    "text/csv",
]

@app.route("/upload/csv", methods=["POST"], content_types=["application/octet-stream"])
def upload_csv():
    try:
        account = TransactionUploader().upload(app.current_request.raw_body)
        return account.json()
    except UploadTransactionError as e:
        app.log.error("Exception: %s" % e, exc_info=True)
        raise ChaliceViewError("upload failed")


@app.route("/{account_id}")
def process_csv(account_id):
    return TransactionProcessor().process(account_id)



@app.route("/verify_email", methods=['POST'])
def verify_email():
    email = app.current_request.json_body.get('email')
    if not email:
        return {"Message": 'Email is required'}
    return EmailVerifier().verify(email)
