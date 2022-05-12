from django.contrib import admin
from .models import Customer,Orders,Feedback,Cake,Drink,Cakeitem,Drinkitem,Cart,Shipment,Paypal,Payment,Comment
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)

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

class CakeitemAdmin(admin.ModelAdmin):
    pass
admin.site.register(Cakeitem, CakeitemAdmin)

class DrinkitemAdmin(admin.ModelAdmin):
    pass
admin.site.register(Drinkitem, DrinkitemAdmin)

class CartAdmin(admin.ModelAdmin):
    pass
admin.site.register(Cart, CartAdmin)

class ShipmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Shipment, ShipmentAdmin)

class PaymentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Payment, PaymentAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentAdmin)

class PaypalAdmin(admin.ModelAdmin):
    pass
admin.site.register(Paypal, PaypalAdmin)
# Register your models here.
