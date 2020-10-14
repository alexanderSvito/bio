import base64
import json
import time

import jwt
from django.test import TestCase

from users.models import JWTToken, User
from django.test import Client


class TestAuthToken(TestCase):
    fingerprint = "1234567890"
    ipv4 = '127.0.0.1'
    client = Client()

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='test',
        )
        self.user.set_password('password')
        self.user.create_all_related_blocks()
        self.user.save()

    def refresh_user(self):
        self.user = User.objects.get(username='test')

    def test_token_deserialization(self):
        access, refresh = JWTToken.create_token_pair(self.user, self.fingerprint, self.ipv4)

        retrieved_user = JWTToken.verify(access, self.fingerprint)

        self.assertEqual(self.user, retrieved_user)

    def test_token_becomes_inactive_after_new_one(self):
        for i in range(5):
            access, refresh = JWTToken.create_token_pair(self.user, self.fingerprint, self.ipv4)

        actives = list(self.user.tokens.values_list('is_active', flat=True))

        self.assertEqual(sum(actives), 2)

    def test_login_attempts_being_logged(self):
        response = self.client.post('/login', {'username': 'test', 'password': 'password'})
        self.assertEqual(response.status_code, 200)

        logins = self.user.security_block.logins.all()
        self.assertEqual(len(logins), 1)

        self.assertEqual(logins[0].is_successful, True)

    def test_tokens_received_after_login(self):
        response = self.client.post('/login', {'username': 'test', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('access_token', data)
        self.assertNotIn('refresh_token', data)

    def test_unsuccessful_logins_result_in_lock(self):
        for i in range(4):
            response = self.client.post('/login', {'username': 'test', 'password': 'password123'})

        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertIn(data['status'], 'failure')
        self.assertIn(data['error'], 'Too many unsuccessful login attempts. User is locked.')
        self.refresh_user()
        self.assertEqual(self.user.is_locked, True)

    def test_correct_token_grants_access(self):
        response = self.client.post('/login', {'username': 'test', 'password': 'password'})

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        access_token = data['access_token']

        response = self.client.get('/me', HTTP_AUTHORIZATION=f"Bearer {access_token}")

        self.assertEqual(response.status_code, 200)

    def test_token_signature_change(self):
        response = self.client.post('/login', {'username': 'test', 'password': 'password'})

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        access_token = data['access_token']
        decoded = jwt.decode(access_token, verify=False)
        decoded['userid'] = 99999
        payload = base64.b64encode(json.dumps(decoded).encode('ascii')).decode()
        parts = access_token.split('.')
        parts[1] = payload
        fake_token = '.'.join(parts)

        response = self.client.get('/me', HTTP_AUTHORIZATION=f"Bearer {fake_token}")

        self.assertEqual(response.status_code, 403)

    def test_token_corruption(self):
        response = self.client.post('/login', {'username': 'test', 'password': 'password'})

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        access_token = data['access_token']
        access_token = access_token[:15] + ('a' if access_token[15] != 'a' else 'b') + access_token[16:]

        response = self.client.get('/me', HTTP_AUTHORIZATION=f"Bearer {access_token}")

        self.assertEqual(response.status_code, 403)

    def test_token_wrong_fingerprint(self):
        response = self.client.post('/login', {'username': 'test', 'password': 'password'})

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        access_token = data['access_token']

        response = self.client.get('/me', HTTP_AUTHORIZATION=f"Bearer {access_token}", HTTP_USER_AGENT="Mozilla/5.0")

        self.assertEqual(response.status_code, 403)

    def test_token_same_fingerprint_different_ip(self):
        response = self.client.post('/login', {'username': 'test', 'password': 'password'})

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        access_token = data['access_token']

        response = self.client.get('/me', HTTP_AUTHORIZATION=f"Bearer {access_token}", HTTP_X_FORWARDED_FOR='8.8.8.8')

        self.assertEqual(response.status_code, 403)

    def test_token_expiry(self):
        with self.settings(TOKEN_MINUTES=1/60):
            response = self.client.post('/login', {'username': 'test', 'password': 'password'})

            self.assertEqual(response.status_code, 200)

            data = json.loads(response.content)
            access_token = data['access_token']
            time.sleep(2)

            response = self.client.get('/me', HTTP_AUTHORIZATION=f"Bearer {access_token}")

            self.assertEqual(response.status_code, 403)
