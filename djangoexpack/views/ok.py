from django.http import JsonResponse
from django.urls import path
from django.views import generic


class OKView(generic.View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'result': 'ok'})


urlpatterns = [
    path('', OKView.as_view()),
]
