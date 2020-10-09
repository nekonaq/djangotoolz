from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.static import serve as django_serve


def serve(request, path, document_root=None, show_indexes=False):
    if getattr(settings, 'USE_ACCEL_REDIRECT', False):
        response = HttpResponse()
        response['X-Accel-Redirect'] = '@media'
        response['Content-Type'] = ''   # リダイレクト先から正しい content-type を返すために必要
        return response

    return django_serve(request, path, document_root=document_root, show_indexes=show_indexes)


serve_protected = login_required(serve)
