from django.contrib import admin
from .models import Customer,Product,Orders,Feedback,Cake,Drink
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Orders, OrderAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    pass
admin.site.register(Feedback, FeedbackAdmin)

class CakeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Cake, CakeAdmin)

class DrinkAdmin(admin.ModelAdmin):
    pass
admin.site.register(Drink, DrinkAdmin)
# Register your models here.
