from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from django.contrib.auth import authenticate, login, logout
from decimal import Decimal
from django.conf import settings

import json
import datetime

from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm


from .models import *
from .forms import *
from .utils import cookieCart, cartData, guestOrder
from .models import *
from .filters import *

# Create your views here.
def about(request):

    return render(request, 'Axis/about.html', {})

def home(request):
    return render(request, 'home_base.html', {})


def store(request, category_slug=None):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    category = None

    products = Product.objects.all()
    categorylist = Category.objects.annotate(total_products=Count('product'))
    context = {'cartItems': cartItems, 'products':products , 'category_list' : categorylist ,'category' : category , 'shipping': False}
    return render(request, 'Axis/store.html', context)



def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'Axis/cart.html', context)

def product_details(request, pk):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    category = None

    categorylist = Category.objects.annotate(total_products=Count('product'))
    product = Product.objects.get(id=pk)
    category = None
    context = {'cartItems': cartItems, 'product':product , 'category_list' : categorylist ,'category' : category , 'shipping': False}
    print("Categry List: ", categorylist)
    return render(request, 'Axis/product.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'Axis/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, status="Pending")

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        if  product.stock >= 1:
            product.stock = (product.stock - 1)
            orderItem.quantity = (orderItem.quantity + 1)
            print("Stock: ",product.stock)

        else:
            messages.success(request, ("There is currently not enough stock available to fullfill your order"))

    elif action == 'remove':
        product.stock = (product.stock + 1)
        print("Stock: ",product.stock)
        orderItem.quantity = (orderItem.quantity - 1)

    product.save()

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def contact(request):
    if request.method == 'POST':
        message = request.POST['message']
        if request.user.is_authenticated:
            name = request.user.username
            email = request.user.email
            message = name + "\n" + email + "\n"+ message
            send_mail('Contact Form', message, settings.EMAIL_HOST_USER, ['christopher@3rdaxis.co.za', 'mcn10.foxx@gmail.com'], fail_silently="false" )
            messages.success(request, ("Your message has been sent successfully..."))
        else:
            name = request.POST['name']
            email = request.POST['email']
            message = name + "\n" + email + "\n"+ message
            send_mail('Contact Form', message, settings.EMAIL_HOST_USER, ['christopher@3rdaxis.co.za', 'mcn10.foxx@gmail.com'], fail_silently="false" )
            messages.success(request, ("Your message has been sent successfully..."))
        return redirect('Axis:store')

    return render(request, 'Axis/contact.html', {})

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status="Pending")
    else:
        customer, order = guestOrder(request, data)

    total = Decimal(data['form']['total'])
    order.transaction_id = transaction_id
    print("Order total:::::::: ", total)

    if total == order.get_cart_total:
        print("Order total is correct")
        order.status = "Payment Confirmed, Processing Order"
        order.save()

    else:
        print("Order total is incorrect")

    if order.shipping == True:
        ShippingAddress.objects.create(
        country=data['shipping']['country'],
        address1=data['shipping']['address1'],
        address2=data['shipping']['address2'],
        city=data['shipping']['city'],
        province=data['shipping']['province'],
        postal_code=data['shipping']['postal_code'],
        )
        Customer.objects.filter(user=request.user).update(shippingAddress='ShippingAddress.id')

# Add code to send email to Store Owner
    return JsonResponse('Payment submitted..', safe=False)



#-------------------(DETAIL/LIST VIEWS) -------------------

def dashboard(request):
    orders = Order.objects.all().order_by('-status')[0:5]
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = Order.objects.all().count()
    delivered = Order.objects.filter(status='Delivered').count()
    pending = Order.objects.filter(status='Pending').count()



    context = {'customers':customers, 'orders':orders,
    'total_customers':total_customers,'total_orders':total_orders,
    'delivered':delivered, 'pending':pending}
    return render(request, 'Axis/AxisCRM/dashboard.html', context)


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    shippingDetails = ShippingAddress.objects.all()
    total_orders = orders.count()

    orderFilter = OrderFilter(request.GET, queryset=orders)
    orders = orderFilter.qs

    context = {'shippingDetails':shippingDetails, 'customer':customer, 'orders':orders, 'total_orders':total_orders,
    'filter':orderFilter}
    return render(request, 'Axis/AxisCRM/customer.html', context)


