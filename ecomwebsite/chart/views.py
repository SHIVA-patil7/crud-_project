from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages 
from django.contrib.auth.models import User
from .models import *
import random 
from .forms import Userregisterform
from django.core.mail import send_mail 
from django.contrib.auth.hashers import make_password 
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm,PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import *
from django.utils import timezone 
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import CardForm

def regform(request):
    print("hi")
    if request.method=='POST':
        fm=Userregisterform(request.POST)
        if fm.is_valid():
           
            username=request.POST['username']
            email=request.POST['email']
            password1=request.POST['password1']
            password2=request.POST['password2']
            phone_fields=request.POST['phone_fields']
            request.session['username']=username 
            request.session['password1']=password1 
            request.session['email']=email 
            request.session['phone_fields']=phone_fields
            #print(request.session['email'])
            if password1==password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request,'User already exists')
                    return redirect('regform')
                elif User.objects.filter(email=email).exists():
                   messages.info(request,'User email ID already exists')
                   return redirect('regform')
                else:
                     user=User.objects.create_user(username=username,email=email,password=password1)
                     user.save()
                     data=Customer(user=user,phone_fields=phone_fields)
                     data.save()
                     user_name=authenticate(username=username,password=password1)
                     email_subject="Activate your account"
                     message=render_to_string('activate.html',{
                         'user':user,
                         'domain':'127.0.0.1:8000',
                         'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                         'token':generate_token.make_token(user)
                     })
                     if user_name is not None:
                        return redirect('login')
                
            else:
                messages.info(request,'password mismatch')
                return redirect('regform')
    
    else:
        fm=Userregisterform() 
    return render(request,'register.html',{'form':fm})

    


