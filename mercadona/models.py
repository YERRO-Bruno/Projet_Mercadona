from django.db import models

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
