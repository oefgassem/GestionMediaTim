from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import ObjectDoesNotExist
from app.models import Adherent


def index(request):
    if request.user.is_anonymous:
        return redirect("/login.html")
    return html(request, "index")



def adherent_table(request):
    adherents = Adherent.objects.all()
    context= {
            "adherents":adherents
    }
    return render(request, "adherent_table.html", context=context)

def adherent_detail(request, pk):
    adhde = Adherent.objects.get(id=pk)
    context = {
        "adherent":adhde
    }
    return render(request, "adherent_detail.html", context=context)

def html(request, filename):
    context = {"filename": filename,
               "collapse": ""}
    if request.user.is_anonymous and filename != "login":
        return redirect("/login.html")
    if filename == "logout":
        logout(request)
        return redirect("/")
    if filename == "login" and request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            if "@" in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                context["error"] = "Wrong password"
        except ObjectDoesNotExist:
            context["error"] = "User not found"

        print("login")
        print(username, password)
    print(filename, request.method)
    if filename == "adherent_table":
        adherents = Adherent.objects.all()
        context= {
            "adherents":adherents
        }
    return render(request, f"{filename}.html", context=context)

