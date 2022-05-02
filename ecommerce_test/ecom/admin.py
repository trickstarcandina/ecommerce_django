from django.contrib import admin
from .models import Customer,Orders,Feedback,Cake,Drink,Cakeitem,Drinkitem,Cart,Shipment,Paypal,Payment,Comment
# Register your models here.
'''
Ai làm mà thấy bị bug thì dùng phần khai báo ở trên này, 
t khai báo trang admin như ở dưới cho nó đơn giản hơn

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
admin.site.register(Cakeitem, CakeAdmin)
class DrinkitemAdmin(admin.ModelAdmin):
    pass
admin.site.register(Drinkitem, CakeAdmin)
class CartAdmin(admin.ModelAdmin):
    pass
admin.site.register(Cart, CakeAdmin)
class ShipmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Shipment, CakeAdmin)

class PaymentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Paypal, CakeAdmin)
class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, CakeAdmin)
'''
# Register your models here.
admin.site.register(Customer)
admin.site.register(Cake)
admin.site.register(Cakeitem)
admin.site.register(Drink)
admin.site.register(Drinkitem)
admin.site.register(Cart)
admin.site.register(Paypal)
admin.site.register(Shipment)
admin.site.register(Payment)
admin.site.register(Orders)
admin.site.register(Feedback)
admin.site.register(Comment)