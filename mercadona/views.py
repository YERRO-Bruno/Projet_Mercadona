from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, User, VerifAdmin
from rest_framework import viewsets
from .serializers import ProductSerializer, CategorySerializer
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from django.contrib import messages
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from imagekitio import ImageKit
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import json


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
                # userx = User.objects.create_user(email=emailx, password=passwordx)
                # userx = UserManager()
                userx = User.objects.create_user(email=emailx, password=passwordx, role="admin")
                # suppression de l'enregistrememnt du code de verification et de l'email associée
                verif_admins[i].delete()
                # connexion
                return redirect('/mercadona/connect')
        # Pas authentifié
        return render(request, 'register.html', {'errorVerif': "Email et/ou code de vérification erroné"})
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


def administration(request):
    context = {}
    if not request.user.is_authenticated:
        ##NOT AUTHENTIFIED
        messages.add_message(request, messages.INFO, "Vous n' êtes pas connecté")
        return redirect("/mercadona/connect")
    else:
        userx = User.objects.get(email=request.user.email)
        if userx is not None:
            if not userx.role == "admin":
                ##NOT ADMINISTRATOR
                messages.add_message(request, messages.INFO, "Vous n' êtes pas administrateur")
                return redirect("/mercadona/connect")

    #L'utilisateur est un administrateur
    context["vlogin"] = "logged"
    context.update(csrf(request))
    if request.method == 'POST':
        idx = request.POST['prodid']
        btnx = request.POST['BTN']
        addcatx = request.POST['addcat']
        updcatx = request.POST['updcat']
        imgx = request.POST['fileimage']
        labelx = request.POST['label']
        descriptionx = request.POST['description']
        catx = request.POST['categ']
        pricex = request.POST['price']
        promox = request.POST['promo']
        print(request.POST['begin'])
        beginx = request.POST['begin']
        endx = request.POST['end']
        context['prodid'] = idx
        context['label'] = labelx
        context['addcat'] = addcatx
        context['updcat'] = updcatx
        context['description'] = descriptionx
        context['fileimage'] = imgx
        context['categ'] = catx
        context['price'] = pricex
        context['promo'] = promox
        context['begin'] = beginx
        context['end'] = endx
        print(context)
        # ADD CATEGORY
        if btnx == "addcat":

            retour = Category.create_category(Category(), label=addcatx)
            if retour['obj'] is not None:
                context["vlogin"] = "logged"
                context.update(csrf(request))
                messages.add_message(request, messages.INFO, "Catégorie ajoutée")
                return render(request, "administration.html", context)
            else:
                context['errorline'] = retour['msg']
                return render(request, "administration.html", context)
        #UPDATE CATEGORY
        if btnx == "updcat":
            category_updated = Category.objects.filter(label=catx).first()
            updcat_id = category_updated.id
            retour = Category.update_category(Category(), updcat_id, updcatx)
            if retour['obj'] is not None:
                context["vlogin"] = "logged"
                context.update(csrf(request))
                messages.add_message(request, messages.INFO, "Catégorie modifiée")
                return render(request, "administration.html", context)
            else:
                context['errorline'] = retour['msg']
                return render(request, "administration.html", context)
        if btnx == "delcat":
            category_deleted = Category.objects.filter(label=catx).first()
            delcat_id = category_deleted.id
            retour = Category.delete_category(Category(), delcat_id)
            if retour['obj']:
                context = {}
                context["vlogin"] = "logged"
                context.update(csrf(request))
                messages.add_message(request, messages.INFO, "Catégorie supprimée")
                return render(request, "administration.html", context)
            else:
                context['errorline'] = retour['msg']
                return render(request, "administration.html", context)
        # ADD PRODUCT
        if btnx == "new":
            if idx != "0":
                messages.add_message(request, messages.INFO,
                                     "vous devez 'Effacer les champs' avant de 'créer produit'")
                return render(request, "administration.html", context)
            else:
                retour = Product.create_product(Product(), labelx, descriptionx, catx, imgx, pricex, promox, beginx,
                                                endx)
                if retour['obj'] is not None:
                    context = {}
                    context["vlogin"] = "logged"
                    context.update(csrf(request))
                    messages.add_message(request, messages.INFO, "Produit ajoutéé")
                    return render(request, "administration.html", context)
                else:
                    context['errorline'] = retour['msg']
                    messages.add_message(request, messages.INFO, "Produit NON ajoutéé")
                    return render(request, "administration.html", context)
        # UPDATE PRODUCT
        if btnx == "updat":
            print(beginx)
            retour = Product.update_product(Product(), idx, labelx, descriptionx, catx, imgx, pricex, promox,
                                            beginx, endx)
            if retour['obj'] is not None:
                messages.add_message(request, messages.INFO, "Produit modifié")
                return render(request, "administration.html", context)
            else:
                print("erreurupdate")
                context['errorline'] = retour['msg']
                return render(request, "administration.html", context)
        # DELETE PRODUCT
        if btnx == "suppr":
            retour = Product.delete_product(Product(), product_id=idx)
            if retour['obj'] is not None:
                context = {}
                context["vlogin"] = "logged"
                context.update(csrf(request))
                messages.add_message(request, messages.INFO, "Produit supprimé")
                return render(request, "administration.html", context)
            else:
                context['errorline'] = retour['msg']
                return render(request, "administration.html", context)
    else:
        return render(request, "administration.html", context)


#API ,images serveur IMAGEKIT.IO
def pictures(request):
    imagekit = ImageKit(
        public_key='public_JqHpBljMCPzQEgTZ61Yz++1LfKs=',
        private_key='private_LJ/YlRNoJAL8T7FAPZl/aNAw+qk=',
        url_endpoint='https://ik.imagekit.io/kpvotazbj'
    )
    listfiles = imagekit.list_files()
    response = {}
    i = 0
    for picture in listfiles.list:
        key = "img{}".format(i)
        response[key] = listfiles.list[i].name
        i += 1
    return JsonResponse(response)
