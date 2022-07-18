from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.signals import user_logged_in

from myapp.forms import CustomerRegistrationForm, CustomerProfileForm
from myapp.models import Customer, Product, Cart, OrderPlaced
from django.core.cache import cache

# def product(request):
#     return render(request, 'app/home.html')


def mobile(request, data=None):

    if data is None:
        mobile = Product.objects.filter(category='M')
    elif data == 'Samsung' or data == 'Apple' or data == 'Realme':
        mobile = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobile = Product.objects.filter(category='M').filter(discounted_price__lt=50001)
    elif data == 'above':
        mobile = Product.objects.filter(category='M').filter(discounted_price__gt=50000)

    context = {'mobiles': mobile}
    return render(request, 'app/mobile.html', context)


def laptop(request, data=None):

    if data is None:
        laptop = Product.objects.filter(category='L')
    elif data == 'Apple' or data == 'Asus' or data == 'Dell' or data == 'Gemini' or data == 'Msi' or data == 'Razer':
        laptop = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptop = Product.objects.filter(category='L').filter(discounted_price__lt=200001)
    elif data == 'above':
        laptop = Product.objects.filter(category='L').filter(discounted_price__gt=200000)

    context = {'laptops': laptop}

    return render(request, 'app/laptop.html', context)


class ProductView(View):

    def get(self, request):
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        tablets = Product.objects.filter(category='TB')
        accessorys = Product.objects.filter(category='AC')
        carts = 0
        if request.user.is_authenticated:
            carts = Cart.objects.filter(user=request.user)

        context = {'mobiles': mobiles,
                   'laptops': laptops,
                   'tablets': tablets,
                   'carts': carts,
                   'accessorys': accessorys
                   }
        return render(request, 'app/home.html', context)


# def product_detail(request):
#  return render(request, 'app/productdetail.html')


class ProductDetailView(View):

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        context = {'product': product, 'item_already_in_cart': item_already_in_cart}
        return render(request, 'app/productdetail.html', context)


# def login(request):
#     return render(request, 'app/login.html')


# def customer-registration(request):
#     return render(request, 'app/customer_registration.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        context = {'form': form}
        return render(request, 'app/customer_registration.html', context)

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        context = {'form': form}

        if form.is_valid():
            messages.success(request, 'Registration Successful!!')
            form.save()
        return render(request, 'app/customer_registration.html', context)


# def profile(request):
#     return render(request, 'app/profile.html')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomerProfileForm()

        # user ip address using session (signals.py):
        ip = request.session.get('ip', 0)

        # user login count using cache (signals.py):
        count = cache.get('count', version=request.user.pk)

        context = {'form': form,
                   'active': 'btn-primary',
                   'ip': ip, 'count': count}

        return render(request, 'app/profile.html', context)

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        context = {'form': form,
                   'active': 'btn-primary'}
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            form = Customer(user=user, name=name, locality=locality, city=city,
                            state=state, zipcode=zipcode)
            form.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully.')

        return render(request, 'app/profile.html', context)


class AddressView(View):

    def get(self, request):
        addr = Customer.objects.filter(user=request.user)
        context = {'addr': addr,
                   'active': 'btn-primary'}
        return render(request, 'app/address.html', context)


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('/cart')


class ShowCartView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            carts = Cart.objects.filter(user=user)
            amount = 0.0
            shipping_amount = 99.0
            total_amount = 0.0
            cart_product = [prod for prod in Cart.objects.all() if prod.user == user]

            if cart_product:
                for prod in cart_product:
                    temp_amount = (prod.quantity * prod.product.discounted_price)
                    amount += temp_amount
                    total_amount = amount + shipping_amount

                context = {'carts': carts, 'total_amount': total_amount, 'amount': amount, 'shipping_amount': shipping_amount}
                return render(request, 'app/addtocart.html', context)
            else:
                return render(request, 'app/empty_cart.html')


class PlusCart(View):
    def get(self, request):
        if request.method == 'GET':
            prod_id = request.GET['prod_id']
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.quantity += 1
            c.save()
            amount = 0.0
            shipping_amount = 99.0
            cart_product = [prod for prod in Cart.objects.all() if prod.user == request.user]
            for prod in cart_product:
                temp_amount = (prod.quantity * prod.product.discounted_price)
                amount += temp_amount

                data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'total_amount': amount + shipping_amount
                       }
            return JsonResponse(data)


class MinusCart(View):
    def get(self, request):
        if request.method == 'GET':
            prod_id = request.GET['prod_id']
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.quantity -= 1
            c.save()
            amount = 0.0
            shipping_amount = 99.0
            cart_product = [prod for prod in Cart.objects.all() if prod.user == request.user]
            for prod in cart_product:
                temp_amount = (prod.quantity * prod.product.discounted_price)
                amount += temp_amount

                data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'total_amount': amount + shipping_amount
                       }
            return JsonResponse(data)


class RemoveCart(View):
    def get(self, request):
        if request.method == 'GET':
            prod_id = request.GET['prod_id']
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.delete()
            amount = 0.0
            shipping_amount = 99.0
            cart_product = [prod for prod in Cart.objects.all() if prod.user == request.user]
            for prod in cart_product:
                temp_amount = (prod.quantity * prod.product.discounted_price)
                amount += temp_amount

                data = {
                    'amount': amount,
                    'total_amount': amount + shipping_amount
                       }
            return JsonResponse(data)


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        address = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 99.0
        total_amount = 0.0
        cart_product = [prod for prod in Cart.objects.all() if prod.user == user]
        if cart_product:
            for prod in cart_product:
                temp_amount = (prod.quantity * prod.product.discounted_price)
                amount += temp_amount
            total_amount = amount + shipping_amount

        context = {'address': address, 'total_amount': total_amount, 'cart_items': cart_items}
        return render(request, 'app/checkout.html', context)


class PaymentDoneView(View):
    def get(self, request):
        user = request.user
        custid = request.GET.get('custid')
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, customer=customer,
                        product=c.product, quantity=c.quantity).save()
            c.delete()
        return redirect("orders")


def buy_now(request):
    return render(request, 'app/buynow.html')


class OrderPlacedView(LoginRequiredMixin, View):
    def get(self, request):
        op = OrderPlaced.objects.filter(user=request.user)
        context = {'order_placed': op}
        return render(request, 'app/orders.html', context)


# def change_password(request):
#     return render(request, 'app/change_password.html')

def setsession(request):
    request.session['fname'] = 'nimesh'
    request.session['mname'] = 'b'
    request.session['lname'] = 'ahir'
    return render(request, 'test/setsession.html')


def getsession(request):
    fname = request.session.get('fname') # default='nimss'
    mname = request.session.get('mname')
    lname = request.session.get('lname')

    # for test in request.session.items():
    #     import pdb;
    #     pdb.set_trace()
    keys = request.session.keys()
    items = request.session.items()
    # import pdb;pdb.set_trace()
    return render(request, 'test/getsession.html', {'fname': fname, 'mname': mname, 'lname': lname, 'keys': keys, 'items': items})


def deletesession(request):
    """delete session dta from browser but not from database"""
    # if 'fname' in request.session:
    #     del request.session['fname']
    # if 'mname' in request.session:
    #     del request.session['mname']
    # if 'lname' in request.session:
    #     del request.session['lname']

    """delete session data from browser as well as from database"""
    request.session.flush()

    return render(request, 'test/delete.html')

