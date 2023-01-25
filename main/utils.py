import json
from .models import *

def cookieCart(request):
  try:
      cart = json.loads(request.COOKIES['cart'])
  except:
    cart = {}
  print('Cart:', cart)
  items = []
  order = {'get_cart_total':0, 'get_cart_items':0}
  cartItems = order['get_cart_items']

  for item in cart:
    try:
      cartItems += cart[item]['quantity']

      product = Product.objects.get(id=item)
      total = (product.price * cart[item]['quantity'])

      order['get_cart_total'] += total
      order['get_cart_items'] += cart[item]['quantity']

      item = {
          'product':{
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image': product.image
            },
          'quantity': cart[item]['quantity'],
          'get_total': total
          }
      items.append(item)
    except:
      pass
  return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
  if request.user.is_authenticated:
    client = request.user.client
    order, created = Order.objects.get_or_create(client=client, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']
  return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
  print('Not logged in')
  print('COOKIES:', request.COOKIES)
  first_name = data['form']['first_name']
  last_name = data['form']['last_name']
  email_field = data['form']['email_field']

  cookieData = cookieCart(request)
  items = cookieData['items']

  client, created = Client.objects.get_or_create(
    email_field = email_field,
    )

  client.first_name = first_name
  client.last_name = last_name
  client.save()

  order = Order.objects.create(
      client = client,
      complete = False,
      )

  for item in items:
      product = Product.objects.get(id=item['product']['id'])
      orderItem = OrderItem.objects.create(
          product = product,
          order = order,
          quantity = item['quantity']
          )
  return client, order