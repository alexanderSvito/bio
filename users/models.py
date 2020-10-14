import datetime
import uuid

import jwt
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from users.helpers import get_random_string

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10)
    has_other_names = models.BooleanField(default=False)
    other_name = models.CharField(max_length=64, null=True, blank=True)
    is_locked = models.BooleanField(default=False)

    @property
    def address(self):
        return self.addresses.filter(is_current=True).first()

    @property
    def passport(self):
        return self.passports.latest('date_of_issue')

    @classmethod
    def authenticate(cls, request, username, password) -> (bool, dict):
        fingerprint = request.fingerprint
        meta = request.user_agent.meta

        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_locked:
            is_locked = user.log_login(request, is_successful=True)
            return is_locked, user.get_tokens(fingerprint, request.ipv4, **meta)
        else:
            try:
                compromised_user = cls.objects.get(username=username)
            except cls.DoesNotExist:
                return False, None
            is_locked = compromised_user.log_login(request, is_successful=False)
            return is_locked, None

    def get_tokens(self, fingerprint, ipv4, **meta):
        access_token, refresh_token = JWTToken.create_token_pair(
            self, fingerprint, issuer_ip_address=ipv4, meta=meta
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def create_all_related_blocks(self):
        security_block = Security()
        self.security_block = security_block
        security_block.user = self
        security_block.save()

    def check_restricted_access(self):
        if self.security_block.unsuccessful_login_attempts > settings.MAX_LOGIN_ATTEMPTS:
            self.is_locked = True
            self.save()
            return True
        return False

    def log_login(self, request, is_successful=False):
        self.security_block.logins.create(
            issuer_ip_address=request.ipv4,
            is_successful=is_successful,
            platform=request.user_agent.meta['platform'],
            device=request.user_agent.meta['device'],
            browser=request.user_agent.meta['browser'],
        )
        if is_successful:
            self.security_block.unsuccessful_login_attempts = 0
        else:
            self.security_block.unsuccessful_login_attempts += 1

        self.security_block.save()
        return self.check_restricted_access()

    def logout(self):
        self.tokens.all().update(is_active=False)


class FingerprintMixin(models.Model):
    device = models.CharField(max_length=32, null=True)
    platform = models.CharField(max_length=32, null=True)
    browser = models.CharField(max_length=32, null=True)
    fingerprint = models.CharField(max_length=128)
    issuer_ip_address = models.GenericIPAddressField(unpack_ipv4=True)

    class Meta:
        abstract = True


class JWTToken(FingerprintMixin):
    user = models.ForeignKey(User, related_name='tokens', on_delete=models.CASCADE)
    token_id = models.UUIDField(unique=True)
    token_type = models.CharField(max_length=8)

    token_secret = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['token_id'], name='index_active_tokens_btree', condition=models.Q(is_active=True)),
        ]

    @classmethod
    def _create_single_token(cls, user, fingerprint, issuer_ip_address, token_type='access', meta=None):
        token_id = str(uuid.uuid4())

        private_key = ec.generate_private_key(ec.SECP521R1(), default_backend())
        public_key = private_key.public_key()

        rsa_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        if meta is not None:
            device = meta.get('device')
            platform = meta.get('platform')
            browser = meta.get('browser')
        else:
            device, platform, browser = None, None, None

        payload = {
            "userid": user.id,
            "username": user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.TOKEN_MINUTES),
            "iss": "ceteus:security",
            "type": token_type,
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, private_key, algorithm='ES512', headers={
            'tokenid': token_id
        })

        cls.objects.create(
            user=user,
            token_id=token_id,
            token_type=token_type,
            token_secret=rsa_pem,
            fingerprint=fingerprint,
            device=device,
            platform=platform,
            browser=browser,
            issuer_ip_address=issuer_ip_address
        )

        return token

    @classmethod
    def create_token_pair(cls, user, fingerprint, issuer_ip_address, meta=None):
        cls.objects.filter(user=user, fingerprint=fingerprint).update(is_active=False)

        access_token = cls._create_single_token(user, fingerprint, issuer_ip_address, token_type='access', meta=meta)
        refresh_token = cls._create_single_token(user, fingerprint, issuer_ip_address, token_type='access', meta=meta)

        return access_token.decode(), refresh_token.decode()

    @classmethod
    def alert_security_breach(cls, message, *args):
        print(message, *args)

    @classmethod
    def _decode_token(cls, encoded, fingerprint):
        try:
            headers = jwt.get_unverified_header(encoded)
        except jwt.exceptions.DecodeError as e:
            cls.alert_security_breach(f"Token forgery: Corrupted token header ({e})")
            return None

        if headers['alg'] == 'none':
            cls.alert_security_breach("None-alg in token header")
            return None

        token_id = headers['tokenid']

        token = cls.objects.get(token_id=token_id)

        if token.is_active:
            if token.fingerprint != fingerprint:
                cls.alert_security_breach("Wrong fingerprint")
                return None

            pem_key = token.token_secret.encode('ascii')
            public_key = serialization.load_pem_public_key(pem_key, default_backend())

            try:
                payload = jwt.decode(encoded, public_key, iss="ceteus:security", algorithms=['ES512'])
            except jwt.exceptions.InvalidSignatureError:
                cls.alert_security_breach("Token forgery: Signature verification failed")
                return None
            except jwt.exceptions.DecodeError as e:
                cls.alert_security_breach(f"Token forgery: Corrupted token payload ({e})")
                return None
            except jwt.exceptions.ExpiredSignatureError:
                cls.alert_security_breach(f"Token expired")
                return None
            user = get_user_model().objects.get(pk=payload['userid'])
            tokens_ids = user.tokens.all().values_list('token_id', flat=True)
            if uuid.UUID(token_id) not in tokens_ids:
                cls.alert_security_breach("Non-existent token ID for user", user)
                return None

            return token
        else:
            cls.alert_security_breach("Inactive token usage attempt")
            return None

    @classmethod
    def refresh(cls, encoded, fingerprint):
        token = cls._decode_token(encoded, fingerprint)
        if token and token.token_type == 'refresh':
            return token.user
        else:
            return None

    @classmethod
    def verify(cls, encoded, fingerprint):
        token = cls._decode_token(encoded, fingerprint)
        if token and token.token_type == 'access':
            return token.user
        else:
            return None


