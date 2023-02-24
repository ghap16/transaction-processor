from pydantic import EmailStr
from ..services import SESEmailVerifier


class EmailVerifier:
    def __init__(self) -> None:
        self.email_verifier = SESEmailVerifier()

    def verify(self, email: EmailStr):
        self.email_verifier.verify(email=email)
        return {"Message": "Email verification sent"}
