from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest
from .settings_local import SERVER_VERSION


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "user_name": str(request.user),
            "server_version": SERVER_VERSION,
        }
        return render(request, "about/index.html", context=context)

