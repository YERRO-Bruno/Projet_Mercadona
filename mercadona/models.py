import string, decimal
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
from django.db import DatabaseError
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date
from django.core.validators import validate_email


class Category(models.Model):
    label = models.CharField(max_length=64, null=False)

    # def __init__(self, label, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.label = label

    def __str__(self):
        return str(self.label)

    def __get__(self):
        return {'id': self.id, 'label': self.label}

    def create_category(self, label: string):
        if label == "" or label is None:
            return {'obj': None, 'msg': "Categorie inexistante"}
        categories = Category.objects.filter(label=label)
        # if categories.exists:
        #     return {'obj': None, 'msg': "Catégorie déjà existante"}
        try:
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
                return category
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

    def __str__(self):
        return str(self.product_label)

    def create_product(self, label: string, description: string, category_id, picture_file: string,
                       price: decimal, reduction: decimal = 0,
                       begin_promo = date(2000,12,25), end_promo=date(200,12,25)):

            if label == "" or label is None:
                return {'obj': None, 'msg': "label inexistant"}
            if description == "" or description is None:
                return {'obj': None, 'msg': "description inexistante"}
            if picture_file == "" or picture_file is None:
                return {'obj': None, 'msg': "image inexistante"}
            category = Category.objects.filter(id=category_id).first()
            if category is None:
                return {'obj': None, 'msg': "Categorie introuvable"}
            if price is None:
                return {'obj': None, 'msg': "prix inexistante"}
            if not isinstance(Decimal(price), Decimal):
                return {'obj': None, 'msg': "prix non décimal"}
            if not isinstance(Decimal(reduction), Decimal):
                return {'obj': None, 'msg': "réduction non décimal"}
            if not isinstance(begin_promo, date):
                return {'obj': None, 'msg': "date de debut n'est pas une date"}
            if not isinstance(end_promo, date):
                return {'obj': None, 'msg': "date de fin n'est pas une date"}
            try:
                product = Product()
                product.product_label = label
                product.description = description
                product.picture_file = picture_file
                product.category = category
                product.price = price
                # product.reduction = reduction
                # product.begin_promo = begin_promo
                # product.end_promo = end_promo
                product.save()
                return {'obj': product, 'msg': "Created"}
            except DatabaseError:
                return {'obj': None, 'msg': category[0].label}

    def update_product(self, product_id, label: string, description: string, category_id, picture_file: string,
                       price: decimal, reduction: decimal = 0,
                       begin_promo = date(2000,12,25), end_promo=date(200,12,25)):
        try:
            if product_id =="" or product_id is None:
                return {'obj': None, 'msg': "product_id inexistant"}
            if not isinstance(Decimal(product_id), Decimal):
                return {'obj': None, 'msg': "product_id non décimal"}
            product = Product.objects.get(id=product_id)
            if product:
                if label == "" or label is None:
                    return {'obj': None, 'msg': "label inexistant"}
                if description == "" or description is None:
                    return {'obj': None, 'msg': "description inexistante"}
                if picture_file == "" or picture_file is None:
                    return {'obj': None, 'msg': "image inexistante"}
                category = Category.objects.filter(id=category_id).first()
                if category is None:
                    return {'obj': None, 'msg': "Categorie introuvable"}
                if price is None:
                    return {'obj': None, 'msg': "prix inexistante"}
                if not isinstance(Decimal(price), Decimal):
                    return {'obj': None, 'msg': "prix non décimal"}
                if not isinstance(Decimal(reduction), Decimal):
                    return {'obj': None, 'msg': "réduction non décimal"}
                if not isinstance(begin_promo, date):
                    return {'obj': None, 'msg': "date de debut n'est pas une date"}
                if not isinstance(end_promo, date):
                    return {'obj': None, 'msg': "date de fin n'est pas une date"}
                product = Product()
                product.product_label = label
                product.description = description
                product.picture_file = picture_file
                product.price = price
                product.reduction = reduction
                product.begin_promo = begin_promo
                product.end_promo = end_promo
                product.save()
                return {'obj': product, 'msg': "Updated"}
            else:
                return {'obj': None, 'msg': "PB base de données"}
        except DatabaseError:
            return {'obj': None, 'msg': "PB base de données"}

    def delete_product(self, product_id):
        try:
            product = Product.objects.get(id=product_id)
            if product:
                product.delete()
                return {'obj': True, 'msg': "Produit supprimée"}
            else:
                return {'obj': False, 'msg': "Produit non trouvée ou erreur base de donnée"}

        except (Category.DoesNotExist, DatabaseError):
            return {'obj': False, 'msg': "produit non trouvée ou erreur base de donnée"}


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
    verification = models.CharField(max_length=128)

    def __str__(self):
        return self.email

    def getVerifAdmin(self):
        return {'id': self.id, 'email': self.email, 'verification': self.verification}
