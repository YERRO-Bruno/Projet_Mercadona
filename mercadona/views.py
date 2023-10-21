from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, User, VerifAdmin
from rest_framework import viewsets
from .serializers import ProductSerializer, CategorySerializer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def index(request):
    context = {}
    if request.user.is_authenticated:
        context["vlogin"] = "logged"
    else:
        context["vlogin"] = "nologged"
    return render(request, "index.html", context)


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


def logoutUser(request):
    logout(request)
    context = {}
    if request.user.is_authenticated:
        context["vlogin"] = "logged"
    else:
        context["vlogin"] = "nologged"

    return render(request, "logout.html", context)


def loginUser(request):
    context = {}
    if request.user.is_authenticated:
        context["vlogin"] = "logged"
    else:
        context["vlogin"] = "nologged"
    return render(request, "login.html", context)


# Inscription administrateur
def register(request):
    if request.method == 'POST':
        emailx = request.POST['email']
        passwordx = request.POST['password']
        verificationx = request.POST['verification']
        verif_admins = VerifAdmin.objects.all()
        # recherche du code de verification pour l'email de l'administrateur à créer
        for i in range(len(verif_admins)):
            if (verif_admins[i].email == emailx and verif_admins[i].verification == verificationx):
                userx = User.objects.create_user(email=emailx, password=passwordx)
                # suppression de l'enregistrememnt du code de verification et de l'email associée
                verif_admins[i].delete()
                # connexion
                return redirect('/mercadona/connect')
        # Pas authentifié
        return render(request,'register.html', {'errorVerif': "Email et/ou code de vérification erroné"})
    else:
        return render(request, 'register.html')


def connect(request):
    if request.method == 'POST':
        emailx = request.POST['email']
        passwordx = request.POST['password']
        userConnected = authenticate(email=emailx, password=passwordx)
        if userConnected is not None:

            login(request, userConnected)
            request.session['email'] = emailx
            request.session['password'] = passwordx

            return redirect("/mercadona/login")
        else:
            # messages.add_message(request, messages.INFO, "Vous n' avez pas été authentifié")
            return render(request, 'connect.html', {'errorLogin': "Email et/ou mot de passe erroné"})
    else:
        return render(request, 'connect.html')
