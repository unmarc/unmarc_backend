from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout
)
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST


@require_POST
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username is None or password is None:
        return HttpResponseBadRequest('No username/password received')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return HttpResponse()
    else:
        resp = HttpResponse(status=401)
        resp['WWW-Authenticate'] = 'UnmarcApi'
        return resp


@require_POST
def logout(request):
    auth_logout(request)
    return HttpResponse()


def auth_status(request):
    return JsonResponse({'userIsLoggedIn': request.user.is_authenticated})
