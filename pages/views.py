from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterUserForm, UserUpdateForm
from django.contrib.auth import login, logout, authenticate
from .models import Food, Cart, CartItem, Order, OrderItem
from django.core.exceptions import ObjectDoesNotExist
from joblib import load
import numpy as np

# Create your views here.
def home(request):
    context = {}
    return render(request, 'pages/home.html', context)

def menu(request):
    items = Food.objects.all()
    context = {'items': items}
    return render(request, 'pages/menu.html', context)

def account(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Account with username {request.user.username} has succesfully been updated!')
            return redirect('account')
    form = UserUpdateForm(instance=request.user)
    context = {'form': form}
    return render(request, 'pages/account.html', context)

def orders(request):
    context = {}
    return render(request, 'pages/orders.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username (or) Password is incorrect')

    context = {}
    return render(request, 'pages/login.html', context)

def logoutUser(request):
    if not request.user.is_authenticated:
        return redirect('home')
    messages.success(request, f'{request.user} has been succesfully logged out.')
    logout(request)
    return redirect('login')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterUserForm()
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {user}')
            return redirect('login')
        
    context = {'form': form}
    return render(request, 'pages/register.html', context)

def vegetarian(request):
    items = Food.objects.all().filter(vegetarian=True)
    context = {'items': items}
    return render(request, 'pages/menu.html', context)

def nonvegetarian(request):
    items = Food.objects.all().filter(vegetarian=False)
    context = {'items': items}
    return render(request, 'pages/menu.html', context)

def search(request):
    items = Food.objects.filter(name__contains=request.GET['name'])
    context = {'items': items}
    return render(request, 'pages/menu.html', context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, food_id):
    food = Food.objects.get(id=food_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()
    try:
        cart_item = CartItem.objects.get(item=food, cart=cart)
        if cart_item.quantity < cart_item.item.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            item=food,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart')

def cart(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.item.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        try:
            email = request.POST['email']
            name = request.POST['name']
            address = request.POST['address']
            city = request.POST['city']
            postcode = request.POST['postcode']
            country = request.POST['country']
            try:
                order_details = Order.objects.create(
                    total = total,
                    emailAddress=email,
                    name=name,
                    address=address,
                    city=city,
                    postcode=postcode,
                    country=country
                )
                order_details.save()
                for order_item in cart_items:
                    or_item = OrderItem.objects.create(
                        item = order_item.item.name,
                        quantity=order_item.quantity,
                        price=order_item.item.price,
                        order=order_details
                    )
                    or_item.save()
                    items = Food.objects.get(id=order_item.item.id)
                    items.stock = int(order_item.item.stock - order_item.quantity)
                    items.save()
                    order_item.delete()
                    print('done')
                return redirect('thanks')
            except:
                print('error')
        except:
            print('error2')

    context = {'cart_items': cart_items, 'total': total, 'counter': counter}
    return render(request, 'pages/cart.html', context)

def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Food, id=product_id)
    cart_item = CartItem.objects.get(item=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def cart_remove_product(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Food, id=product_id)
    cart_item = CartItem.objects.get(item=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

def recommendation_form(request):
    if request.method == 'POST':
        classifier = load("pages/model/sdp_ml.pkl")
        # glucose, bloodpressure, skinthickness, insulin, bmi, age --> outcome
        glucose = float(request.POST.get('glucose'))
        bloodpressure = float(request.POST.get('bloodpressure'))
        skinthickness = float(request.POST.get('skinthickness'))
        insulin = float(request.POST.get('insulin'))
        bmi = float(request.POST.get('bmi'))
        age = float(request.POST.get('age'))
        healthy = classifier.predict(np.array([[glucose, bloodpressure, skinthickness, insulin, bmi, age]]))[0]
        message = None
        if healthy == 0:
            message = 'Not Healthy'
        else:
            message = 'Healthy'
        items = Food.objects.all().filter(healthy=True)
        context = {'message': message, 'items': items}

        return render(request, 'pages/recommendation_form.html', context)

    message = "Please fill out the details"
    context = {'message': message}
    return render(request, 'pages/recommendation_form.html', context)

def thanks(request):
    context = {}
    return render(request, 'pages/thanks.html', context)