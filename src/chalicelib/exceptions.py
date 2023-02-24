from chalice import ChaliceViewError


class UploadTransactionError(ChaliceViewError):
    pass


class EmailMessageError(ChaliceViewError):
    pass

class EmailSenderError(ChaliceViewError):
    pass

class EmailVerifierError(ChaliceViewError):
    pass
