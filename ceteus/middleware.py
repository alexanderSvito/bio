import json

from user_agents import parse

from users.helpers import get_hashed
from users.models import JWTToken


class FingerprintMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def client_user_agent(self, request):
        return request.META.get('HTTP_USER_AGENT', '')

    def get_client_key(self, request):
        return request.POST.get('clientkey')

    def __call__(self, request):
        raw_user_agent = self.client_user_agent(request)
        user_agent = parse(raw_user_agent)
        request.user_agent = user_agent

        request.user_agent.meta = {
            "platform": f"{user_agent.os.family} {user_agent.os.version_string}",
            "device": f"{user_agent.device.brand} {user_agent.device.model}",
            "browser": f"{user_agent.browser.family} {user_agent.browser.version_string}",
        }

        request.ipv4 = self.get_client_ip(request)
        request.client_key = self.get_client_key(request)
        payload = {
            "ip": request.ipv4,
            "ua": raw_user_agent,
            "key": request.client_key,
        }
        fingerprint = get_hashed(json.dumps(payload))
        request.fingerprint = fingerprint

        response = self.get_response(request)

        return response


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')
            user = JWTToken.verify(token, request.fingerprint)
            request.user = user

        response = self.get_response(request)

        return response
