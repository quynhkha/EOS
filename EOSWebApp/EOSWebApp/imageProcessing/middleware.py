from django.contrib.auth import logout
from django.contrib import messages
import datetime

from django.http import HttpResponse
from django.shortcuts import redirect

from django.conf import settings

from EOSWebApp.user.views import logout_user


class SessionIdleTimeout(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        return HttpResponse("in exception")

    def process_request(self, request):
        if request.user.is_authenticated():
            current_datetime = datetime.datetime.now()
            if ('last_login' in request.session):
                last = (current_datetime - request.session['last_login']).seconds
                if last > settings.SESSION_IDLE_TIMEOUT:
                    logout_user(request)
            else:
                request.session['last_login'] = current_datetime
        return None

