import urllib.parse

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.shortcuts import redirect
from django.urls import reverse
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return self.request.build_absolute_uri(reverse('facebook_callback'))


def facebook_callback(request):
    params = urllib.parse.urlencode(request.GET)
    return redirect(f'http://localhost:3001/auth/facebook?{params}')


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return self.request.build_absolute_uri(reverse('github_callback'))


def github_callback(request):
    params = urllib.parse.urlencode(request.GET)
    return redirect(f'http://localhost:3001/auth/github?{params}')


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        return self.request.build_absolute_uri(reverse('google_callback'))


def google_callback(request):
    params = urllib.parse.urlencode(request.GET)
    return redirect(f'http://localhost:3001/auth/google?{params}')


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_info_view(request):
    content = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    return Response(content)
