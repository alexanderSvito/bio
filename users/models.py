from hashlib import md5
import base64
import random
import string

from django.contrib.auth.models import AbstractUser
from django.core.signing import TimestampSigner
from django.db import models


APHABET = (string.printable + string.ascii_letters * 3)


class User(AbstractUser):
    signer = TimestampSigner(salt='Hello World!')

    is_email_verified = models.BooleanField(default=False)
    initial_secret_key = models.CharField(null=True, max_length=256)
    verification_email_sent_at = models.DateTimeField(null=True)

    def get_initial_key(self):
        initial_key = "".join(random.sample(APHABET, 256))
        self.initial_secret_key = initial_key
        self.save()
        return initial_key

    def get_signed_key(self):
        initial_key = self.initial_secret_key
        signed_key = self.signer.sign(initial_key)
        encoded_key = base64.b64encode(signed_key)
        return encoded_key

    def get_verification_link(self):
        self.get_initial_key()
        host = 'http://127.0.0.1:8000'
        key = self.get_signed_key()
        link = f"{host}/verify-email?key={key}"
        return link

    def check_key(self, secret_key):
        decoded_key = base64.b64decode(secret_key)
        unsigned_key = self.signer.unsign(
            decoded_key,
            max_age=24 * 60 * 60
        )
        return unsigned_key == self.initial_secret_key

