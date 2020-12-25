# from django.shortcuts import render
from django.http import HttpResponse
from lib.logging.logger import log


def abc(request):
    log.info("I'm heree")
    log.error("Error heree")
    log.data("Hehehee")

    try:
        raise Exception("WTFe?")
    except Exception:
        log.exception("Whate?|from=%s,to=%s", "aasdasd", 1111)
    return HttpResponse('Welcome to AlgoCourse!e')
