from http.client import HTTPResponse
from mmap import PAGESIZE
from typing import IO
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import ObjectDoesNotExist
from app.models import Adherent
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4


def index(request):
    if request.user.is_anonymous:
        return redirect("/login.html")
    return html(request, "index")

def adherent_detail_pdf(requet, pk):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    adherent = Adherent.objects.get(id=pk)
    lines = []
    
    lines.append(adherent.codeadh)
    lines.append(adherent.nomadh)
    lines.append(adherent.prenomadh)

    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='adherent.pdf')

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