def shippingDetails(request):
    action = 'update'
    shippingDetails = ShippingAddress.objects.all()
    form = ShippingDetailsForm(instance=shippingDetails)

    context =  {'action':action, 'form':form}
    return render(request, 'Axis/AxisCRM/order_form.html', context)

#-------------------(CRUD ORDERS) -------------------

def createOrder(request):
    action = 'create'
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context =  {'action':action, 'form':form}
    return render(request, 'Axis/AxisCRM/order_form.html', context)

def updateOrder(request, pk):
    action = 'update'
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/order_details/' + str(order.id))

    context =  {'action':action, 'form':form}
    return render(request, 'Axis/AxisCRM/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        customer_id = order.customer.id
        customer_url = '/customer/' + str(customer_id)
        order.delete()
        return redirect(customer_url)

    return render(request, 'Axis/AxisCRM/delete_item.html', {'item':order})

def viewOrder(request, pk):
    order = Order.objects.get(id=pk)
    # shippingDetails = Order.shippingDetails
    items = order.orderitem_set.all()
    customer = request.user.customer
    cartItems = order.get_cart_items

    form = OrderItemsForm(instance=order)
    if request.method == 'POST':
        form = OrderItemsForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/customer/' + str(order.customer.id))

    shippingDetails = customer.shippingAddress
    print("Shipping Address: ", customer.shippingAddress)


    context =  { 'order':order,  'form':form, 'shippingDetails': shippingDetails, 'items':items, 'cartItems': cartItems}
    return render(request, 'Axis/AxisCRM/order_details.html', context)



#-------------------(CRUD - PRODUCTS) -------------------

def addProduct(request):
    action = 'create'
    name = "Product"
    form = ProductsForm()
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/products/')

    context =  {'action':action, 'form':form, 'name':name }
    return render(request, 'Axis/AxisCRM/order_form.html', context)

def products(request):
    products = Product.objects.all()
    productFilter = ProductFilter(request.GET, queryset=products)
    total_products = products.count()
    products = productFilter.qs

    context = {'total_products': total_products, 'products':products, 'filter': productFilter}

    return render(request, 'Axis/AxisCRM/products.html', context)

def updateProduct(request, pk):
    action = 'update'
    product = Product.objects.get(id=pk)
    name = product.name
    form = ProductsForm(instance=product)

    if request.method == 'POST':
        form = ProductsForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/products/')

    context =  {'action':action, 'form':form, 'name':name }
    return render(request, 'Axis/AxisCRM/order_form.html', context)

def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('/products')

    return render(request, 'Axis/AxisCRM/delete_item.html', {'item':product})


#-------------------(CRUD - CATEGORIES) -------------------

def categories(request):
    categories = Category.objects.all()
    categoryFilter = CategoryFilter(request.GET, queryset=categories)
    total_categories = categories.count()
    categories = categoryFilter.qs

    context = {'total_categories': total_categories, 'categories':categories, 'filter': categoryFilter}

    return render(request, 'Axis/AxisCRM/category.html', context)

def addCategory(request):
    action = 'create'
    name = "Category"
    form = CategoriesForm()
    if request.method == 'POST':
        form = CategoriesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/categories/')

    context =  {'action':action, 'form':form, 'name':name }
    return render(request, 'Axis/AxisCRM/order_form.html', context)

def updateCategory(request, pk):
    action = 'update'
    category = Category.objects.get(id=pk)
    name = category.category_name
    form = CategoriesForm(instance=category)

    if request.method == 'POST':
        form = CategoriesForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('/categories/')

    context =  {'action':action, 'form':form, 'name':name }
    return render(request, 'Axis/AxisCRM/order_form.html', context)

def deleteCategory(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('/categories/')

    return render(request, 'Axis/AxisCRM/delete_item.html', {'item':category})
