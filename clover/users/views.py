from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import redirect
from .models import *
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
import operator
import collections

from .lib import core
from .lib import kitmap as kits
from .lib import practice as practice_lib
from .lib import hcf

import datetime
import json

# Create your views here.
def register_request(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        uuid = request.GET.get('uuid')
        name = request.GET.get('name')

        if not email:
            return JsonResponse({"success": False, "reason": "Email not provided"})

        if not name:
            return JsonResponse({"success": False, "reason": "Username not provided"})

        if not uuid:
            return JsonResponse({"success": False, "reason": "UUID not provided"})

        if RegisterToken.objects.filter(uuid=uuid).exists():
            return JsonResponse({"success": False, "reason": "Request already sent"})

        if User.objects.filter(uuid=uuid).exists():
            return JsonResponse({"success": False, "reason": "Player is already signed up!"})

        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "reason": "Email already exists"})

        token = RegisterToken.objects.create(uuid=uuid, email=email)

        send_mail(
                'Clover Network | Account Registration',
                '\nHey ' + name + '!' +
                '\n\nThanks for signing up on the Clover Network! Please click the link below to finish up your sign-up process!' +
                '\nConfirmation Link: https://clover.gg/register/confirm?token=' + token.id,
                'admin@clover.gg',
                [email],
                fail_silently=False,
            )

        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


def register(request):
    return render(request, 'users/register.html')

def register_confirm(request):
    if request.method == 'POST':
        token_id = request.POST.get('token')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        try:
            token = RegisterToken.objects.get(id=token_id)
        except:
            raise Http404("Token does not exist")
            
        email = token.email
        uuid = token.uuid

        if User.objects.filter(uuid=uuid).exists():
            raise Http404("Player is already signed up!")
        
        if (password != password2):
            raise Http404("Passwords do not match!")

        if User.objects.filter(email=email).exists():
            raise Http404("Email already exists")
        
        user = User.objects.create_user(email=email, uuid=uuid, password=password)
        user.save()
        token.delete()
        return redirect("login")
    elif request.method != 'GET':
        return redirect("index")

    token_id = request.GET.get('token')
    uuid = request.GET.get('uuid')

    try:
        token = RegisterToken.objects.get(id=token_id)
    except expression as identifier:
        raise Http404("Token does not exist")

    return render(request, 'users/register-confirm.html', {"data": core.get_player_by_uuid(token.uuid), "token": token})

def logout_page(request):
    logout(request)

    return redirect('index')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
  
        if not username:
            raise Http404("Username not found!")

        if not password:
            raise Http404("Password not found")
 
        data = core.get_player_ignore_case(username)

        if not data:
            raise Http404("Player not found")

        uuid = data['uuid']
        
        user = authenticate(request, username=uuid, password=password)
        login(request, user)
        # user.ip_address = get_client_ip(request)
        
        return redirect("index")

    return render(request, 'users/login.html')


def user(request, user):
    data = core.get_player_ignore_case(user)
    if not data:
        raise Http404("Player has never logged onto the server.")

    ip = get_client_ip(request)
    uuid = data['uuid']
    now = datetime.datetime.now()
    month = now.month
    year = now.year

    visits = UserVisit.objects.filter(date__month=month).filter(date__year=year).filter(visited_user=uuid)

    if not visits.filter(viewed_by=ip).exists():
        UserVisit.objects.create(viewed_by=ip, visited_user=uuid)

    return render(request, 'users/detail/general.html',
                  {"data": data, "practice": practice_lib.get_player(data['uuid']),
                   "views": visits})


def api_get_trending_players(request):
    now = datetime.datetime.now()
    month = now.month
    day = now.day
    year = now.year

    visits = UserVisit.objects.filter(date__month=month).filter(date__day=day).filter(date__year=year)

    data = {}

    for visits in visits:
        amount = 1

        if visits.visited_user in data:
            amount =  data[visits.visited_user] + 1
        
        data[visits.visited_user] = amount
    
    data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)

    return JsonResponse({"success": True, "data": data})


def api_get_player(request, uuid):
    data = core.get_player_by_uuid(uuid)

    if not data:
        raise Http404("User not found")

    data = {
        "name": data["name"],
        "uuid": data["uuid"],
        "rank": data["webData"]["rank"],
        "color": core.fix_chat_color(data["webData"]["color"]),
    }

    return JsonResponse({"success": True, "data": data})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip