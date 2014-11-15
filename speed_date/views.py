import random
from django.shortcuts import render
import facebook
from speed_date.models import User


def index(request):
    return render(request, "index.html")

def home(request):
    user_social_auth = request.user.social_auth.filter(provider='facebook').first()
    graph = facebook.GraphAPI(user_social_auth.extra_data['access_token'])
    profile_data = graph.get_object("me")
    friends = graph.get_object("me/friends")
    picture = graph.get_object("me/picture", height="400")
    print "THe type is ", type(User.objects.order_by('?'))
    all_users = User.objects.order_by('?').exclude(email=request.user.email)
    other_user = all_users[0]
    data = {
        'profile_data': profile_data,
        'friends': friends,
        'picture': picture,
        'other_user': other_user
    }
    return render(request, "home.html", data)

# 10.12.4.254:8000/caller
def caller(request):
    user_social_auth = request.user.social_auth.filter(provider='facebook').first()
    graph = facebook.GraphAPI(user_social_auth.extra_data['access_token'])
    profile_data = graph.get_object("me")
    friends = graph.get_object("me/friends")
    picture = graph.get_object("me/picture", height="400")
    data = {
        'profile_data': profile_data,
        'friends': friends,
        'picture': picture
    }
    return render(request, "caller.html", data)


def callee(request):
    return render(request, "callee.html")