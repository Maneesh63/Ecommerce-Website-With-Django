from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse,get_object_or_404
from .forms import AddressForm,CustomUserForm,SearchForm,CommentForm,EditDashboardForm,EditproductForm,LoginForm,ProductForm,ForgotPasswordForm,ResetPasswordForm
from django.contrib import messages
from django.core.mail import send_mail
from .models import CustomUser,Product,Comment,Cart
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from urllib.parse import quote
from django.http import JsonResponse
import razorpay
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login,logout as auth_logout,authenticate
from django.core.paginator import Paginator
 

def home(request):
    products = Product.objects.all().order_by('-date')
    search = SearchForm()

    if request.method == 'GET':
        search = SearchForm(request.GET)
        if search.is_valid():
            query = search.cleaned_data['query']
            search =Product.objects.filter(name__icontains=query)

    paginator = Paginator(products, 6)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, 'home.html', {'products': products, 'search':search, 'page_obj': page_obj})

def signup(request):

    form=CustomUserForm()

    if request.method == 'POST':

        form=CustomUserForm(request.POST)

        if form.is_valid():

            user=form.save(commit=False)

            password=form.cleaned_data['password']

            email=form.cleaned_data['password']

            username=form.cleaned_data['username']

            user.set_password(password)

            user.save()

            email=user.email

            subject = 'Welcome to our Test Authentication platform!'
            message = f'Hii {username}, Welcome! Thank you for registering with us. Complete your profile: Let the community know who you are! Add a profile picture and some information about yourself to personalize your account. Explore our features: Take some time to navigate through the platform and discover all the tools and resources available to you.'
            sender_email = 'maneeshmaneesh391@gmail.com'   
            
            send_mail(subject,message,sender_email,[email])

            user = authenticate(request,email=email,password=password)

            if user is not None:

              auth_login(request,user)

              messages.success(request,'You Became a Member of our family')

              return redirect('home')
        
    return render(request,'signup.html',{'form':form})


def login(request):

    form=LoginForm()

    if request.method == 'POST':

        form =LoginForm(request.POST)

        if form.is_valid():

            email=form.cleaned_data['email']

            password=form.cleaned_data['password']

            user = authenticate(request,email=email,password=password)

            if user is not None:

              auth_login(request,user)

              messages.success(request,'Youre Back!')

              return redirect('home')
        
    return render(request,'login.html',{'form':form})

def logout(request):

    auth_logout(request)
    
    messages.success(request,'We Miss You')

    return redirect('home')

 

def forgotpassword(request):
    form = ForgotPasswordForm()

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            user_obj = CustomUser.objects.filter(email=email).first()

            if user_obj:
                
                token = default_token_generator.make_token(user_obj)

                request.session['password_reset_email'] = email
                
                #to craete link 
                reset_link = request.build_absolute_uri(reverse('reset_password') + f'?email={quote(email)}&token={quote(token)}')

                #Mail Template Contents
                subject = 'Password Reset Request'
                message = f'Click the link below to reset your password:\n\n{reset_link}'
                send_mail(subject, message, 'maneeshmaneesh391@gmail.com', [email])

                messages.success(request, 'An email has been sent with instructions to reset your password.')
                return redirect('forgot_password')
            else:
                messages.error(request, 'No user found with that email address.')
    else:
        form = ForgotPasswordForm

    return render(request, 'forgot_password.html', {'form': form})


def reset_password(request):
    form = ResetPasswordForm()
    email = request.GET.get('email')
    token = request.GET.get('token')

    if not (email and token):
        messages.error(request, 'Email or token missing in request itself')
        return HttpResponseRedirect(reverse('forgot_password'))

    user = CustomUser.objects.filter(email=email).first()

    session_email = request.session.get('password_reset_email')

    if user and session_email == email and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()

                
                messages.success(request, 'Your password has been reset successfully.')
                del request.session['password_reset_email']

                return redirect('login')
    else:
        messages.error(request, 'Invalid email or token.')

    return render(request, 'reset_password.html', {'form': form, 'email': email, 'token': token})



def create_product(request):
  
  form=ProductForm()
  

  if request.method == 'POST':
      
      form=ProductForm(request.POST,request.FILES)

      if form.is_valid():
          
          product=form.save(commit=False)
          
          product.user=request.user

          product.save()

          messages.success(request,'Your product Created')

          return redirect('home')
      
  return render(request,'create_product.html',{'form':form})
 

def edit_product(request,pk):
    
    product=get_object_or_404(Product,pk=pk)

    form=EditproductForm(instance=product)

    if request.method == 'POST':
        
        form=EditproductForm(request.POST,request.FILES,instance=product)

        if form.is_valid():
            
            form.save()
            
            messages.success(request,'Your Product was edited successfully!')
            return redirect('home')
    
        else:

         form=EditproductForm(instance=product)
 
    return render(request,'edit_product.html',{'form':form,'product':product})

def list_product(request):

    product = Product.objects.all().order_by('-date')
    search = SearchForm()

    if request.method == 'GET':
        search = SearchForm(request.GET)
        if search.is_valid():
            query = search.cleaned_data['query']
            search =Product.objects.filter(name__icontains=query)

    paginator = Paginator(product, 6)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request,'list_product.html',{'product':product,'search':search, 'page_obj': page_obj})


