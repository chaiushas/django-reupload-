from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.views import generic
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from .utils import cookieCart, cartData, guestOrder
from .forms import CommentForm
import json
import datetime
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

# Create your views here.
def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems':cartItems}
    return render(request, 'index.html', context)


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'products':products, 'cartItems':cartItems, 'page_obj': page_obj}
    return render(request, 'store.html', context)


class ProductDetailView(FormMixin, generic.DetailView):
    model = Product
    template_name = 'product_detail.html'
    form_class = CommentForm

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.product = self.object
        form.instance.commenter = self.request.user
        form.save()
        return super(ProductDetailView, self).form_valid(form)


class ProductUserCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'price', 'image', 'description']
    success_url = "/"
    template_name = 'product_create_form.html'

    def form_valid(self, form):
        self.request.user.is_superuser = self.request.user
        return super().form_valid(form)


class ProductUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'price', 'image', 'description']
    success_url = "/"
    template_name = 'product_create_form.html'

    def form_valid(self, form):
        self.request.user.is_superuser = self.request.user
        return super().form_valid(form)

    def test_func(self):
            return self.request.user.is_superuser
    

class ProductUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = "/"
    template_name = 'product_delete.html'

    def form_valid(self, form):
        self.request.user.is_superuser = self.request.user
        return super().form_valid(form)

    def test_func(self):
            return self.request.user.is_superuser


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html', context)


@csrf_protect
def register(request):
    if request.method == "POST":

        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username "{username}" is taken!')
                return redirect('register')
                
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with email "{email}" is already registered!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password, first_name = first_name, last_name = last_name)
                    messages.info(request, f'User "{username}" is registered!')
                    return redirect('login')
        else:
            messages.error(request, "Passwords don't match!")
            return redirect('register')
    return render(request, 'registration/register.html')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action :', action)
    print('productId :',productId)
    client = request.user.client
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(client=client, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    print(f"Data: {request.body}")
    order_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        client = request.user.client
        order, created = Order.objects.get_or_create(client=client, complete=False)

    else:
        client, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.order_id = order_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    Shipping.objects.create(
        client = client,
        order = order,
        address = data['shipping']['address'],
        city = data['shipping']['city'],
        state = data['shipping']['state'],
        zipcode = data['shipping']['zipcode'],
        )
    return JsonResponse('Payment complete', safe=False)