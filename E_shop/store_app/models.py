from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Filter(models.Model):
    FILTER_PRICE = (

        ('1000 To 2000', '1000 To 2000'),
        ('2000 To 3000', '2000 To 3000'),
        ('3000 To 4000', '3000 To 4000'),
        ('4000 To 5000', '4000 To 5000'),
        ('5000 To 6000', '5000 To 6000'),
    )
    price = models.CharField(choices=FILTER_PRICE, max_length=60)

    def __str__(self):
        return self.price


class Product(models.Model):
    CONDITION = (
        ('New', 'new'), ('old', 'old')
    )
    STOCK = (
        ('IN STOCK', 'IN STOCK'), ('OUT OF STOCK', 'OUT OF STOCK')
    )
    STATUS = (
        ('Publish', 'Publish'), ('Draft', 'Draft')
    )
    unique_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/img')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    condition = models.CharField(choices=CONDITION, max_length=100)
    information = RichTextField(null=True)
    description = RichTextField(null=True)
    stock = models.CharField(choices=STOCK, max_length=200)
    status = models.CharField(choices=STATUS, max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    Categories = models.ForeignKey(Categories, on_delete=models.CASCADE, default=None)
    Brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=None)
    Color = models.ForeignKey(Color, on_delete=models.CASCADE, default=None)
    Filter = models.ForeignKey(Filter, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

        #
        # def save(self, *args, **kwargs):
        #     if self.unique_id is None and self.created_date and self.id:
        #         self.unique_id = self.created_date.strftime('75%Y%m%d23').str(self.id)
        #     return super.save(*args, **kwargs)




class Images(models.Model):
    image = models.ImageField(upload_to='product_images/img')
    Product = models.ForeignKey(Product, on_delete=models.CASCADE,default=None)




class Tag(models.Model):
    name = models.CharField(max_length=200)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    postcode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=200)
    additional_info = models.TextField()
    amount = models.CharField(max_length=200)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    paid = models.CharField(max_length=200, default=False, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product_images/img')
    quantity = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    total = models.CharField(max_length=200)

    def __str__(self):
        return self.order.user.username