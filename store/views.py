from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json


def store_view(request):
    if request.user.is_authenticated :
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer= customer, complete= False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        item = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitems =order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products,
               'cartitems': cartitems}
    return render(request, 'store/store.html', context)


def cart_view(request):
    if request.user.is_authenticated :
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer= customer, complete= False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        item = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {
        'items' : items,
        'order' : order ,
        'cartitems' : cartitems
    }
    return render(request, 'store/cart.html', context)



def checkout_view(request):
    if request.user.is_authenticated :
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer= customer, complete= False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        item = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {
        'items' : items,
        'order' : order ,
    }
    return render(request, 'store/checkout.html', context)

def updateitem_view (request):
    data = json.loads(request.data)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(order= order, complete= False)
    cartitems = order.get_cart_items
    
    if action == 'add' :
        cartitems =  cartitems + 1
    elif action == 'remove':
       cartitems =  cartitems - 1
    OrderItem.save()
    
    if OrderItem.quantity <= 0 :
        OrderItem.delete()
        
    return JsonResponse('Item was added', safe = False)