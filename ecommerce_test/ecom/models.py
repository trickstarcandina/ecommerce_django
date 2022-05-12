from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name



class Cake(models.Model):
    name=models.CharField(max_length=40)
    TYPE =(
        ('Bánh sinh nhật','Bánh sinh nhật'),
        ('Bánh mặn','Bánh mặn'),
        ('Bánh ngọt','Bánh ngọ'),
    )
    type = models.CharField(max_length=200, null = True, choices = TYPE)
    expiry = models.CharField(max_length=40, null = True)
    def __str__(self):
        return self.name

class Cakeitem(models.Model):
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    cake = models.ForeignKey('Cake', on_delete=models.CASCADE,null=True)
    discount=models.PositiveIntegerField()
    price=models.FloatField()
    description=models.CharField(max_length=40)

class Drink(models.Model):
    name=models.CharField(max_length=40)
    description=models.CharField(max_length=40)
    SIZE =(
        ('L','L'),
        ('M','M'),
        ('XL','XL'),
    )
    size = models.CharField(max_length=200, null = True, choices = SIZE)
    TYPE =(
        ('Giải khát','Giải khát'),
        ('Nước ngọt','Nước ngọt'),
        ('Trà sữa','Trà sữa'),
    )
    type = models.CharField(max_length=200, null = True, choices = TYPE)    
    expiry = models.CharField(max_length=40, null = True)
    def __str__(self):
        return self.name

class Drinkitem(models.Model):
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    drink = models.ForeignKey('Drink', on_delete=models.CASCADE,null=True)    
    discount=models.PositiveIntegerField()
    price=models.FloatField()
    description=models.CharField(max_length=40)    

class Cart(models.Model):
    cakeitem=models.ForeignKey('Cakeitem',on_delete=models.CASCADE,null=True)
    drinkitem=models.ForeignKey('Drinkitem',on_delete=models.CASCADE,null=True)
    dateCreated= models.DateField(auto_now_add=True,null=True)
    totalMoney=models.FloatField(null=True)

class Paypal(models.Model):
    idPaypal = models.PositiveIntegerField()
    datePay = models.DateField(auto_now_add=True,null=True)

class Shipment(models.Model):
    name = models.CharField(max_length=40)
    price = models.FloatField()
    
class Payment(models.Model):
    totalMoney = models.FloatField()
    paypal = models.ForeignKey('Paypal',on_delete=models.CASCADE,null=True)
    shipment = models.ForeignKey('Shipment',on_delete=models.CASCADE,null=True)


class Orders(models.Model):
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    cart=models.ForeignKey('Cart', on_delete=models.CASCADE,null=True)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE,null=True)
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )    
    status=models.CharField(max_length=50,null=True,choices=STATUS)
    dateCreated= models.DateField(auto_now_add=True,null=True)


class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name

    
class Comment(models.Model):
    content = models.CharField(max_length=500)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    cakeitem=models.ForeignKey('Cakeitem',on_delete=models.CASCADE,null=True)
    drinkitem=models.ForeignKey('Drinkitem',on_delete=models.CASCADE,null=True)
  
# tao form    
class Product(models.Model):
    name=models.CharField(max_length=40)
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description=models.CharField(max_length=40)
    def __str__(self):
        return self.name