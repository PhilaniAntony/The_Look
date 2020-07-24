from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store_view, name="store"),
	path('cart/', views.cart_view, name="cart"),
	path('checkout/', views.checkout_view, name="checkout"),

	path('update_item/', views.updateitem_view, name="updateitem"),
	path('process_order/', views.processorder_view, name="processorder"),

]