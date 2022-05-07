"""

Developed By : sumit kumar
facebook : fb.com/sumit.luv
Youtube :youtube.com/lazycoders


"""
from django.contrib import admin
from django.urls import path
from ecom import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='ecom/customerlogin.html'),name='customerlogin'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='ecom/logout.html'),name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view,name='contactus'),
    path('search', views.search_view,name='search'),
    path('send-feedback', views.send_feedback_view,name='send-feedback'),
    path('view-feedback', views.view_feedback_view,name='view-feedback'),

    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='ecom/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('view-customer', views.view_customer_view,name='view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),

    path('admin-products', views.admin_products_view,name='admin-products'),
    path('admin-drinks', views.admin_drinks_view,name='admin-drinks'),
    path('admin-cakes', views.admin_cakes_view,name='admin-cakes'),
    path('admin-shipment', views.admin_shippment_view,name='admin-shipment'),
    path('admin-add-shipment', views.admin_add_shipment_view,name='admin-add-shipment'),
    path('admin-delete-shipment/<int:pk>', views.admin_delete_shipment_view, name='admin-delete-shipment'),
    path('admin-update-shipment/<int:pk>', views.admin_update_shipment_view, name='admin-update-shipment'),
    path('admin-add-drink', views.admin_add_drink_view,name='admin-add-drink'),
    path('admin-add-drinkitem', views.admin_add_drinkitem_view,name='admin-add-drinkitem'),
    path('admin-add-cake', views.admin_add_cake_view,name='admin-add-cake'),
    path('admin-add-cakeitem', views.admin_add_cakeitem_view,name='admin-add-cakeitem'),
    path('delete-cake/<int:pk>', views.delete_cake_view,name='delete-cake'),
    path('delete-drink/<int:pk>', views.delete_drink_view,name='delete-drink'),
    path('update-drink/<int:pk>', views.update_drink_view,name='update-drink'),
    path('update-cake/<int:pk>', views.update_cake_view,name='update-cake'),

    path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', views.update_order_view,name='update-order'),


    path('customersignup', views.customer_signup_view),
    path('customerlogin', LoginView.as_view(template_name='ecom/customerlogin.html'),name='customerlogin'),
    path('customer-products', views.customer_products_view,name='customer-products'),
    path('customer-drinks', views.customer_drinks_view,name='customer-drinks'),
    path('customer-cakes', views.customer_cakes_view,name='customer-cakes'),
    path('customer-home', views.customer_home_view,name='customer-home'),
    path('my-order', views.my_order_view,name='my-order'),
    path('my-profile', views.my_profile_view,name='my-profile'),
    path('edit-profile', views.edit_profile_view,name='edit-profile'),
    path('download-invoice/<int:orderID>/<int:productID>', views.download_invoice_view,name='download-invoice'),


    path('add-to-cart-product/<int:pkproduct>', views.add_to_cart_product_view,name='add-to-cart-product'),
    path('add-to-cart-cake/<int:pkcake>', views.add_to_cart_cake_view,name='add-to-cart-cake'),
    path('add-to-cart-drink/<int:pkdrink>', views.add_to_cart_drink_view,name='add-to-cart-drink'),
    
    
    path('cart', views.cart_view,name='cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),
    path('remove-cake-from-cart/<int:pk>', views.remove_cake_from_cart_view,name='remove-cake-from-cart'),
    path('remove-drink-from-cart/<int:pk>', views.remove_drink_from_cart_view,name='remove-drink-from-cart'),
    path('customer-address', views.customer_address_view,name='customer-address'),
    path('payment-success', views.payment_success_view,name='payment-success'),
    
    


]
