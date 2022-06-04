from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest, JsonResponse


class IndexLoginView(View):
    def get(self, reguest: HttpRequest) -> HttpResponse:
        return render(reguest, 'templates/login/index.html')

    def post(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse(request.POST, json_dumps_params={"ident": 4})
