from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm

from django.conf import settings

from .models import *
from .forms import *
from .utils import cookieCart, cartData, guestOrder
from .filters import *

# Create your views here.
def about(request):

    return render(request, 'Collective/about.html', {})


def store(request, category_slug=None):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    category = None
    products = CollectiveProduct.objects.all()
    categorylist = CollectiveCategory.objects.annotate(total_products=Count('collectiveproduct'))
    context = {'cartItems': cartItems, 'products':products , 'category_list' : categorylist ,'category' : category , 'shipping': False}

    return render(request, 'Collective/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'cartItems': cartItems, 'items': items , 'order': order}

    return render(request, 'Collective/cart.html', context)



def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'cartItems': cartItems , 'items': items, 'order': order}
    return render(request, 'Collective/checkout.html', context)

def contact(request):
    if request.method == 'POST':
        message = request.POST['message']
        if request.user.is_authenticated:
            name = request.user.username
            email = request.user.email
            message = name + "\n" + email + "\n"+ message
            send_mail('Contact Form', message, settings.EMAIL_HOST_USER, ['django10.foxx@gmail.com', 'mcn10.foxx@gmail.com'], fail_silently="false" )
            messages.success(request, ("Your message has been sent successfully..."))
        else:
            name = request.POST['name']
            email = request.POST['email']
            message = name + "\n" + email + "\n"+ message
            send_mail('Contact Form', message, settings.EMAIL_HOST_USER, ['django10.foxx@gmail.com', 'mcn10.foxx@gmail.com'], fail_silently="false" )
            messages.success(request, ("Your message has been sent successfully..."))
        return redirect('Collective:store')

    return render(request, 'Collective/contact.html', {})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.collectivecustomer
    product = CollectiveProduct.objects.get(id=productId)
    order, created = CollectiveOrder.objects.get_or_create(customer=customer, status="Pending")

    orderItem, created = CollectiveOrderItem.objects.get_or_create(order=order, product=product)

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

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = ColletiveOrder.objects.get_or_create(customer=customer, status="Pending")
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        print("Order total is correct")
        order.status = "Payment Confirmed, Processing Order"
        order.save()

    else:
        print("Order total is incorrect")

    if order.shipping == True:
        CollectiveShippingAddress.objects.create(
        customer=customer,
        order=order,
        country=data['shipping']['country'],
        address1=data['shipping']['address1'],
        address2=data['shipping']['address2'],
        city=data['shipping']['city'],
        province=data['shipping']['province'],
        postal_code=data['shipping']['postal_code'],
        )

        # Add code to send email to Store Owner
    return JsonResponse('Payment Complete', safe=False)


#-------------------(DETAIL/LIST VIEWS) -------------------

def dashboard(request):
    orders = CollectiveOrder.objects.all().order_by('-status')[0:5]
    customers = CollectiveCustomer.objects.all()

    total_customers = customers.count()

    total_orders = CollectiveOrder.objects.all().count()
    delivered = CollectiveOrder.objects.filter(status='Delivered').count()
    pending = CollectiveOrder.objects.filter(status='Pending').count()



    context = {'customers':customers, 'orders':orders,
    'total_customers':total_customers,'total_orders':total_orders, 
    'delivered':delivered, 'pending':pending}
    return render(request, 'Collective/CollectiveCRM/dashboard.html', context)


def customer(request, pk):
    customer = CollectiveCustomer.objects.get(id=pk)
    orders = customer.order_set.all()
    shippingDetails = CollectiveShippingAddress.objects.all()
    total_orders = orders.count()

    orderFilter = CollectiveOrderFilter(request.GET, queryset=orders) 
    orders = orderFilter.qs

    context = {'shippingDetails':shippingDetails, 'customer':customer, 'orders':orders, 'total_orders':total_orders,
    'filter':orderFilter}
    return render(request, 'Collective/CollectiveCRM/customer.html', context)


def shippingDetails(request):
    action = 'update'
    shippingDetails = CollectiveShippingAddress.objects.all()
    form = CollectiveShippingDetailsForm(instance=shippingDetails)

    context =  {'action':action, 'form':form}
    return render(request, 'Collective/CollectiveCRM/order_form.html', context)

#-------------------(CRUD ORDERS) -------------------

