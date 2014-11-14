from django.shortcuts import render


def index(request):
    return render(request, "index.html")

# 10.12.4.254:8000/caller
def caller(request):
    return render(request, "caller.html")


def callee(request):
    return render(request, "callee.html")