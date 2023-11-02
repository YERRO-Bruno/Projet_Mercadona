import os
import re
import string, decimal
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
from django.db import DatabaseError
from decimal import Decimal, DecimalException
from datetime import date
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projet_mercadona.settings")

def est_email(val):
    # Modèle d'expression régulière pour une adresse e-mail valide
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+'

    # Utilisez la fonction match() pour vérifier si la chaîne correspond au modèle
    if re.match(pattern, val):
        return True
    else:
        return False

class Category(models.Model):
    label = models.CharField(max_length=64, unique=True, null=False)

    # def __init__(self, label, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.label = label

    def __str__(self):
        return str(self.label)

    def __get__(self):
        return {'id': self.id, 'label': self.label}

    def create_category(self, label: string):
        try:
            if label == "" or label is None:
                return {'obj': None, 'msg': "Categorie inexistante"}
            category_created_yet = Category.objects.filter(label=label).first()
            if category_created_yet:
                return {'obj': None, 'msg': "Catégorie déjà existante"}
            category = Category()
            category.label = label
            category.save()
            return {'obj': category, 'msg': "Created"}
        except DatabaseError:
            return {'obj': None, 'msg': "PB base de données"}

    def update_category(self, category_id, label):
        try:
            category = Category.objects.get(id=category_id)
            if category:
                category.label = label
                category.save()
                return {'obj': category, 'msg': "Catégorie non trouvée"}
            else:
                return {'obj': None, 'msg': "Catégorie non trouvée"}
        except (Category.DoesNotExist, DatabaseError):
            return {'obj': None, 'msg': "Catégorie non trouvée"}

    def delete_category(self, category_id):
        try:
            category = Category.objects.get(id=category_id)
            if category:
                category.delete()
                return {'obj': True, 'msg': "Catégorie supprimée"}
            else:
                return {'obj': False, 'msg': "Catégorie non trouvée ou erreur base de donnée"}
        except (Category.DoesNotExist, DatabaseError):
            return {'obj': False, 'msg': "Catégorie non trouvée ou erreur base de donnée"}