def createOrder(request):
    action = 'create'
    form = CollectiveOrderForm()
    if request.method == 'POST':
        form = CollectiveOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/TheCollective')

    context =  {'action':action, 'form':form}
    return render(request, 'Collective/CollectiveCRM/order_form.html', context)

def updateOrder(request, pk):
    action = 'update'
    order = CollectiveOrder.objects.get(id=pk)
    form = CollectiveOrderForm(instance=order)

    if request.method == 'POST':
        form = CollectiveOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/TheCollective/order_details/' + str(order.id))

    context =  {'action':action, 'form':form}
    return render(request, 'Collective/CollectiveCRM/order_form.html', context)

def deleteOrder(request, pk):
    order = CollectiveOrder.objects.get(id=pk)
    if request.method == 'POST':
        customer_id = order.customer.id
        customer_url = '/TheCollective/customer/' + str(customer_id)
        order.delete()
        return redirect(customer_url)
        
    return render(request, 'Collective/CollectiveCRM/delete_item.html', {'item':order})

def viewOrder(request, pk):
    order = CollectiveOrder.objects.get(id=pk) 
    # shippingDetails = Order.shippingDetails
    items = order.orderitem_set.all()

    cartItems = order.get_cart_items

    form = CollectiveOrderItemsForm(instance=order)
    if request.method == 'POST':
        form = CollectiveOrderItemsForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/TheCollective/customer/' + str(order.customer.id))

    context =  { 'order':order,  'form':form, 'shippingDetails': shippingDetails, 'items':items, 'cartItems': cartItems}
    return render(request, 'Collective/CollectiveCRM/order_details.html', context)


#-------------------(CRUD - PRODUCTS) -------------------

def addProduct(request):
    action = 'create'
    name = "Product"
    form = CollectiveProductsForm()
    if request.method == 'POST':
        form = CollectiveProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/TheCollective/products/')

    context =  {'action':action, 'form':form, 'name':name }
    return render(request, 'Collective/CollectiveCRM/order_form.html', context)

def products(request):
    products = CollectiveProduct.objects.all()
    productFilter = CollectiveProductFilter(request.GET, queryset=products) 
    total_products = products.count()
    products = productFilter.qs

    context = {'total_products': total_products, 'products':products, 'filter': productFilter}

    return render(request, 'Collective/CollectiveCRM/products.html', context)

def updateProduct(request, pk):
    action = 'update'
    product = CollectiveProduct.objects.get(id=pk)
    name = product.name
    form = CollectiveProductsForm(instance=product)

    if request.method == 'POST':
        form = CollectiveProductsForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/TheCollective/products/')

    context =  {'action':action, 'form':form, 'name':name }
    return render(request, 'Collective/CollectiveCRM/order_form.html', context)

def deleteProduct(request, pk):
    product = CollectiveProduct.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('/TheCollective/products')
        
    return render(request, 'Collective/CollectiveCRM/delete_item.html', {'item':product})



#-------------------(CRUD - CATEGORIES) -------------------

def categories(request):
    categories = CollectiveCategory.objects.all()
    categoryFilter = CollectiveCategoryFilter(request.GET, queryset=categories) 
    total_categories = categories.count()
    categories = categoryFilter.qs

    context = {'total_categories': total_categories, 'categories':categories, 'filter': categoryFilter}

    return render(request, 'Collective/CollectiveCRM/category.html', context)

def addCategory(request):
    action = 'create'
    name = "Category"
    form = CollectiveCategoriesForm()
    if request.method == 'POST':
        form = CollectiveCategoriesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/TheCollective/categories/')

    context =  {'action':action, 'form':form, 'name':name }
    return render(request, 'Collective/CollectiveCRM/order_form.html', context)

def updateCategory(request, pk):
    action = 'update'
    category = CollectiveCategory.objects.get(id=pk)
    name = category.category_name
    form = CollectiveCategoriesForm(instance=category)

    if request.method == 'POST':
        form = CollectiveCategoriesForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('/TheCollective/categories/')

    context =  {'action':action, 'form':form, 'name':name }
    return render(request, 'Collective/CollectiveCRM/order_form.html', context)

def deleteCategory(request, pk):
    category = CollectiveCategory.objects.get(id=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('/TheCollective/categories/')
        
    return render(request, 'Collective/CollectiveCRM/delete_item.html', {'item':category})
