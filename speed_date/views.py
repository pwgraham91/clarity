import json
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import facebook
from geopy import Point
from speed_date.models import User, Chat


def index(request):
    return render(request, "index.html")

def home(request):
    user_social_auth = request.user.social_auth.filter(provider='facebook').first()
    graph = facebook.GraphAPI(user_social_auth.extra_data['access_token'])
    profile_data = graph.get_object("me")
    friends = graph.get_object("me/friends")
    picture = graph.get_object("me/picture", height="400")
    data = {
        'profile_data': profile_data,
        'friends': friends,
        'picture': picture,
        'user': request.user,
    }
    return render(request, "home.html", data)

# 10.12.4.254:8000/caller
def caller(request):
    user_social_auth = request.user.social_auth.filter(provider='facebook').first()
    graph = facebook.GraphAPI(user_social_auth.extra_data['access_token'])
    profile_data = graph.get_object("me")
    friends = graph.get_object("me/friends")
    picture = graph.get_object("me/picture", height="400")
    all_users = User.objects.filter(gender=True).order_by('?').exclude(email=request.user.email)
    other_user = all_users[0]
    other_user = User.objects.get(email='sfpacific100@gmail.com')
    data = {
        'profile_data': profile_data,
        'friends': friends,
        'picture': picture,
        'other_user': other_user
    }
    return render(request, "caller.html", data)


def callee(request):
    return render(request, "callee.html")

def loc(request):
    # pnt = Point(-95.23592948913574, 38.97127105172941)
    # imperial_d = D(mi=5)
    return render(request, "firebase_chat.html")

def chat_messages(request, dater_id):
    target_dater = User.objects.get(pk=dater_id)
    message_sent = Chat.objects.filter(sender=request.user, recipient=target_dater)
    message_received = Chat.objects.filter(sender=target_dater, recipient=request.user)
    messages = []
    for message in message_sent:
        messages.append(message)
    for message in message_received:
        messages.append(message)
    if len(messages) > 0:
        messages.sort(key=lambda x: x.time, reverse=True)
    data = {
        'messages': messages,
        'target_dater': target_dater,
    }
    return render(request, 'chat_messages.html', data)

@csrf_exempt
def new_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = Chat.objects.create(
            message=data['message'],
            sender=User.objects.get(id=data['sender']),
            recipient=User.objects.get(id=data['recipient'])
        )
    response = serializers.serialize('json', [message])
    return HttpResponse(response, content_type='application/json')


def gender(request, user_gender, user_preference):
    user = User.objects.get(email=request.user.email)
    user_gender = int(user_gender)
    user_preference = int(user_preference)
    if user_gender == 0:
        user.gender = False
    elif user_gender == 1:
        user.gender = True
    if user_preference == 0:
        user.preference = False
    elif user_gender == 1:
        user.preference = True
    user.save()
    print "gender" + str(user.gender)
    print "preference" + str(user.preference)
    return HttpResponse("Gendered")