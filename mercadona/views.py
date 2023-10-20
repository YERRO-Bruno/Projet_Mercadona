from django.shortcuts import render,redirect, get_object_or_404
from .models import Product, Category
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import ProductSerializer, CategorySerializer

from django.http import HttpResponse


def index(request):
    return render(request, "index.html")


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
