from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    name = " to kunal"
    return render(request, 'index.html', {"name": name})


def contact(request):
    obj = None

    if request.POST:

        obj = request.POST
    return render(request, 'form.html', {'title': "contact us", 'obj': obj})


