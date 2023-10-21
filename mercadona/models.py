from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    label = models.CharField(max_length=64, null= False)

    def __str__(self):
        return str(self.label)


class Product(models.Model):
    product_label = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    picture_file = models.CharField(null=True, max_length=64)   #filename ex 'pantalon.jpg'
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reduction = models.DecimalField(max_digits=3, decimal_places=0)    # ex 10 for 10%
    begin_promo = models.DateField(null=True)
    end_promo = models.DateField(null=True)

    def __str__(self):
        return str(self.product_label)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=16, default = True)
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