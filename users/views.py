from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.http import require_GET
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from users.helpers import get_random_string, get_verification_link, check_key, get_username, login_required
from users.models import User, JWTToken
from users.serializers import UserSerializer


@api_view(['GET', 'POST'])
def verify_email(request):
    if request.method == 'POST':
        request.data['addresses'] = [request.data['addresses']]
        request.data['username'] = get_username(request.data['first_name'], request.data['last_name'])
        form = UserSerializer(data=request.data)
        if form.is_valid():
            initial_key = get_random_string()
            user = form.save()
            user.security_block.initial_email_key = initial_key
            user.security_block.save()
            print(get_verification_link(user.username, initial_key))
            return JsonResponse(form.data)
        else:
            return JsonResponse(form.errors, status=400)
    elif request.method == 'GET':
        secret_key = request.GET.get('key')
        username = request.GET.get('username')
        user = User.objects.get(username=username)
        initial_key = user.security_block.initial_email_key

        if check_key(initial_key, secret_key):
            user.security_block.is_email_verified = True
            user.security_block.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return Http404()


@api_view(['POST'])
def get_access_token(request):
    username, password = request.data['username'], request.data['password']
    is_locked, tokens = User.authenticate(request, username, password)
    if tokens is not None:
        access = {"access_token": tokens["access_token"]}
        response = JsonResponse(access)
        response.set_cookie(
            "refresh_token",
            tokens["refresh_token"],
            httponly=True,
            secure=not settings.DEBUG,
            samesite='none'
        )
        return response
    else:
        if is_locked:
            return JsonResponse(
                {"status": "failure", "error": "Too many unsuccessful login attempts. User is locked."},
                status=401
            )
        else:
            return JsonResponse(
                {"status": "failure", "error": "Couldn't authenticate user with these credentials"},
                status=401
            )


@api_view(['POST'])
def refresh_token(request):
    refresh_token = request.COOKIES.get('refresh_token')
    user = JWTToken.refresh(refresh_token, request.fingerprint)
    if user is not None:
        tokens = user.get_tokens(request.fingerprint, request.ipv4, **request.user_agent.meta)

        access = {"access_token": tokens["access_token"]}
        response = JsonResponse(access)
        response.set_cookie(
            "refresh_token",
            tokens["refresh_token"],
            httponly=True,
            secure=not settings.DEBUG,
            samesite='none'
        )
        return response
    else:
        return JsonResponse(
            {"status": "failure", "error": "Token forgery"},
            status=403
        )


@api_view(['GET'])
@login_required
def me(request):
    user = request.user
    serializer = UserSerializer(instance=user)
    return Response(serializer.data)


@login_required
@require_GET
def verify_view(request):
    secret_ket = request.GET.get('key')
    if request.user.check_key(secret_ket):
        return render(request, 'confirmation_success.html')
    else:
        return redirect("/")


def logout_view(request):
    logout(request)
    return redirect("/")
