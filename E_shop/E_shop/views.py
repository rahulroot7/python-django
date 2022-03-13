from django.shortcuts import render, redirect
from store_app .models import Product, Categories,Filter, Brand,Color,Contact,Order, OrderItem
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import razorpay
from django.views.decorators.csrf import csrf_exempt

client = razorpay.Client(auth=(settings.ROZARPAY_KEY_ID, settings.ROZARPAY_KEY_SECRATE))


def base(request):
    return render(request, 'main/base.html')


def index(request):
    product = Product.objects.filter(status='Publish')

    context = {

        'product':product,
    }
    return render(request, 'main/index.html',context)


def product(request):
    product = Product.objects.filter(status='Publish')
    category = Categories.objects.all()
    price_filter = Filter.objects.all()
    brand = Brand.objects.all()
    color = Color.objects.all()

    CATID = request.GET.get('categories')
    BRANDID = request.GET.get('brand')
    PRICEID = request.GET.get('price')
    COLORID= request.GET.get('color')
    ATOZ = request.GET.get('ATOZ')
    ZTOA = request.GET.get('ZTOA')
    LOWTOHIGH = request.GET.get('PRICE_LOW_TO_HIGH')
    HIGHTOLOW = request.GET.get('PRICE_HIGH_TO_LOW')
    NEW = request.GET.get('new')
    OLD = request.GET.get('old')

    if CATID:
        product = Product.objects.filter(Categories=CATID,status='Publish')
    elif BRANDID:
        product = Product.objects.filter(Brand=BRANDID, status='Publish')
    elif PRICEID:
        product = Product.objects.filter(Filter=PRICEID, status='Publish')
    elif COLORID:
        product = Product.objects.filter(Color=COLORID, status='Publish')
    elif ATOZ:
        product = Product.objects.filter(status='Publish').order_by('name')
    elif ZTOA:
        product = Product.objects.filter(status='Publish').order_by('-name')
    elif LOWTOHIGH:
        product = Product.objects.filter(status='Publish').order_by('price')
    elif HIGHTOLOW:
        product = Product.objects.filter(status='Publish').order_by('-price')
    elif NEW:
        product = Product.objects.filter(status='Publish', condition='New').order_by('-id')
    elif OLD:
        product = Product.objects.filter(status='Publish', condition='old').order_by('-id')

    else:
        product = Product.objects.filter(status='Publish')
    context = {

        'product': product,
        'category':category,
        'brand':brand,
        'color':color,
        'price_filter':price_filter

    }
    return render(request, 'main/product.html', context)

def search(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains = query)

    context = {

        'product':product,
    }
    return render(request, 'main/search.html',context)

def single_product(request, id):
    prod = Product.objects.filter(id=id).first()
    context = {
        'prod':prod,
    }
    return render(request, 'main/single_product.html', context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact(
           name = name,
           email = email,
           subject = subject,
           message = message,
        )

        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail(subject,message, email_from, ['gulab.a1999@gmail.com'])
            contact.save()
            return redirect('index')
        except:
            return redirect('contact')

    return render(request, 'main/contact.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        customer = User.objects.create_user(username, email, password)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('register')
    return render(request, 'Registration/auth.html')


def auth_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')
    return render(request, 'Registration/auth.html')

def auth_logout(request):
    logout(request)

    return redirect('index')


@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_detail(request):

    return render(request, 'cart/cart_detail.html')

def checkout(request):
    amount_str = request.POST.get('amount')
    amount_float = float(amount_str)
    amount = int(amount_float)

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    order_id = payment['id']

    context = {
        'order_id' : order_id,
        'payment' : payment,
    }

    return render(request, 'cart/checkout.html', context)

def placeorder(request):
     if request.method == "POST":
         uid = request.session.get('_auth_user_id')
         user = User.objects.get(id = uid)
         cart = request.session.get('cart')

         firstname = request.POST.get('firstname')
         lastname = request.POST.get('lastname')
         country = request.POST.get('country')
         address = request.POST.get('address')
         city = request.POST.get('city')
         state = request.POST.get('state')
         postcode = request.POST.get('postcode')
         phone = request.POST.get('phone')
         email = request.POST.get('email')
         additional_info = request.POST.get('additional_info')
         amount = request.POST.get('amount')
         order_id = request.POST.get('order_id')
         payment = request.POST.get('payment')

         context = {

             'order_id': order_id,
         }
         order = Order(

         user = user,
         firstname=firstname,
         lastname=lastname,
         country=country,
         address=address,
         city=city,
         state=state,
         postcode=postcode,
         phone=phone,
         email=email,
         additional_info=additional_info,
         amount = amount,
         payment_id= order_id,
        )

     order.save()
     for i in cart:
         a = (int(cart[i]['price']))
         b = cart[i]['quantity']
         total = a + b

         item = OrderItem(
              user = user,
              order = order,
              product = cart[i]['name'],
              image = cart[i]['image'],
              quantity = cart[i]['quantity'],
              price = cart[i]['price'],
              total = total,
          )
         item.save()

         return render(request, 'cart/placeorder.html',  context)
@csrf_exempt
def thankyou(request):
    if request.method == 'POST':
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
        user = Order.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()


    return render(request, 'cart/thankyou.html')

def aboutus(request):
    return render(request, 'main/aboutus.html')

def order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    order = OrderItem.objects.filter(user=user)

    context = {
        'order' : order,
    }
    return render(request, 'cart/yourorder.html',context)