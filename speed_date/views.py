from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def caller(request):
    return render(request, "caller.html")


def callee(request):
    return render(request, "callee.html")