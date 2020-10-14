from datetime import timedelta
from hashlib import sha256
import base64
import random
import string
import unidecode

from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner
from django.conf import settings
from django.http import JsonResponse

signer = TimestampSigner()


def get_username(first_name, last_name):
    usernames = set(get_user_model().objects.all().values_list('username', flat=True))

    first_name = unidecode.unidecode(first_name)
    last_name = unidecode.unidecode(last_name)

    prefix = f"{first_name.lower()}{last_name.lower()}"
    username = prefix
    while username in usernames:
        username = prefix + str(random.randint(1, 1000))

    return username


def get_sms_code():
    return "".join([random.choice(string.digits) for _ in range(6)])


def get_random_string():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    initial_key = "".join([random.choice(alphabet) for _ in range(256)])
    return initial_key


def get_hashed(key):
    return sha256(bytes(key, encoding='ascii')).hexdigest()


def get_encoded_key(key):
    return base64.b64encode(bytes(key, encoding='ascii')).decode(encoding='utf-8')


def get_decoded_key(key):
    return base64.b64decode(bytes(key, encoding='ascii')).decode(encoding='utf-8')


def get_signed_key(initial_key):
    hashed_key = get_hashed(initial_key)
    signed_key = signer.sign(hashed_key)
    encoded_key = get_encoded_key(signed_key)
    return encoded_key


def get_verification_link(username, initial_key):
    host = settings.HOST_NAME
    key = str(get_signed_key(initial_key))
    link = f"{host}verify/email?username={username}&key={key}"
    return link


def check_key(initial_key, secret_key):
    decoded_key = get_decoded_key(secret_key)
    unsigned_key = signer.unsign(
        decoded_key,
        max_age=timedelta(hours=1)
    )
    hashed_key = get_hashed(initial_key)
    return unsigned_key == hashed_key


def login_required(function=None, redirect_field_name=None):
    """
    Just make sure the user is authenticated to access a certain ajax view

    Otherwise return a HttpResponse 401 - authentication required
    instead of the 302 redirect of the original Django decorator
    """
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({"status": "failure", "error": "Not Authorized"}, status=403)
        return _wrapped_view

    if function is None:
        return _decorator
    else:
        return _decorator(function)
