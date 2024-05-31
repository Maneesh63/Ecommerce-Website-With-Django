from django.urls import path
from . import views


urlpatterns=[
   path('',views.home,name='home'),

   path('signup/', views.signup, name='signup'),

   path('login/',views.login,name='login'),

    path('logout/',views.logout,name='logout'),

    path('create_product/',views.create_product,name='create_product'),

    path('forgot_password/',views.forgotpassword,name='forgot_password'),

    path('reset_password/',views.reset_password,name='reset_password'),

    path('edit_product/<int:pk>/',views.edit_product,name='edit_product'),

    path('delete_product/<int:pk>/',views.delete_product,name='delete_product'),

    path('list/',views.list_product,name='list'),

    path('product_detail/<int:pk>/',views.product_detail,name='product_detail'),

    path('dashboard/',views.dashboard,name='dashboard'),

    path('edit_dashboard/',views.edit_dashboard,name='edit_dashboard'),

    path('add_cart/<int:pk>/',views.add_cart,name='add_cart'),

    path('cart',views.list_cart,name='cart'),

    path('remove_cart/<int:pk>/',views.remove_cart,name='remove_cart'),

    path('increase_quantity/<int:pk>/', views.increase_quantity, name='increase_quantity'),
    
    path('decrease_quantity/<int:pk>/', views.decrease_quantity, name='decrease_quantity'),
    
    path('comment/<int:pk>/',views.comment,name='comment'),

    path('address/<int:pk>/',views.address,name='address'),

    path('payment/<int:pk>/',views.initiate_payment,name='payment'),

    path('payment/success/', views.paymenthandler,name='payment_success'),
    
    path('common/',views.common,name='common'),
]

    
    
 

