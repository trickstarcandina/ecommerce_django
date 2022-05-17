from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings
from .filters import CakeFilter, DrinkFilter, ShippmentFilter

def home_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'ecom/index.html',{'products':products,'product_count_in_cart':product_count_in_cart})


#for showing login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'ecom/customersignup.html',context=mydict)

#-----------for checking user iscustomer
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()



#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,CUSTOMER
def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-home')
    else:
        return redirect('admin-dashboard')

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    # for cards on dashboard
    customercount=models.Customer.objects.all().count()
    cakecount=models.Cake.objects.all().count()
    drinkcount=models.Drink.objects.all().count()
    ordercount=models.Orders.objects.all().count()

    # for recent order tables
    orders=models.Orders.objects.all()
    ordered_cakes=[]
    ordered_drinks=[]
    ordered_bys=[]
    for order in orders:
        if order.cart.cakeitem != None:
           ordered_cake=models.Cake.objects.all().filter(id=order.cart.cakeitem.id)
           ordered_cakes.append(ordered_cake)
           
        if order.cart.drinkitem != None:
           ordered_drink=models.Drink.objects.all().filter(id=order.cart.drinkitem.id)
           ordered_drinks.append(ordered_drink)           
           
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'productcount':cakecount+drinkcount,
    'ordercount':ordercount,
    'data':zip(ordered_cakes,ordered_drinks,ordered_bys,orders),
    }
    return render(request,'ecom/admin_dashboard.html',context=mydict)


# admin view customer table
@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'ecom/view_customer.html',{'customers':customers})

# admin delete customer
@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('view-customer')
    return render(request,'ecom/admin_update_customer.html',context=mydict)

# admin view the product
@login_required(login_url='adminlogin')
def admin_products_view(request):
    products=models.Product.objects.all()
    return render(request,'ecom/admin_products.html',{'products':products})

@login_required(login_url='adminlogin')
def admin_drinks_view(request):
    drinkitem = models.Drinkitem.objects.all()
    context = {'products' : drinkitem}
    return render(request,'ecom/admin_drinks.html', context)

@login_required(login_url='adminlogin')
def admin_cakes_view(request):    
    cakeitem = models.Cakeitem.objects.all()
    context = {'products':cakeitem}
    return render(request,'ecom/admin_cakes.html', context)

# admin add product by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_drink_view(request):
    productForm = forms.DrinkForm()
    if request.method=='POST':
        productForm=forms.DrinkForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-add-drinkitem')
    return render(request,'ecom/admin_add_drinks.html',{'productForm':productForm})


@login_required(login_url='adminlogin')
def admin_add_drinkitem_view(request):
    productForm = forms.DrinkItemForm()
    if request.method=='POST':
        productForm=forms.DrinkItemForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-drinks')
    return render(request,'ecom/admin_add_drinks.html',{'productForm':productForm})


@login_required(login_url='adminlogin')
def admin_add_cake_view(request):
    productForm = forms.CakeForm()
    if request.method=='POST':
        productForm=forms.CakeForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-add-cakeitem')
    return render(request,'ecom/admin_add_cakes.html',{'productForm':productForm})

@login_required(login_url='adminlogin')
def admin_add_cakeitem_view(request):
    productForm = forms.CakeItemForm()
    if request.method=='POST':
        productForm=forms.CakeItemForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-cakes')

    return render(request,'ecom/admin_add_cakeitems.html',{'productForm':productForm})



@login_required(login_url='adminlogin')
def delete_cake_view(request,pk):
    cakeitem =models.Cakeitem.objects.get(id=pk)
    cake = cakeitem.cake
    if request.method == "POST":
        cake.delete()
        return redirect('admin-cakes')

    context = {'item' : cakeitem}
    return render(request, 'ecom/cake_delete.html', context)


@login_required(login_url='adminlogin')
def delete_drink_view(request,pk):
    drinkitem =models.Drinkitem.objects.get(id=pk)
    drink = drinkitem.drink
    if request.method == "POST":
        drink.delete()
        return redirect('admin-drinks')

    context = {'item' : drinkitem}
    return render(request, 'ecom/drink_delete.html', context)


