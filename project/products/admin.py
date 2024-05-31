from django.contrib import admin
from .models import CustomUser,Product,Cart,Comment


admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Comment)