class Product(models.Model):
    product_label = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    picture_file = models.CharField(null=True, max_length=64)  # filename ex 'pantalon.jpg'
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reduction = models.DecimalField(max_digits=3, decimal_places=0)  # ex 10 for 10%
    begin_promo = models.DateField(null=True)
    end_promo = models.DateField(null=True)

    class Meta:
        ordering = ["-picture_file"]

    def __str__(self):
        return str(self.product_label)

    def create_product(self, product_label: string, description: string, category_label, picture_file: string,
                       price: decimal,
                       reduction: decimal, begin_promo, end_promo):
        try:
            if product_label == "" or product_label is None:
                return {'obj': None, 'msg': "label inexistant"}
            if description == "" or description is None:
                return {'obj': None, 'msg': "description inexistante"}
            if picture_file == "" or picture_file is None:
                return {'obj': None, 'msg': "image inexistante"}
            if category_label == "" or category_label is None:
                return {'obj': None, 'msg': "Categorie introuvable"}
            categoryc = Category.objects.filter(label=category_label).first()
            if price == "" or price is None:
                return {'obj': None, 'msg': "prix inexistante"}
            if not isinstance(Decimal(price), Decimal):
                return {'obj': None, 'msg': "prix non décimal"}
            if reduction == "" or reduction is None:
                reduction = 0
            if reduction is not None:
                if not isinstance(Decimal(reduction), Decimal):
                    return {'obj': None, 'msg': "réduction non décimal"}
            formdt = "%Y-%m-%d"
            if begin_promo == "" or begin_promo is None:
                begin_promo = date(2000, 12, 25)
            if not isinstance(begin_promo, date):
                return {'obj': None, 'msg': "date de début n'est pas une date"}
            if end_promo == "" or end_promo is None:
                end_promo = date(2000, 12, 25)
            if not isinstance(end_promo, date):
                return {'obj': None, 'msg': "date de fin n'est pas une date"}
            product = Product()
            product.product_label = product_label
            product.description = description
            product.picture_file = picture_file
            product.category = categoryc
            product.price = price
            product.reduction = reduction
            product.begin_promo = begin_promo
            product.end_promo = end_promo
            product.save()
            return {'obj': product, 'msg': "Created"}
        except DatabaseError:
            return {'obj': None, 'msg': "error DATABASE"}
        except decimal.DecimalException:
            return {'obj': None, 'msg': DecimalException}

    def update_product(self, product_id, product_label: string, description: string, category_label, picture_file: string,
                       price: decimal, reduction, begin_promo, end_promo):
        try:
            # print("date " + str(begin_promo))
            if product_id == "" or product_id is None:
                return {'obj': None, 'msg': "produit non trouvé"}
            if not isinstance(Decimal(product_id), Decimal):
                return {'obj': None, 'msg': "produit non trouvé"}
            product = Product.objects.filter(id=product_id).first()
            if product:
                if product_label == "" or product_label is None:
                    return {'obj': None, 'msg': "label inexistant"}
            else:
                return {'obj': None, 'msg': "produit inexistant"}
            if description == "" or description is None:
                return {'obj': None, 'msg': "description inexistante"}
            if picture_file == "" or picture_file is None:
                return {'obj': None, 'msg': "image inexistante"}
            categoryc = Category.objects.filter(label=category_label).first()
            if categoryc is None:
                return {'obj': None, 'msg': "Categorie introuvable"}
            if price is None:
                return {'obj': None, 'msg': "prix inexistante"}
            if not isinstance(Decimal(price), Decimal):
                return {'obj': None, 'msg': "prix non décimal"}
            if reduction == "" or reduction is None:
                reduction = 0
            if reduction is not None:
                if not isinstance(Decimal(reduction), Decimal):
                    return {'obj': None, 'msg': "réduction non décimal"}
            formdt = "%Y-%m-%d"
            if begin_promo == "" or begin_promo is None:
                begin_promo = date(2000, 12, 25)
            # print(begin_promo)
            if not isinstance(begin_promo, date):

                begin_promo = date(2000, 12, 25)
            # print("pasdate")
            if end_promo == "" or end_promo is None:
                end_promo = date(2000, 12, 25)
            # if not isinstance(end_promo, date):
            #     end_promo = date(2000, 12, 25)
            product = Product()
            product.id = product_id
            product.product_label = product_label
            product.description = description
            product.category = categoryc
            product.picture_file = picture_file
            product.price = price
            product.reduction = reduction
            product.begin_promo = begin_promo
            product.end_promo = end_promo
            product.save()
            return {'obj': product, 'msg': "Updated"}
        except DatabaseError:
            return {'obj': None, 'msg': "PB base de données"}

        except decimal.DecimalException:
            return {'obj': None, 'msg': DecimalException}
        except Exception:
            return {'obj': None, 'msg': Exception}

    def delete_product(self, product_id):
        try:
            if (product_id == "" or product_id is None):
                return {'obj': False, 'msg': "Produit non trouvé"}
            product = Product.objects.filter(id=product_id).first()
            if product:
                product.delete()
                return {'obj': True, 'msg': "Produit supprimé"}
            else:
                return {'obj': False, 'msg': "Produit non trouvé"}

        except (Category.DoesNotExist, DatabaseError):
            return {'obj': False, 'msg': "produit non trouvé"}


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=16, default=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class VerifAdmin(models.Model):
    email = models.CharField(max_length=64, null=False, unique=True)
    verification = models.CharField(null=True, max_length=128)

    def __str__(self):
        return self.email



    def create_verifadmin (self, verif_email):
        if verif_email == "" or verif_email is None:
            return {'obj': None, 'msg': "email inexistante"}
        if not est_email(verif_email):
            return {'obj': None, 'msg': "email non conforme"}
        try:
            verifadmin = VerifAdmin()
            verifadmin.email = verif_email
            verifadmin.verification = ""
            verifadmin.save()
            return {'obj': verifadmin, 'msg': "créé"}
        except DatabaseError:
            return {'obj': None, 'msg': "PB base de données"}

    def update_verifadmin(self, email, verification):
        if email == "" or email is None:
            return {'obj': False, 'msg': "non trouvé"}
        verifadmin = VerifAdmin.objects.filter(email=email).first()
        if verifadmin:
            verifadmin.verification = verification
            verifadmin.save()
            return {'obj': verifadmin, 'msg': "mise à jour effevtuée"}
        else:
            return {'obj': None, 'msg': "PB base de données"}

    def delete_verifadmin(self, email):
        if email == "" or email is None:
            return {'obj': False, 'msg': "non trouvé"}
        verifadmin = VerifAdmin.objects.filter(email=email).first()
        if verifadmin:
            verifadmin.delete()
            return {'obj': True, 'msg': "suppression effevtuée"}
        else:
            return {'obj': False, 'msg': "PB base de données"}