@login_required(login_url='adminlogin')
def update_drink_view(request,pk):
    drinkitem = models.Drinkitem.objects.get(id=pk)
    productItemForm = forms.DrinkItemForm(instance=drinkitem)
    productForm = forms.DrinkForm(instance=drinkitem.drink)
    if request.method=='POST':
        productForm=forms.DrinkForm(request.POST, request.FILES, instance=drinkitem.drink)
        productItemForm = forms.DrinkItemForm(request.POST, request.FILES, instance=drinkitem)
        if productForm.is_valid() and productItemForm.is_valid():
            productForm.save()
            productItemForm.save()
            return redirect('admin-drinks')

    context = {'productForm' : productForm, 'productItemForm' : productItemForm}
    return render(request,'ecom/admin_update_drink.html',context)

@login_required(login_url='adminlogin')
def update_cake_view(request,pk):
    cakeitem = models.Cakeitem.objects.get(id=pk)
    cakeForm = forms.CakeForm(instance= cakeitem.cake)
    cakeItemForm = forms.CakeItemForm(instance= cakeitem)
    if request.method=='POST':
        cakeForm=forms.CakeForm(request.POST, instance=cakeitem.cake)
        cakeitemForm=forms.CakeItemForm(request.POST, request.FILES, instance=cakeitem)
        if cakeForm.is_valid() and cakeitemForm.is_valid():
            cakeForm.save()
            cakeitemForm.save()
            return redirect('admin-cakes')

    context = {'cakeForm' : cakeForm, 'cakeitemForm' : cakeItemForm}
    return render(request,'ecom/admin_update_cake.html',context)


@login_required(login_url='adminlogin')
def admin_view_booking_view(request):
    orders=models.Orders.objects.all()
    ordered_cakes=[]
    ordered_drinks=[]
    ordered_bys=[]
    for order in orders:
        if order.cake != None:
           ordered_cake=models.Cake.objects.all().filter(id=order.cake.id)
           ordered_cakes.append(ordered_cake)
           
        if order.drink != None:
           ordered_drink=models.Drink.objects.all().filter(id=order.drink.id)
           ordered_drinks.append(ordered_drink)           
           
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_bys.append(ordered_by)

    return render(request,'ecom/admin_view_booking.html',{'data':zip(ordered_cakes, ordered_drinks,ordered_bys,orders)})


@login_required(login_url='adminlogin')
def delete_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')

# for changing status of order (pending,delivered...)
@login_required(login_url='adminlogin')
def update_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=order)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request,'ecom/update_order.html',{'orderForm':orderForm})


# admin view the feedback
@login_required(login_url='adminlogin')
def view_feedback_view(request):
    feedbacks=models.Feedback.objects.all().order_by('-id')
    return render(request,'ecom/view_feedback.html',{'feedbacks':feedbacks})



#---------------------------------------------------------------------------------
#------------------------ PUBLIC CUSTOMER RELATED VIEWS START ---------------------
#---------------------------------------------------------------------------------
def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    cakes=models.Cake.objects.all().filter(name__icontains=query)
    if 'cake_ids' in request.COOKIES:
        cake_ids = request.COOKIES['cake_ids']
        counter=cake_ids.split('|')
        cake_count_in_cart=len(set(counter))
    else:
        cake_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'ecom/customer_home_cake.html',{'products':cakes,'word':word,'product_count_in_cart':cake_count_in_cart})
    return render(request,'ecom/index.html',{'products':cakes,'word':word,'product_count_in_cart':cake_count_in_cart})


# any one can add product to cart, no need of signin
def add_to_cart_product_view(request,pkproduct):
    products=models.Product.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=1

    response = render(request, 'ecom/index.html',{'products':products,'product_count_in_cart':product_count_in_cart})

    #adding product id to cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(pkproduct)
        else:
            product_ids=product_ids+"|"+str(pkproduct)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pkproduct)

    product=models.Product.objects.get(id=pkproduct)
    messages.info(request, product.name + ' added to cart successfully!')

    return response

