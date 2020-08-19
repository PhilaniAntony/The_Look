from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "store"
urlpatterns = [
	#store urls
	path('',views.store_view   , name="home"),
    path('product/<int:pk>/', views.product_detail_view, name='product'),
	path('cart/', views.cart_view, name="cart"),
	path('checkout/', views.checkout_view, name="checkout"),
 
	path('update_item/', views.updateitem_view, name="updateitem"),
    path('add_wishlist/', views.wishlist_view, name="add_wishlist"),
	path('process_order/', views.processorder_view, name="processorder"),
 
    #Detail Views
    path('brand/<int:pk>/', views.brand_list_view, name='brand'),
    path('category/<int:pk>/', views.category_list_view, name='category'),
    path('collection/<int:pk>/', views.collection_list_view, name='collection'),
    path('tag/<int:pk>/', views.tag_list_view, name='tag'),
    
    #register ex: register/
    path('register/', views.register_view, name= 'register'),
    path('login/', views.login_view, name= 'login'),
    path('logout/', views.login_view, name= 'logout'),
   #Password Reset Views
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name= "store/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name= "store/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name= "store/password_reset_form.html"), name='password_reset_confirm' ),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name= "store/password_reset_done.html"), name='0                                       '),
]