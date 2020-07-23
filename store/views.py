from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json


def store_view(request):
    if request.user.is_authenticated :
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer= customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitems =order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products,
               'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart_view(request):
    if request.user.is_authenticated :
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer= customer, complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
        
    context = {
        'order' : order ,
        'items' : items,
        'cartItems' : cartItems
    }
    return render(request, 'store/cart.html', context)



def checkout_view(request):
    if request.user.is_authenticated :
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer= customer, complete= False)
        cartItems = order.get_cart_items
        items = order.orderitem_set.all()
        
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    
      
    context = {
       'items' : items,
       'order' : order,
       'cartItems' : cartItems,
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
    
    if OrderItem.quantity <= 0 :
        OrderItem.delete()
        
    return JsonResponse('Item was added', safe = False)