def add_to_cart_cake_view(request,pkcake):
    cakes=models.Cake.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'cake_ids' in request.COOKIES:
        cake_ids = request.COOKIES['cake_ids']
        counter=cake_ids.split('|')
        cake_count_in_cart=len(set(counter))
    else:
        cake_count_in_cart=1

    response = render(request, 'ecom/indexCake.html',{'cakes':cakes,'cake_count_in_cart':cake_count_in_cart})

    #adding product id to cookies
    if 'cake_ids' in request.COOKIES:
        cake_ids = request.COOKIES['cake_ids']
        if cake_ids=="":
            cake_ids=str(pkcake)
        else:
            cake_ids=cake_ids+"|"+str(pkcake)
        response.set_cookie('cake_ids', cake_ids)
    else:
        response.set_cookie('cake_ids', pkcake)

    cake=models.Cake.objects.get(id=pkcake)
    messages.info(request, cake.name + ' added to cart successfully!')

    return response

def add_to_cart_drink_view(request,pkdrink):
    drinks=models.Drink.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'drink_ids' in request.COOKIES:
        drink_ids = request.COOKIES['drink_ids']
        counter=drink_ids.split('|')
        drink_count_in_cart=len(set(counter))
    else:
        drink_count_in_cart=1

    response = render(request, 'ecom/indexDrink.html',{'drinks':drinks,'drink_count_in_cart':drink_count_in_cart})

    #adding product id to cookies
    if 'drink_ids' in request.COOKIES:
        drink_ids = request.COOKIES['drink_ids']
        if drink_ids=="":
            drink_ids=str(pkdrink)
        else:
            drink_ids=drink_ids+"|"+str(pkdrink)
        response.set_cookie('drink_ids', drink_ids)
    else:
        response.set_cookie('drink_ids', pkdrink)

    drink=models.Drink.objects.get(id=pkdrink)
    messages.info(request, drink.name + ' added to cart successfully!')

    return response

# for checkout of cart
def cart_view(request):
        
    #for cart counter: cake    
    if 'cake_ids' in request.COOKIES:
        cake_ids = request.COOKIES['cake_ids']
        counter_cake=cake_ids.split('|')
        cake_count_in_cart=len(set(counter_cake))
    else:
        cake_count_in_cart=0        
       
       
    if 'drink_ids' in request.COOKIES:
        drink_ids = request.COOKIES['drink_ids']
        counter_drink=drink_ids.split('|')
        drink_count_in_cart=len(set(counter_drink))
    else:
        drink_count_in_cart=0          
    # fetching product details from db whose id is present in cookie
    total=0
    cakes=None
    if 'cake_ids' in request.COOKIES:
        cake_ids = request.COOKIES['cake_ids']
        if cake_ids != "":
            cake_id_in_cart=cake_ids.split('|')
            cakes=models.Cakeitem.objects.all().filter(id__in = cake_id_in_cart)
            #for total price shown in cart
            for p in cakes:
                total=total+p.price    
       
    drinks=None
    if 'drink_ids' in request.COOKIES:
        drink_ids = request.COOKIES['drink_ids']
        if drink_ids != "":
            drink_id_in_cart=drink_ids.split('|')
            drinks=models.Drinkitem.objects.all().filter(id__in = drink_id_in_cart)
            #for total price shown in cart
            for p in drinks:
                total=total+p.price      
    amount = drink_count_in_cart + cake_count_in_cart                
    return render(request,'ecom/cart.html',{'cakes':cakes, 'drinks':drinks,'total':total,'product_count_in_cart':amount})


