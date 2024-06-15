from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone

from users.models import User
from .models import *

# Create your views here.
def thread(request, id, title):
    try:
        thread = Thread.objects.get(id=id)
    except Thread.DoesNotExist:
        raise Http404("Thread does not exist")
    
    ip = get_client_ip(request)
    now = datetime.now()
    month = now.month
    year = now.year

    visits = ThreadVisit.objects.filter(date__month=month).filter(date__year=year).filter(thread=thread)

    if not visits.filter(viewed_by=ip).exists():
        ThreadVisit.objects.create(viewed_by=ip, thread=thread)

    return render(request, "forums/thread.html", {"thread": thread, "visits": visits})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def forum(request, forum):
    try:
        forum = forum.replace("_", " ").capitalize()
        forum = Forum.objects.get(name=forum)
    except Forum.DoesNotExist:
        raise Http404("Forum does not exist")
    return render(request, "forums/forum.html", {"forum": forum})

def forums(request):
    return render(request, "forums/forums_main.html", {"categories": Category.objects.all()})

@login_required
def create_thread(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        forum = request.POST.get('forum')
        content = request.POST.get('content')

        try:
            forum = Forum.objects.get(name=forum)
        except Forum.DoesNotExist:
            raise Http404("Forum does not exist")
        
        if forum.is_overview:
            raise HttpResponse("Cannot create an overview thread.")
        
        if not request.user.has_permission("thread.create." + forum.category.name):
            raise HttpResponseForbidden("Lacking the permissions to create a thread in this forum.")

        instance = Thread.objects.create(title=title, forum=forum, author=request.user, content=content)

        return redirect('thread', instance.id, instance.get_slug())

    return render(request, "forums/create_thread.html", {"categories": Category.objects.all()})


#API METHODS
@login_required
def api_reply(request, reply_type):
    if reply_type != "thread" and reply_type != "child":
        return JsonResponse({
            "success": "false",
            "reason": "Invalid Reply type"
        })
    
    if reply_type == "thread" and request.method == 'POST':
        content = request.POST.get('content')
        user = request.user
        thread = request.POST.get('thread')

        try:
            thread = Thread.objects.get(id=thread)
        except Thread.DoesNotExist:
            raise Http404("Thread does not exist")
        
        reply = ThreadReply.objects.create(author=user, thread=thread, content=content)

        return JsonResponse({
            "success": "true",
            "data": reply.id
        })


    if reply_type == "child" and request.method == 'POST':
        content = request.POST.get('content')
        user = request.user
        reply = request.POST.get('reply')

        try:
            reply = ThreadReply.objects.get(id=reply)
        except ThreadReply.DoesNotExist:
            raise Http404("Reply does not exist")
        
        result = ThreadReply.objects.create(author=user, parent_reply=reply, content=content)

        return JsonResponse({
            "success": "true",
            "data": result.id
        })


    return JsonResponse({
            "success": "false",
            "reason": "Invalid HTTP method"
        })

@login_required
def api_reply_edit(request, reply):
    if request.method == 'POST':
        content = request.POST.get('content')

        try:
            reply = ThreadReply.objects.get(id=reply)
        except ThreadReply.DoesNotExist:
            raise Http404("Reply does not exist")
        
        if not content:
            raise HttpResponse("Content is empty!")
        
        if request.user != reply.author and not request.user.has_permission("admin"):
            raise HttpResponse("Invalid permissions!")

        reply.content = content
        reply.edited_by = request.user
        reply.edited_at = timezone.now()
        reply.save()

        return JsonResponse({
            "success": "true"
        })

    return JsonResponse({
            "success": "false",
            "reason": "Invalid HTTP method"
        })

@login_required
def api_reply_delete(request, reply):
    if request.method == 'POST':
        user = request.user

        try:
            reply = ThreadReply.objects.get(id=reply)
        except ThreadReply.DoesNotExist:
            raise Http404("Reply does not exist")
        
        if request.user != reply.author and not request.user.has_permission("admin"):
            raise HttpResponse("Invalid permissions!")

        reply.is_deleted = True
        reply.deleted_by = user
        reply.deleted_at = timezone.now()
        reply.save()

        return JsonResponse({
            "success": "true"
        })

    return JsonResponse({
            "success": "false",
            "reason": "Invalid HTTP method"
        })


@login_required
def api_thread_edit(request, thread):
    if request.method == 'POST':
        user = request.user

        try:
            thread = Thread.objects.get(id=thread)
        except Thread.DoesNotExist:
            raise Http404("Thread does not exist")
        
        if request.user != thread.author and not request.user.has_permission("admin"):
            raise HttpResponse("Invalid permissions!")

        title = request.POST.get('title')
        content = request.POST.get('content')

        if title:
            thread.title = title
        
        if content:
            thread.content = content

        thread.edited_by = user
        thread.edited_at = timezone.now()
        thread.save()

        return JsonResponse({
            "success": "true"
        })

    return JsonResponse({
            "success": "false",
            "reason": "Invalid HTTP method"
        })


def api_reply_get(request, reply):
    if request.method != 'GET':
        return JsonResponse({
            "success": "false",
            "reason": "Invalid HTTP method"
        })

    try:
        reply = ThreadReply.objects.get(id=reply)
    except ThreadReply.DoesNotExist:
        raise Http404("Reply does not exist")

    return render(request, "forums/partial/reply.html", {"reply": reply})


def api_sub_reply_create_partial(request, reply):
    try:
        reply = ThreadReply.objects.get(id=reply)
    except ThreadReply.DoesNotExist:
        raise Http404("Reply does not exist")

    return render(request, "forums/partial/sub-reply-create.html", {"reply": reply, "user": request.user})