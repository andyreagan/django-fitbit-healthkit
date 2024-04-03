# a simple view that just loads index.html
# and puts the user in the context
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "sample/index.html", {"user": request.user})
