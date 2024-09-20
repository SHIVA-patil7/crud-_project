from django.urls import path
from chart import views
from django.views.generic import TemplateView 
from django.contrib.auth import views as auth_views
from .views import card_payment_view, payment_complete_view






urlpatterns = [
    path('sign_up/',views.regform,name='regform'),
    #path('verify/',views.Signin_verification,name='Signin_verification'),
    path('login/',views.loginform,name='login'),
    path('send_otp',views.send_otp,name='send_otp'),
    path('otp_verification/',views.otp_verification,name='otp_verification'),
    path('success/',TemplateView.as_view(template_name='seccess.html'),name="success"),
    path('forgetpassword/',TemplateView.as_view(template_name='forgotpassword.html'),name='verifypassword'),
    path('verifyemail/',views.verify_email,name='verify_email'),
    path('confirmemail/',views.confirm,name='conform'),
    path('otp_verification1/',views.otp_verification1,name='otp_verification1'),
    path('passwordchange/',TemplateView.as_view(template_name='password_reset_email.html'),name='passwordchange'),
    path('resetpassword/',views.resetpassowrd,name='resetpassword'),
    path('send_otp1',views.send_otp1,name='send_otp1'),
    path('set_password/',views.setpassowrd,name='setpassword'),
    path('logout/',views.logoutform,name='logout'),
    path('changepassword',views.ChangePasswordView.as_view(),name='changepassword'),
    path('',views.homepage,name='homepage'),
    path('AddProduct/',views.Add_Product,name='Add_Product'),
    path('add_to_cart/<pk>',views.Add_To_Cart,name='Add_To_Cart'),
    path('product_Desc/<pk>',views.Product_desc,name='Product_desc'),
    path('orderlist/',views.orderlist,name='orderlist'),
    path('add_item/<int:pk>',views.Add_Item,name='Add_Item'),
    path('remove_item/<int:pk>',views.Remove_item,name='Remove_Item'),
    path('checkout_page/',views.Checkout_page,name='Checkout_page'),
     path('payment/', card_payment_view, name='card_payment'),
    path('payment_complete/', payment_complete_view, name='payment_complete'),
   
    
 
    

]
