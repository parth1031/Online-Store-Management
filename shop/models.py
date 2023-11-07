from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customers(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(primary_key=True,max_length=15,default="")
    address = models.TextField(default="",blank=True)
    security_key = models.CharField(max_length=50)

    def __str__(self):
        return str(self.user) or ' '


class Products(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(unique=True, max_length=50)
    price = models.IntegerField(blank=True, default=0)
    quantity = models.IntegerField(blank=True, default=0)
    short_description = models.CharField(max_length=200, blank=True, default="NA")
    category = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to='shop/images', default="",blank=True)
    discount = models.IntegerField(blank=True, default=0)
    sub_category = models.CharField(max_length=30,default="")  # for trending,new-arrivals section
    description=models.CharField(max_length=200, blank=True, default="NA")

    def __str__(self):
        return str(self.product_name) or ' '


class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)
    total_quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)


class cartitems(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user.username) + " " + str(self.product.product_name)


class wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)
    total_quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)


class wishlistitems(models.Model):
    wishlist = models.ForeignKey(wishlist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user.username) + " " + str(self.product.product_name)