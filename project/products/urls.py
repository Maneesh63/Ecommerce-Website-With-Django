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
   
   #here im providing multiple url to same function
   #url 1 for listing products
    path('list/',views.list_product, name='list'),

#url 2 for category wise listing
    #path('list/category/<int:pk>/',views.list_product,name='category_products'),

    path('product_detail/<int:pk>/',views.product_detail,name='product_detail'),

    path('dashboard/',views.dashboard,name='dashboard'),

    path('edit_dashboard/',views.edit_dashboard,name='edit_dashboard'),

    path('add_cart/<int:pk>/',views.add_cart,name='add_cart'),

    path('cart',views.list_cart,name='cart'),

    path('remove_cart/<int:pk>/',views.remove_cart,name='remove_cart'),

    path('increase_quantity/<int:pk>/', views.increase_quantity, name='increase_quantity'),
    
    path('decrease_quantity/<int:pk>/', views.decrease_quantity, name='decrease_quantity'),
    
    path('comment/<int:pk>/',views.comment,name='comment'),

    path('address/',views.address,name='address'),

    #path('order_details/',views.order_details,name='order_details'),

    path('payment/<int:pk>/',views.initiate_payment,name='payment'),

    path('payment/success/', views.paymenthandler,name='payment_success'),
    
    #path('common/',views.common,name='common'),

     path('create_order/', views.create_order, name='create_order'),

     path('create_category/',views.create_category,name='create_category'),

     path('category',views.list_category,name='category'),

     path('delete_category/<int:pk>',views.delete_category,name='delete_category'),

      path('categories/<int:pk>/products/',views.list_product_by_category, name='list_products_by_category'),
        
     #path('redirect_to_address/', views.redirect_to_address, name='redirect_to_address'),
      
      path('order_detail/<int:pk>/', views.order_detail, name='order_detail'),
    
     path('order_history/', views.order_history, name='order_history'),
]

    
    
 

