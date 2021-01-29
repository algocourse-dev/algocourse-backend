from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme
from lib.logging.logger import log


def abc(request):
    log.info(request.META)
    next_url = request.GET.get('next', '')
    is_allowed_next_url = url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts=request.get_host(),
        require_https=request.is_secure(),
    )
    log.info("next_url=%s,allowed=%s", next_url, is_allowed_next_url)

    try:
        raise Exception("WTFe?")
    except Exception:
        log.exception("Whate?|from=%s,to=%s", "aasdasd", 1111)
    return HttpResponse('Welcome to AlgoCourse!e')


def login(request):
    # check if the next query string contain an allowed URL to be redirected or not
    next_url = request.GET.get('next', '')
    is_allowed_next_url = url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts=request.get_host(),
        require_https=request.is_secure(),
    )

    # redirect the user to next_url if authenticated
    if request.user.is_authenticated:
        if is_allowed_next_url:
            return redirect(next_url)
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))

    return render(request, 'login.html', {'next_url': next_url})


@login_required
def home(request):
    return render(request, 'home.html')
