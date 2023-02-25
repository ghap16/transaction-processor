from chalice import ChaliceViewError


class UploadTransactionError(ChaliceViewError):
    pass


class EmailMessageError(ChaliceViewError):
    pass


class EmailSenderError(ChaliceViewError):
    pass
