
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user


class GetRelationFieldIsCreated(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'session')
        user = SimpleLazyObject(lambda: get_user(request))
        try:
            user.avatarused
            user.is_avatarused_exist = True
        except:
            user.is_avatarused_exist = False




