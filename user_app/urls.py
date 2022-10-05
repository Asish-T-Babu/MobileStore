from django.contrib import admin
from user_app import views
from django.urls import path,include

urlpatterns = [
    path('', views.index,name="index"),
    path('login/', views.login, name="login"),
    path('login_otp/', views.login_otp, name="otp"),
    path('login_home/',views.login_home,name="login_home"),
    path('home/', views.home, name="home"),
    path('insert/', views.insert, name="insert"),
    path('products',views.products, name='product'), 
    path('product_details/<int:id>',views.product_details, name='product_details'), 
    path('logout/', views.logout, name="logout"),
    path('view_cart/',views.view_cart, name='view_cart'),
    path('add_quantity/<int:id>',views.add_quantity, name='add_quantity'), 
    path('sub_quantity/<int:id>',views.sub_quantity, name='sub_quantity'), 
    path('delete_from_cart/<int:id>',views.delete_from_cart, name='delete_from_cart'),
    path('checkout/',views.checkout,name="checkout"),
    path('add_address/',views.add_address,name="add_address"),
    path('view_wishlist/',views.view_wishlist, name='view_wishlist'),
    path('delete_from_wishlist/<int:id>',views.delete_from_wishlist, name='delete_from_wishlist'),
    path('my_profile/',views.my_profile, name='my_profile'),
    path('address_management/',views.address_management, name='address_management'),
    path('delete_address/<int:id>',views.delete_address, name='delete_address'),
    path('edit_profile/<int:id>',views.edit_profile, name='edit_profile'),
    path('user_order_management/',views.user_order_management, name='user_order_management'),
    path('user_cancel_order/<int:id>',views.user_cancel_order, name='user_cancel_order'), 
    path('download/<int:productID>',views.download, name='download'), 
    path('user_order_detailed_view/<int:id>',views.user_order_detailed_view, name='user_order_detailed_view'),
    path('payment_methods/<int:order_total>',views.payment_methods, name='payment_methods'), 
    path('payment_confirm/<int:order_total>',views.payment_confirm, name='payment_confirm'), 
    path('payment_complete/', views.payment_complete, name="payment_complete"),
    path('payment_methods_razorpay/<int:id>',views.payment_methods_razorpay, name='payment_methods'),
    path('filter_product/<int:id>',views.filter_product, name='filter_product'), 
    path('apply_coupan/',views.apply_coupan, name='apply_coupan'),
    path('razor_pay/<int:id>', views.razor_pay, name="razor_pay"),
    path('user_order_returned/<id>',views.user_order_returned,name='user_order_returned'),
]