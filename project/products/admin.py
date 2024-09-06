from django.contrib import admin
from .models import CustomUser,Product,Cart,Comment,Address,Order,OrderItem,Categories


admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Comment)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Categories)