def remove_from_cart_view(request,pk):
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart=product_ids.split('|')
        product_id_in_cart=list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products=models.Product.objects.all().filter(id__in = product_id_in_cart)
        #for total price shown in cart after removing product
        for p in products:
            total=total+p.price

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(product_id_in_cart)):
            if i==0:
                value=value+product_id_in_cart[0]
            else:
                value=value+"|"+product_id_in_cart[i]
        response = render(request, 'ecom/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})
        if value=="":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids',value)
        return response

def remove_cake_from_cart_view(request,pk):
    #for counter in cart
    if 'cake_ids' in request.COOKIES:
        cake_ids = request.COOKIES['cake_ids']
        counter=cake_ids.split('|')
        cake_count_in_cart=len(set(counter))
    else:
        cake_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'cake_ids' in request.COOKIES:
        cake_ids = request.COOKIES['cake_ids']
        cake_id_in_cart=cake_ids.split('|')
        cake_id_in_cart=list(set(cake_id_in_cart))
        cake_id_in_cart.remove(str(pk))
        cakes=models.Cake.objects.all().filter(id__in = cake_id_in_cart)
        #for total price shown in cart after removing product
        for p in cakes:
            total=total+p.price

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(cake_id_in_cart)):
            if i==0:
                value=value+cake_id_in_cart[0]
            else:
                value=value+"|"+cake_id_in_cart[i]
        response = render(request, 'ecom/cart.html',{'cakes':cakes,'total':total,'cake_count_in_cart':cake_count_in_cart})
        if value=="":
            response.delete_cookie('cake_ids')
        response.set_cookie('cake_ids',value)
        return response

def remove_drink_from_cart_view(request,pk):
    #for counter in cart
    if 'drink_ids' in request.COOKIES:
        drink_ids = request.COOKIES['drink_ids']
        counter=drink_ids.split('|')
        drink_count_in_cart=len(set(counter))
    else:
        drink_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'drink_ids' in request.COOKIES:
        drink_ids = request.COOKIES['drink_ids']
        drink_id_in_cart=drink_ids.split('|')
        drink_id_in_cart=list(set(drink_id_in_cart))
        drink_id_in_cart.remove(str(pk))
        drinks=models.Drink.objects.all().filter(id__in = drink_id_in_cart)
        #for total price shown in cart after removing product
        for p in drinks:
            total=total+p.price

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(drink_id_in_cart)):
            if i==0:
                value=value+drink_id_in_cart[0]
            else:
                value=value+"|"+drink_id_in_cart[i]
        response = render(request, 'ecom/cart.html',{'drinks':drinks,'total':total,'drink_count_in_cart':drink_count_in_cart})
        if value=="":
            response.delete_cookie('drink_ids')
        response.set_cookie('drink_ids',value)
        return response

def send_feedback_view(request):
    feedbackForm=forms.FeedbackForm()
    if request.method == 'POST':
        feedbackForm = forms.FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            feedbackForm.save()
            return render(request, 'ecom/feedback_sent.html')
    return render(request, 'ecom/send_feedback.html', {'feedbackForm':feedbackForm})


#---------------------------------------------------------------------------------
#------------------------ CUSTOMER RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_home_view(request):
    cakes=models.Cakeitem.objects.all()
    if 'cake_ids' in request.COOKIES:
        cake_ids = request.COOKIES['cake_ids']
        counter=cake_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'ecom/customer_home_cake.html',{'products':cakes,'product_count_in_cart':product_count_in_cart})

def customer_home_without_login(request):
    cakes=models.Cakeitem.objects.all()
    return render(request,'ecom/customer_home_cake_without_login.html',{'products':cakes})

@login_required(login_url='customerlogin')
def customer_products_view(request):
    products=models.Product.objects.all()
    return render(request,'ecom/customer_home.html',{'products':products})

def customer_drinks_view(request):
    drinks=models.Drinkitem.objects.all()
    return render(request,'ecom/customer_home_drink.html',{'products':drinks})

def customer_cakes_view(request):
    cakes=models.Cakeitem.objects.all()
    return render(request,'ecom/customer_home_cake.html',{'products':cakes})

def customer_drinks_view_without_login(request):
    drinks=models.Drinkitem.objects.all()
    return render(request,'ecom/customer_home_drink_without_login.html',{'products':drinks})

def customer_cakes_view_without_login(request):
    cakes=models.Cakeitem.objects.all()
    return render(request,'ecom/customer_home_cake_without_login.html',{'products':cakes})

