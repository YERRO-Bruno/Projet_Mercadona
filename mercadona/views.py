import smtplib

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, User, VerifAdmin
from rest_framework import viewsets
from .serializers import ProductSerializer, CategorySerializer
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from django.contrib import messages
from projet_mercadona.settings import IMAGEKIT_PUBLIC_KEY, IMAGEKIT_PRIVATE_KEY, IMAGEKIT_URL_ENDPOINT
from imagekitio import ImageKit
from django.http import JsonResponse
import os
import bcrypt
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

global recipient_emailcd


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


def preregister(request):
    if request.method == 'POST':
        emailx = request.POST['email']
        verifadmins = VerifAdmin.objects.all()
        for verifadmin in verifadmins:
            if verifadmin.email == emailx:
                original_code = get_random_string(length=8)
                salt = bcrypt.gensalt()
                crypted_code = bcrypt.hashpw(original_code.encode('utf-8'), salt)
                hash_verif = crypted_code.decode('utf-8')
                verifadmin.verification = hash_verif
                verifadmin.update_verifadmin(verifadmin.email, hash_verif)

                recipient_email = emailx
                mail_subject = "Code de verification pour l'inscription à MERCADONA"
                mail_message = "bonjour, \n"
                mail_message = mail_message + "Veuiller trouvez ci-dessous le code de verification" \
                                              " pour votre inscription au en tant qu'administrateur du site MERCADONA :\n"
                mail_message = mail_message + "\n"
                mail_message = mail_message + original_code
                mail_message = mail_message + "\n"
                mail_message = mail_message + "\n"
                mail_message = mail_message + "Cordialement"

                try:
                    send_mail(mail_subject, mail_message, 'brunoyerro@gmail.com', {emailx},
                              fail_silently=True)
                except Exception as error:
                    print('mail error')
                    print(error)
                return redirect('/mercadona/register')
        return render(request, 'preregister.html',
                      {'errorVerif': "Email non habilité à l'administration", 'email': emailx})

    else:
        return render(request, 'preregister.html')


# Inscription administrateur
def register(request):
    if request.method == 'POST':
        emailx = request.POST['email']
        passwordx = request.POST['password']
        verificationx = request.POST['verification']
        verifadmins = VerifAdmin.objects.all()
        for verifadmin in verifadmins:
            if verifadmin.email == emailx:
                if bcrypt.checkpw(verificationx.encode('utf-8'), verifadmin.verification.encode('utf-8')):
                    print(emailx)
                    try:
                        userx = User.objects.create_user(email=emailx, password=passwordx, role="admin")['obj']
                    except Exception as error:
                        print(error)
                    return redirect('/mercadona/connect')
        print("pas trouvé")
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

    # L'utilisateur est un administrateur
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
        # UPDATE CATEGORY
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
                    context['prodid'] = retour['obj'].id
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


# API ,images serveur IMAGEKIT.IO
def pictures(request):
    imagekit = ImageKit(
        public_key=os.getenv('IMAGEKIT_PUBLIC_KEY'),
        private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
        url_endpoint=os.getenv('IMAGEKIT_URL_ENDPOINT')
    )
    listfiles = imagekit.list_files()
    response = {}
    i = 0
    for picture in listfiles.list:
        key = "img{}".format(i)
        response[key] = listfiles.list[i].name
        i += 1
    return JsonResponse(response)


def page_non_trouvee(request, exception):
    return render(request, '404.html', status=404)
