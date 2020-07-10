from django.http.response import HttpResponseRedirectBase


class HttpAccelRedirect(HttpResponseRedirectBase):
    status_code = 200
    url = property(lambda self: self['X-Accel-Redirect'])

    def __init__(self, redirect_to, *args, **kwargs):
        super().__init__(redirect_to, *args, **kwargs)
        self._headers.pop('location', None)
        self['X-Accel-Redirect'] = redirect_to