def loginform(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print(form)
        username=request.POST['username']
        request.session['username']=username
        if form.is_valid():
            print('h1')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username)
            print(password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('send_otp')  # Redirect to a success page
            messages.info(request,'Invalid login')
                
        else:
            messages.info(request,'Form is invalid')
            
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logoutform(request):
    logout(request)
    return redirect('homepage')

def send_otp(request):
    user = request.user.email
    otp=''
    for x in range(0,4):
        otp+=str(random.randint(0,9))
    request.session['otp']=otp
    email_subject = 'Your OTP for Login'
    email_body = f'Your OTP for login is {otp}'
    from_email = 'svjoshi885@gmail.com' 
    # recipient_list = [request.session.get('email')]+-
    recipient_list = [user]
    print(recipient_list)

    send_mail(
        email_subject,
        email_body,  
        from_email,
        recipient_list,
        fail_silently=False
    )
    return render(request,'otp.html')


def otp_verification(request):
    if request.method=='POST':
        otp_=request.POST.get('otp')
        if otp_==request.session['otp']:
            messages.info(request,'otp verified successfully')
            return redirect('homepage')
        else:
            messages.info(request,'otp does not match')
            return render(request,'otp.html')


def send_otp1(request):
    print(f"Email stored in session: {request.session.get('email')}") 

    # request.session["email"] = user
    #print(request.session.get('email'),"in email otp")
    #print(user,"user in otp")
    otp=''
    for x in range(0,4):
        otp+=str(random.randint(0,9))
    request.session['otp']=otp
    print( request.session['otp'])

    email_subject = 'Your OTP for Login'
    email_body = f'Your OTP for login is {otp}'
    from_email = 'svjoshi885@gmail.com' 
    recipient_list = [request.session.get('email')]
    #recipient_list = [user]
    print(recipient_list)

    send_mail(
        email_subject,
        email_body,  
        from_email,
        recipient_list,
        fail_silently=False
    )
    return render(request,'otp1.html')

def otp_verification1(request):
    if request.method=='POST':
        otp_=request.POST.get('otp')
        if otp_==request.session['otp']:
            messages.info(request,'otp verified')
            return redirect('setpassword')
    else:
        messages.info(request,'otp does not match')
        return render(request,'otp1.html')


 

def verify_email(request):
    if request.method == 'POST':
        # Fetch email from POST data
        email=request.POST.get('email')
        request.session['email']=email
        
        print(f"Submitted email: {email}")
        user=User.objects.get(email=email)
        print(user,"user !!!!")
        if user:
            print('otp redirect page')
            messages.info(request, 'Email verified')
            return redirect('send_otp1')  # Redirect to a success page
        else:
            messages.info(request, 'Email does not match')
            return redirect('resetpassword')  # Show the verification page again
    else:
    # If it's not a POST request, redirect to the verification page
        return redirect('resetpassword')

def confirm(request):
    return render(request,'confirm.html') 

def resetpassowrd(request):
    print("in here ")
    print(request.method)
    if request.method=='POST':
        fm = PasswordResetForm(request.POST)
        if fm.is_valid():
                fm.save(
                    request=request,
                    use_https=request.is_secure(),
                    email_template_name='password_reset_email.html'
                )
               
                
                messages.success(request, 'Password reset link sent to your email.')
        else:
            
             return redirect('passwordchange')
            
              
    else:
        print(12344)
        fm=PasswordResetForm()
    return render(request,'password_reset_email.html',{'form':fm})



def setpassowrd(request): 
    if request.method == 'POST':
        print('h1')
        username=request.session.get('username')
        # Ensure the user is logged in (request.user should not be AnonymousUser)
        user=User.objects.get(username=username)
        if user:
            fm = SetPasswordForm(user=request.user, data=request.POST)
            print(request.user)
            
            if fm.is_valid():
                fm.save()
                print('h2')
                return redirect('login')  # Redirect to the login page after password change
            else:
                print('Form is invalid')    
        else:
            print('User is not authenticated')
            return redirect('login')  # Redirect anonymous user to login
    
    else:
        if user:
            fm = SetPasswordForm(user=request.user)
        else:
            return redirect('login')  # Redirect anonymous user to login
    
    return render(request, 'setpassword.html', {'form': fm})


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')
    template_name = 'change_password.html'



def homepage(request):
    products=Product.objects.all()
    print(products)
    return render(request,'home.html',{'products':products})



def Add_Product(request):
    if request.method=='POST':
        print(request.method)
        print(request.FILES)
        fm=ProductForm(request.POST,request.FILES)
        if fm.is_valid():
            fm.save()
            messages.info(request,'Product added successfully')
            return redirect("homepage")
        else:
            messages.info(request,'Product has not added successfully')
            
         
    else:
         fm=ProductForm()
    return render(request,'add_product.html',{'form':fm})




def Product_desc(request,pk):
    product=Product.objects.get(pk=pk)
    print(product.img)
    return render(request,'Product_desc.html',{'product':product})






def Add_To_Cart(request,pk):
    product=Product.objects.get(pk=pk)


    order_item,created= Order_Item.objects.get_or_create(
        product=product,
        user=request.user,
        Ordered=False)
    order_qs=Order.objects.filter(user=request.user,Ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(product__pk = pk):
            order_item.quantity+=1
            order_item.save()
            messages.info(request,"Added quantity items")
            return redirect('Product_desc',pk=pk)
            
    else:
        Ordered_date= timezone.now()
        order=Order.objects.create(user=request.user, Ordered_date= Ordered_date)
        order.items.add(order_item)
        messages.info(request,"item added to cart ")
        return redirect('Product_desc',pk=pk)
    
def orderlist(request):
    if Order.objects.filter(user=request.user,Ordered=False).exists():
        order=Order.objects.get(user=request.user,Ordered=False)
        return render(request,'orderlist.html',{'order':order})
    return render(request,'orderlist.html',{'message':"Your cart is empty"})



def Add_Item(request,pk):
    product=Product.objects.get(pk=pk)


    order_item,created= Order_Item.objects.get_or_create(
        product=product,
        user=request.user,
        Ordered=False)
    order_qs=Order.objects.filter(user=request.user,Ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(product__pk = pk):
            if order_item.quantity < product.product_available_count:
                order_item.quantity+=1
                order_item.save()
                messages.info(request,"Added quantity items")
                return redirect('orderlist')
            else:
                messages.info("Sorry!! the product is out of stock")
                return redirect('orderlist')
        else :
            order.items.add(order_item)
            messages.info(request,"item added to cart ")
            return redirect('Product_desc',pk=pk)
    else:
        Ordered_date= timezone.now()
        order=Order.objects.create(user=request.user, Ordered_date= Ordered_date)
        order.items.add(order_item)
        messages.info(request,"item added to cart ")
        return redirect('Product_desc',pk=pk)
    


def Remove_item(request,pk):
    item=get_object_or_404(Product,pk=pk)
    order_qs=Order.objects.filter(
        user=request.user,
        Ordered=False,


    )
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item=Order_Item.objects.filter(
                product=item,
                user=request.user,
                Ordered=False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -=1
                order_item.save()
            else:
                order_item.dalete()
            messages.info(request,"Item quantity wa updated")
            return redirect("orderlist")
        else:
            messages.info(request, "This item is not in your cart")
            return redirect("orderlist")
    else:
        messages.info(request,"You do not have any order")
        return redirect("orderlist")


def Checkout_page(request):
    if CheckoutAddress.objects.filter(user=request.user).exists():
        return render(request,'checkout.html',{'payment_allow':"allow"})
    if request.method=='POST':
        print(request.method)
        form=CheckoutForm(request.POST)
        try:
            if form.is_valid():
                street_address=form.cleaned_data.get('street_address')
                Apparment_address=form.cleaned_data.get('Apparment_address')
                country=form.cleaned_data.get('country')
                zip_code=form.cleaned_data.get('zip_code')

                checkout_address=CheckoutAddress(
                     user=request.user,
                     street_address=street_address,
                     Apparment_address=Apparment_address,
                     country=country,
                     zip_code=zip_code,
                )
                checkout_address.save()
                print("It should render the summary page")
                return render(request,'checkout.html',{'payment_allow':"allow"})
        except Exception as e:
            messages.warning(request,'Failed Checkout')
            return redirect ('Checkout_page')
    else:
        form=CheckoutForm()
        return render(request,'checkout.html',{'form':form})

# Create your views here.



def card_payment_view(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            # Handle payment processing here
            # For example, integrate with a payment gateway API
            return redirect('payment_complete')  # Redirect to the payment confirmation page
    else:
        form = CardForm()
    return render(request, 'payment.html', {'form': form})

def payment_complete_view(request):
    return render(request, 'index.html')