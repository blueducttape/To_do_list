from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest, JsonResponse


class IndexView(View):
    """
    Класс, позволяющий использовать специальную статическую форму для входа
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "templates/login/index.html")

    def post(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse(request.POST, json_dumps_params={'indent': 4})
