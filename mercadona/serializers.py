import ordering as ordering

from .models import Product, Category
from rest_framework import serializers



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'description', 'product_label', 'category', 'picture_file', 'price', 'reduction', 'begin_promo',
                  'end_promo']
        ordering = ["picture_file"]


