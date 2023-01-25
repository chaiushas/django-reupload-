from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from tinymce.models import HTMLField

# Create your models here.

class Product(models.Model):
  name = models.CharField('Product name', max_length=200)
  price = models.DecimalField('Product price', max_digits=10, decimal_places=2)
  image = models.ImageField('Product image', null=True, blank=True)
  description = HTMLField(verbose_name='Description', null=True, blank=True)
  date_created = models.DateTimeField(verbose_name='Date of creation', auto_now_add=True)

  def __str__(self):
      return f"{self.name} {self.price} {self.date_created}"

  def get_absolute_url(self):
    return reverse('book-detail', args=[str(self.id)])


class Client(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  first_name = models.CharField('First name', max_length = 100, null=True)
  last_name = models.CharField('Last name', max_length=100, null=True)
  email_field = models.EmailField('Email', max_length=100, help_text='Email of a client', null=True)

  def __str__(self):
      return f"{self.user} {self.first_name} {self.last_name} {self.email_field}"

class Order(models.Model):
  client = models.ForeignKey(Client, verbose_name='Ordered by', on_delete=models.SET_NULL, null=True, blank=True)
  order_id = models.CharField('Order ID', max_length=100, null=True)
  order_date = models.DateTimeField('Date of order', auto_now_add=True)
  complete = models.BooleanField(default=False, null=True, blank=False)

  def __str__(self):
    return f"{self.client} {self.order_id} {self.order_date} {self.complete}"

  @property
  def get_cart_total(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return total

  @property
  def get_cart_items(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.quantity for item in orderitems])
    return total


class OrderItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
  quantity = models.IntegerField(default=0, null=True, blank=True)
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.product} {self.order} {self.quantity} {self.date_added}"

  @property
  def get_total(self):
    total = self.product.price * self.quantity
    return total


class Shipping(models.Model):
  client = models.ForeignKey(Client, verbose_name='Ordered by', on_delete=models.SET_NULL, null=True, blank=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
  address = models.CharField('Address', max_length = 100)
  city = models.CharField('City', max_length = 100)
  state = models.CharField('State', max_length = 100)
  zipcode = models.CharField('Zipcode', max_length = 100)
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.client} {self.order} {self.address} {self.city} {self.state} {self.zipcode} {self.date_added}"


class Comment(models.Model):
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
  commenter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  date_created = models.DateTimeField(auto_now_add=True)
  content = models.TextField('Atsiliepimas', max_length=2000)

  def __str__(self):
      return f"{self.product} {self.commenter} {self.date_created}"
  