def delete_product(request,pk):
   product=get_object_or_404(Product,pk=pk)
   product.delete()
   return redirect('list')


def product_detail(request,pk):

    product=get_object_or_404(Product,pk=pk)

    return render(request,'product_detail.html',{'product':product})

def dashboard(request):
    
    user= request.user
    
    product=Product.objects.filter(user=user).order_by('-date')

    return render(request,'dashboard.html',{'product':product})


def edit_dashboard(request):
    
    form = EditDashboardForm(instance=request.user)  # Pass instance to prepopulate the form
    

    if request.method == 'POST':
    
        form=EditDashboardForm(request.POST,instance=request.user)

        if form.is_valid():

            form.save()
            
            messages.success(request,'profile edited successfully')

            return redirect('dashboard')
        
    return render(request,'edit_dashboard.html',{'form':form})

def add_cart(request, pk):

    product = get_object_or_404(Product, pk=pk)
    
    cart, created = Cart.objects.get_or_create(product=product,user=request.user)
    
    cart.quantity +=1

    cart.save()

    return redirect('cart')


def list_cart(request):

    carts = Cart.objects.filter(user=request.user)

    #total=sum(item.product.discounted_price * item.quantity for item in wishlist)

    return render(request, 'wishlist.html', {'carts': carts})
    
     
def remove_cart(request,pk):

    cart=get_object_or_404(Cart,pk=pk)
    cart.delete()
    return redirect('cart')


def increase_quantity(request, pk):
    cart_item= get_object_or_404(Cart, pk=pk)
    cart_item.quantity += 1
     
    cart_item.save()
    return JsonResponse({'quantity': cart_item.quantity})
    

def decrease_quantity(request,pk):
    cart_item = get_object_or_404(Cart, pk=pk)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        
        cart_item.save()
    return JsonResponse({'quantity': cart_item.quantity})

 
def comment(request,pk):

    form=CommentForm()

    product=get_object_or_404(Product,pk=pk)

    if request.method == 'POST':

        form=CommentForm(request.POST)

        if form.is_valid():

            comment=form.save(commit=False)

            comment.product=product

            comment.save()

            return redirect('product_detail',product.pk)
        else:

            form=CommentForm()

    return render(request,'p_reviews.html',{'product':product})

def delete_comment(request,pk):

    comment=get_object_or_404(Comment,pk=pk)

    comment.delete()

    return redirect('product_detail ')



def address(request,pk):

    product=get_object_or_404(Product,pk=pk)

    form=AddressForm()

    if request.method == 'POST':

        form=AddressForm(request.POST)

        if form.is_valid():

              address=form.save(commit=False)
           
              address.user=request.user

              address.product=product

              address.save()

              return redirect('payment',pk=product.pk)
            
    return render(request,'address.html',{'product':product,'form':form})


def common(request):

    form=SearchForm()
    
    results=[]

    if 'query' in request.GET:

        form=SearchForm(request.GET)

        if form.is_valid():

            query=form.cleaned_data['query']
            
            results=Product.objects.filter(name__icontains=query)

            
            return render(request,'common.html',{'form':form,'results':results,'query':query})



razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def initiate_payment(request, pk):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=pk)
        amount = float(product.discounted_price * 100)

        request.session['payment_amount'] = amount
        currency = 'INR'

        # Create Razorpay order with automatic capture (optional)
        razorpay_order = razorpay_client.order.create(dict(
            amount=amount,
            currency=currency,
            payment_capture='1'  # Capture payment immediately (optional)
        ))

        razorpay_order_id = razorpay_order['id']
        callback_url = request.build_absolute_uri(reverse('payment_success'))

        context = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'razorpay_amount': amount,
            'currency': currency,
            'callback_url': callback_url,
            'product': product
        }

        return render(request, 'payment.html', context=context)

@csrf_exempt
def paymenthandler(request):
    if request.method not in ['GET', 'POST']:
        return HttpResponseBadRequest('Invalid request method.')  # Early exit for invalid methods

    try:
        amount = request.session.get('payment_amount', 0)
        payment_id = request.GET.get('razorpay_payment_id', '')
        razorpay_order_id = request.GET.get('razorpay_order_id', '')
        signature = request.GET.get('razorpay_signature', '')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # Verify payment signature (ensure correct order of parameters)
        verification_result = razorpay_client.utility.verify_payment_signature(params_dict)
        print("Verification Result:", verification_result)

        razorpay_order = request.context.get('razorpay_order')
        if razorpay_order:  # Add the missing colon
            # Access order details from razorpay_order dictionary
            if 'payment_capture' not in razorpay_order:
                capture_response = razorpay_client.payment.capture(payment_id, amount)
                print("Capture Response:", capture_response)
                return render(request, 'payment_success.html')
            else:
                print("Payment already captured")
                return render(request, 'payment_success.html')

        else:
            print("Verification Failed")
            return HttpResponse('Payment verification failed')

    except Exception as e:
        print("Error:", e)  # Log the error for debugging
        return HttpResponseBadRequest('An error occurred during payment processing.')
