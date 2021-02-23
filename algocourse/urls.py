"""algocourse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.socialaccount.providers.facebook import views as facebook_views
from allauth.socialaccount.providers.github import views as github_views
from allauth.socialaccount.providers.google import views as google_views
from django.contrib import admin
from django.urls import path
from knox.views import LogoutView

from algocourse.auth import (
    FacebookLogin,
    GithubLogin,
    GoogleLogin,
    facebook_callback,
    get_user_info_view,
    github_callback,
    google_callback,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Facebook
    path('api/auth/facebook/url/', facebook_views.oauth2_login),
    path('api/auth/facebook/callback/', facebook_callback, name='facebook_callback'),
    path('api/auth/facebook/exchange/', FacebookLogin.as_view(), name='facebook_login'),
    # GitHub
    path('api/auth/github/url/', github_views.oauth2_login),
    path('api/auth/github/callback/', github_callback, name='github_callback'),
    path('api/auth/github/exchange/', GithubLogin.as_view(), name='github_login'),
    # Google
    path('api/auth/google/url/', google_views.oauth2_login),
    path('api/auth/google/callback/', google_callback, name='google_callback'),
    path('api/auth/google/exchange/', GoogleLogin.as_view(), name='google_login'),
    # Logout
    path('api/auth/logout/', LogoutView.as_view()),
    # APIs
    path('api/get_user_info/', get_user_info_view),
]
