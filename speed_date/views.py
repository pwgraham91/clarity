import json
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import facebook
from datetime import datetime, timedelta
from speed_date.models import User, Chat, Match


def index(request):
    return render(request, "index.html")

@login_required
def home(request):
    # Get facebook data from user
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


# How to have someone else login on their own computer locally 10.12.4.254:8000/caller (will not work with facebook)
# Only one caller page for RTC
@login_required
def caller(request):
    # Get Facebook information
    user_social_auth = request.user.social_auth.filter(provider='facebook').first()
    graph = facebook.GraphAPI(user_social_auth.extra_data['access_token'])
    profile_data = graph.get_object("me")
    friends = graph.get_object("me/friends")
    picture = graph.get_object("me/picture", height="400")
    # Filtering by gender and preference
    user_gender = request.user.gender
    user_preference = request.user.preference
    # Filter by recently online users
    recent_range = datetime.now() - timedelta(seconds=5)
    # show a list of users who 1) fit my preference 2) whose preference fits me 3) randomly
    # 4) on the chat page in the last 5 seconds and 5) exclude myself
    # Try with
    all_users = User.objects.filter(gender=user_preference).\
        filter(preference=user_gender).order_by('?').exclude(email=request.user.email)
    other_user = all_users[0]
    try:
        all_users = User.objects.filter(gender=user_preference).\
            filter(preference=user_gender).filter(online=recent_range).\
            order_by('?').exclude(email=request.user.email)
        other_user = all_users[0]
    except:
        pass
    # Give me the first user in this list
    # For testing purposes, rewrite other_user to give me my alter FB account
    # all_users = User.objects.filter(first_name='Peter').exclude(email=request.user.email)
    # other_user = all_users[0]
    data = {
        'profile_data': profile_data,
        'friends': friends,
        'picture': picture,
        'other_user': other_user
    }
    return render(request, "caller.html", data)

@login_required
def callee(request):
    return render(request, "callee.html")

@login_required
def loc(request):
    # pnt = Point(-95.23592948913574, 38.97127105172941)
    # imperial_d = D(mi=5)
    return render(request, "firebase_chat.html")

def chat_messages(request, dater_username):
    target_dater = User.objects.get(username=dater_username)
    message_sent = Chat.objects.filter(sender=request.user, recipient=target_dater)
    message_received = Chat.objects.filter(sender=target_dater, recipient=request.user)
    messages = []
    for message in message_sent:
        messages.append(message)
    for message in message_received:
        messages.append(message)
    if len(messages) > 0:
        messages.sort(key=lambda x: x.time, reverse=False)
    data = {
        'messages': messages,
        'target_dater': target_dater,
    }
    return render(request, 'chat_messages.html', data)

def chat_with(request, dater_username):
    user = User.objects.get(email=request.user.email)
    liked_one = User.objects.get(username=dater_username)
    my_match = Match.objects.create(logged_user=user, chosen_user=liked_one, user1_select=True)
    my_match.save()
    data = {
        'liked_one': liked_one,
    }
    return render(request, 'chat_with.html', data)

@csrf_exempt
def new_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = Chat.objects.create(
            message=data['message'],
            sender=User.objects.get(id=data['sender']),
            recipient=User.objects.get(username=data['recipient'])
        )
    response = serializers.serialize('json', [message])
    return HttpResponse(response, content_type='application/json')


def gender(request, user_gender, user_preference):
    user_gender = int(user_gender)
    user_preference = int(user_preference)
    if user_gender == 0:
        request.user.gender = False
    elif user_gender == 1:
        request.user.gender = True
    request.user.save()
    if user_preference == 0:
        request.user.preference = False
        print 0
    elif user_preference == 1:
        request.user.preference = True
        print 1
    request.user.save()
    print request.user.gender
    print request.user.preference
    return HttpResponse("Gendered")


def online(request):
    user = User.objects.get(email=request.user.email)
    user.online = datetime.now()
    print user.online
    user.save()
    return HttpResponse("online now")


def liked(request, dater_username):
    user = User.objects.get(email=request.user.email)
    liked_one = User.objects.get(username=dater_username)
    my_match = Match.objects.create(logged_user=user, chosen_user=liked_one, user1_select=True)
    my_match.save()
    return HttpResponse("liked")


def mutual(request, dater_username):
    user = User.objects.get(email=request.user.email)
    liked_one = User.objects.get(username=dater_username)
    my_match = Match.objects.create(logged_user=user, chosen_user=liked_one, user1_select=True)
    my_match.save()
    return HttpResponse("liked")