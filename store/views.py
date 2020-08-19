from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.views.generic import View
from django.http import JsonResponse

import json
import datetime
from .models import *

from .forms import CreateUserForm

from .utils import cookieCart, cartData, guestOrder

#register view
def register_view(request):
    form = CreateUserForm()
    if request.method == 'POST' :
        form = CreateUserForm(request.POST)
        if form.is_valid() :   
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user = user)
            messages.success(request, f'A new account has been created ')   
            return redirect('store')  
    context={
        'form' : form
    }
    return render(request, 'store/register.html', context)

#Login View for customer
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password= password)
        if user is not None :
            login(request, user)
            return redirect('store')
        else:
            messages.info(request,'Username or password incorrect')
    
    context={}
    return render(request, 'store/login.html', context)

#logout View for cautomer
def log_out(request):
    logout(request)
    return redirect('login')

#store home view 
def store_view(request):
    brands = Brand.objects.all().order_by('name')
    categories = Category.objects.all()
    collections = Collection.objects.all().order_by('name')
    tags = Tag.objects.all().order_by('name')
    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    
    products = Product.objects.all().order_by('name')
    context = {'products': products,
               'brands' : brands,
               'categories':categories,
               'collections' : collections,
               'tags' : tags,
               'cartItems': cartItems,
               'shipping' : False,
               }
    return render(request, 'store/store.html', context)

#product detail view
def product_detail_view(request,pk):
    product = Product.objects.get(id=pk)
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    context = {
        'product': product,
        'items' : items,
        'order' : order,
        'cartItems' : cartItems,
    } 
    return render(request,'store/partials/product.html', context)


def cart_view(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']  
    context = {
        'order' : order ,
        'items' : items,
        'cartItems' : cartItems,
        'shipping' : False,
    }
    return render(request, 'store/cart.html', context)



def checkout_view(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']  
    context = {
       'items' : items,
       'order' : order,
       'cartItems' : cartItems,
       'shipping' : False,
    }
    return render(request, 'store/checkout.html', context)

def updateitem_view (request):
    data = json.loads(request.body)
    action = data['action']
    productId = data['productId']
    
    product = Product.objects.get(id=productId)
    customer = request.user.customer
    
    order,created = Order.objects.get_or_create(customer= customer, complete= False)
    orderItem,created = OrderItem.objects.get_or_create(order = order, product = product)
    cartItems = order.get_cart_items
    quantity = orderItem.quantity
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    
    if OrderItem.quantity <=  0 :
        OrderItem.delete()
        
    return JsonResponse('Item was added', safe = False)

def wishlist_view(request):
    data = json.loads(request.body)
    action = data['action']
    productId = data['productId']
    
    product = Product.objects.get(Id=productId)
    customer = requset.user.customer
    
    wishitem, created = Wishlist.objects.get_or_create(customer=customer, product=product)
    wishitem.save()
    return JsonResponse("peoduct added to wishlist", safe=False)
    
    
def processorder_view(request):
    transaction_id = datetime.datetime.now().timestamp()
    
    data = json.loads(request.body)
    
    if request.user.is_authenticated():
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer= customer, complete= False)
       
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    
    if order.shipping == True :
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'] ,
                zipcode = data['shipping']['zipcode']
            )
    return JsonResponse('Payment was completed...', safe = False)



def brand_list_view(request,pk):
    brands = Brand.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')
    collections = Collection.objects.all().order_by('name')
    tags = Tag.objects.all().order_by('name')
    
    brand = Brand.objects.get(id=pk)
    products = Product.objects.all().filter(brand=brand)
    #products = brand.product_set.all() 
    print(brand, products )
    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    
    context = {
        'products': products,
        'items' : items,
        'order' : order,
        'cartItems' : cartItems,
        'brands' : brands,
        'categories':categories,
        'collections' : collections,
        'tags' : tags,
    }  
    return render(request,'store/partials/brand.html', context)
    
def category_list_view (request,pk):
    brands = Brand.objects.all().order_by('name')
    categories = Category.objects.all()
    collections = Collection.objects.all().order_by('name')
    tags = Tag.objects.all().order_by('name')
    
    category = Category.objects.get(id=pk) 
    products = Product.objects.all()
    category_products = Product.objects.all().filter(category=category.id)
        
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    
    context = {
        'products': category_products,
        'items' : items,
        'order' : order,
        'cartItems' : cartItems,
        'brands' : brands,
        'categories':categories,
        'collections' : collections,
        'tags' : tags,
    } 
    return render(request,'store/partials/category.html', context) 
   
    
    
def collection_list_view(request,pk):
    brands = Brand.objects.all().order_by('name')
    categories = Category.objects.all()
    collections = Collection.objects.all().order_by('name')
    tags = Tag.objects.all().order_by('name')
    
    collection = Collection.objects.get(id=pk) 
    products = Product.objects.all().filter(collection=collection.id)
    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    
    context = {
        'products': products,
        'items' : items,
        'order' : order,
        'cartItems' : cartItems,
        'brands' : brands,
        'categories':categories,
        'collections' : collections,
        'tags' : tags,
    } 
    return render(request,'store/partials/collection.html',context) 

def tag_list_view (request,pk):
    brands = Brand.objects.all().order_by('name')
    categories = Category.objects.all()
    collections = Collection.objects.all().order_by('name')
    tags = Tag.objects.all().order_by('name')
    
    tag = tags.get(id=pk) 
    products = Product.objects.all().filter(tags=tag)
    print(tags,products)

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    
    context = {
        'products': products,
        'items' : items,
        'order' : order,
        'cartItems' : cartItems,
        'brands' : brands,
        'categories':categories,
        'collections' : collections,
        'tags' : tags,
    } 
    return render(request,'store/partials/tags.html', context) 


    