# shipment address before placing order
def customer_address_view(request):
    # this is for checking whether product is present in cart or not
    # if there is no product in cart we will not show address form

    cake_in_cart=False
    if 'cake_ids' in request.COOKIES:
        cake_ids = request.COOKIES['cake_ids']
        if cake_ids != "":
            cake_in_cart=True
    #for counter in cart
    if 'cake_ids' in request.COOKIES:
        cake_ids = request.COOKIES['cake_ids']
        counter=cake_ids.split('|')
        cake_count_in_cart=len(set(counter))
    else:
        cake_count_in_cart=0

    drink_in_cart=False
    if 'drink_ids' in request.COOKIES:
        drink_ids = request.COOKIES['drink_ids']
        if drink_ids != "":
            drink_in_cart=True
    #for counter in cart
    if 'drink_ids' in request.COOKIES:
        drink_ids = request.COOKIES['drink_ids']
        counter=drink_ids.split('|')
        drink_count_in_cart=len(set(counter))
    else:
        drink_count_in_cart=0

    addressForm = forms.AddressForm()
    if request.method == 'POST':
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            # here we are taking address, email, mobile at time of order placement
            # we are not taking it from customer account table because
            # these thing can be changes
            mobile=addressForm.cleaned_data['Mobile']
            address = addressForm.cleaned_data['Address']
            nameShip = addressForm.cleaned_data['NameShip']
            price = addressForm.cleaned_data['Price']
            #for showing total price on payment page.....accessing id from cookies then fetching  price of product from db
            total=0

            if 'cake_ids' in request.COOKIES:
                cake_ids = request.COOKIES['cake_ids']
                if cake_ids != "":
                    cake_id_in_cart=cake_ids.split('|')
                    cakes=models.Cakeitem.objects.all().filter(id__in = cake_id_in_cart)
                    for p in cakes:
                        total=total+p.price

            if 'drink_ids' in request.COOKIES:
                drink_ids = request.COOKIES['drink_ids']
                if drink_ids != "":
                    drink_id_in_cart=drink_ids.split('|')
                    drinks=models.Drinkitem.objects.all().filter(id__in = drink_id_in_cart)
                    for p in drinks:
                        total=total+p.price

            response = render(request, 'ecom/payment.html',{'total':total+price}) # tổng tiền = total + price ship
            response.set_cookie('mobile',mobile)
            response.set_cookie('address',address)
            response.set_cookie('nameShip',nameShip)
            response.set_cookie('price',price)
            response.set_cookie('total',total)
            return response
    
    product_in_cart = False    
    if cake_in_cart or drink_in_cart : 
        product_in_cart = True 

    return render(request,'ecom/customer_address.html',{'addressForm':addressForm,'product_in_cart':product_in_cart,'drink_count_in_cart':drink_count_in_cart, 'cake_count_in_cart':cake_count_in_cart})




