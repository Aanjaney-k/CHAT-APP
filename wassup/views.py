from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q

from .models import Message

# Demo-only fixed user list (no passwords, just pick who you are)
USERS = ["Alice", "Bob"]


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if username in USERS:
            request.session["username"] = username
            return redirect("home")

    return render(request, "login.html", {"users": USERS})


def logout_view(request):
    request.session.flush()
    return redirect("login")


def home(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")

    other_users = [u for u in USERS if u != username]

    return render(request, "home.html", {
        "username": username,
        "other_users": other_users,
    })


def history(request, user1, user2):
    messages = Message.objects.filter(
        (Q(sender=user1) & Q(receiver=user2)) | (Q(sender=user2) & Q(receiver=user1))
    )
    data = [
        {"sender": m.sender, "message": m.message}
        for m in messages
    ]
    return JsonResponse({"messages": data})