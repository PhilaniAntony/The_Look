from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .models import *
from django.views.decorators.csrf import  csrf_exempt
from .utils import cookieCart, cartData, guestOrder

def store_view(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    
    products = Product.objects.all()
    context = {'products': products,
               'cartItems': cartItems,
               'shipping' : False,
               }
    return render(request, 'store/store.html', context)


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


@csrf_exempt
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


@csrf_exempt
def processorder_view(request):
    transaction_id = datetime.now.timestamp()
    
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
    return JsonResponse('Payment was completed', safe = False)