# here we are just directing to this view...actually we have to check whther payment is successful or not
#then only this view should be accessed
@login_required(login_url='customerlogin')
def payment_success_view(request):
    # Here we will place order | after successful payment
    # we will fetch customer  mobile, address, Email
    # we will fetch product id from cookies then respective details from db
    # then we will create order objects and store in db
    # after that we will delete cookies because after order placed...cart should be empty
    customer=models.Customer.objects.get(user_id=request.user.id)
    cakes=None
    drinks=None
    countCake = 0
    countDrink = 0    
    nameShip=None
    price=None
    total=None
 
    if 'total' in request.COOKIES:
        total=request.COOKIES['total']    
 
    if 'nameShip' in request.COOKIES:
        nameShip=request.COOKIES['nameShip']
    if 'price' in request.COOKIES:
        price=request.COOKIES['price'] 
        shipment = models.Shipment.objects.get_or_create(name = nameShip, price = price) 
        payment = models.Payment.objects.create(totalMoney = total)

          
    if 'cake_ids' in request.COOKIES:
        cake_ids = request.COOKIES['cake_ids']
        if cake_ids != "":
            cake_id_in_cart=cake_ids.split('|')
            cakes=models.Cakeitem.objects.all().filter(id__in = cake_id_in_cart)
            countCake+=1
            
    if 'drink_ids' in request.COOKIES:
        drink_ids = request.COOKIES['drink_ids']
        if drink_ids != "":
            drink_id_in_cart=drink_ids.split('|')
            drinks=models.Drinkitem.objects.all().filter(id__in = drink_id_in_cart)
            countDrink+=1            
    # Here we get products list that will be ordered by one customer at a time
    # these things can be change so accessing at the time of order...


    # dang sai

    if countDrink > 0:
        for drink in drinks:
          cart = models.Cart.objects.get_or_create(drinkitem=drink,totalMoney=drink.price)
          models.Orders.objects.get_or_create(customer = customer,  status = 'Pending' )
    if countCake > 0:
        for cake in cakes:
          cart = models.Cart.objects.get_or_create(cakeitem=cake,totalMoney=cake.price)
          models.Orders.objects.get_or_create(customer = customer, status = 'Pending' )
    
    # after order placed cookies should be deleted
    response = render(request,'ecom/payment_success.html')
    response.delete_cookie('drink_ids')
    response.delete_cookie('cake_ids')
    response.delete_cookie('email')

    return response




@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_order_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    orders=models.Orders.objects.all().filter(customer_id = customer)
    ordered_products=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id) 
        ordered_products.append(ordered_product)

    return render(request,'ecom/my_order.html',{'data':zip(ordered_products,orders)})




#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def download_invoice_view(request,orderID,productID):
    order=models.Orders.objects.get(id=orderID)
    product=models.Product.objects.get(id=productID)
    mydict={
        'orderDate':order.order_date,
        'customerName':request.user,
        'customerEmail':order.email,
        'customerMobile':order.mobile,
        'shipmentAddress':order.address,
        'orderStatus':order.status,

        'productName':product.name,
        'productImage':product.product_image,
        'productPrice':product.price,
        'productDescription':product.description,


    }
    return render_to_pdf('ecom/download_invoice.html',mydict)






@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'ecom/my_profile.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('my-profile')
    return render(request,'ecom/edit_profile.html',context=mydict)



#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START --------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'ecom/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'ecom/contactussuccess.html')
    return render(request, 'ecom/contactus.html', {'form':sub})


#========== SHIPPMENT ============
@login_required(login_url='adminlogin')
def admin_shippment_view(request):    
    shipment = models.Shipment.objects.all()
    shipmentFilter = ShippmentFilter(request.GET, queryset=shipment)
    context = {'shipment' : shipment, 'shipmentFilter' : shipmentFilter}
    return render(request,'ecom/admin_shippment.html', context)

@login_required(login_url='adminlogin')
def admin_add_shipment_view(request):
    shipmentForm = forms.ShipmentForm()
    if request.method=='POST':
        shipmentForm = forms.ShipmentForm(request.POST)
        if shipmentForm.is_valid():
            shipmentForm.save()
        return HttpResponseRedirect('admin-shipment')
    return render(request,'ecom/admin_add_shipment.html',{'shipmentForm' :shipmentForm})

@login_required(login_url='adminlogin')
def admin_delete_shipment_view(request,pk):
    shipment = models.Shipment.objects.get(id=pk)
    if request.method == "POST":
        shipment.delete()
        return redirect('admin-shipment')

    context = {'item' : shipment}
    return render(request, 'ecom/admin_shipment_delete.html', context)


@login_required(login_url='adminlogin')
def admin_update_shipment_view(request,pk):
    shipment = models.Shipment.objects.get(id=pk)
    shipmentForm = forms.ShipmentForm(instance=shipment)
    if request.method=='POST':
        shipmentForm=forms.ShipmentForm(request.POST, instance=shipment)
        if shipmentForm.is_valid():
            shipmentForm.save()
            return redirect('admin-shipment')

    context = {'shipmentForm' : shipmentForm}
    return render(request,'ecom/admin_shipment_update.html',context)