class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    is_current = models.BooleanField(default=False)
    is_correspondence_address = models.BooleanField(default=True)

    address_1 = models.CharField(max_length=64)
    address_2 = models.CharField(max_length=64, blank=True)

    country = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    zip = models.CharField(max_length=16)


class Passport(models.Model):
    owner = models.ForeignKey(User, related_name='passports', on_delete=models.CASCADE)
    country = models.CharField(max_length=64)
    type = models.CharField(max_length=5)
    code_of_country = models.CharField(max_length=5)
    passport_no = models.CharField(max_length=64)
    identification_no = models.CharField(max_length=128)

    surname = models.CharField(max_length=64)
    given_names = models.CharField(max_length=64)
    nationality = models.CharField(max_length=64)

    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=2)
    place_of_birth = models.CharField(max_length=64)

    authority = models.CharField(max_length=128)

    date_of_issue = models.DateField(null=True)
    date_of_expiry = models.DateField(null=True)

    coding = models.CharField(max_length=128)


class Visa(models.Model):
    passport = models.ForeignKey(Passport, related_name='visas', on_delete=models.CASCADE)

    country = models.CharField(max_length=64)
    start_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    issued_in = models.CharField(max_length=64)
    category = models.CharField(max_length=5)

    visa_no = models.CharField(max_length=64)
    coding = models.CharField(max_length=128)


class Security(models.Model):
    user = models.OneToOneField(User, related_name='security_block', on_delete=models.CASCADE)
    is_email_verified = models.BooleanField(default=False)
    initial_email_key = models.CharField(max_length=256, null=True)

    is_phone_verified = models.BooleanField(default=False)
    initial_phone_key = models.CharField(max_length=6, null=True)

    is_passport_verified = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)

    is_locked = models.BooleanField(default=False)

    unsuccessful_login_attempts = models.SmallIntegerField(default=0)


class LoginAttempt(FingerprintMixin):
    security = models.ForeignKey(Security, related_name='logins', on_delete=models.CASCADE)
    attempted_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField()


class Device(models.Model):
    security = models.ForeignKey(Security, related_name='devices', on_delete=models.CASCADE)
    trusted = models.BooleanField(default=False)


class EmailSent(models.Model):
    security = models.ForeignKey(Security, related_name='emails', on_delete=models.CASCADE)
    header = models.CharField(max_length=128)
    sent_at = models.DateTimeField(null=True)


class SMSSent(models.Model):
    security = models.ForeignKey(Security, related_name='sms', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    sent_at = models.DateTimeField(null=True)
