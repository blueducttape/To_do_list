from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from django.template import RequestContext

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render
from django.contrib import auth


class IndexView(View):
    """
    Класс, позволяющий использовать специальную статическую форму для входа
    """

    @csrf_protect
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "templates/login/index.html", RequestContext(request))

# Added RequestContext
    @csrf_protect
    def post(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse(request.POST, json_dumps_params={'indent': 4})

