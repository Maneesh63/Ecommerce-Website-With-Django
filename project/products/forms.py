from django import forms

from .models import CustomUser,Product,Comment,Address,Categories


class CustomUserForm(forms.ModelForm):

    class Meta:
        fields=['username','email','password']
        model=CustomUser

class LoginForm(forms.Form):

    email=forms.EmailField(max_length=400,label='Email',widget=forms.EmailInput)

    password=forms.CharField(label='Password',widget=forms.PasswordInput)
    
class ProductForm(forms.ModelForm):

    class Meta:

        fields=['category','name','description','image','orginal_price','discounted_price']
        model=Product
       
        image=forms.ImageField(required=False)

class ForgotPasswordForm(forms.Form):

    email=forms.EmailField(max_length=100,label='Email',widget=forms.EmailInput)




class ResetPasswordForm(forms.Form):

    new_password=forms.CharField(max_length=100,widget=forms.PasswordInput(),label='New Password')


class EditproductForm(forms.ModelForm):
  
    name = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    image = forms.ImageField(label='Image', required=False)  # Required may vary based on your needs
    orginal_price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2, min_value=0)
    discounted_price = forms.DecimalField(label='Discounted Price', max_digits=10, decimal_places=2, min_value=0)
    

    class Meta:
        model = Product
        fields = ['category','name', 'description', 'image', 'orginal_price', 'discounted_price']


class EditDashboardForm(forms.ModelForm):
  
     class Meta:
        fields=['username','email']
        model=CustomUser


class CommentForm(forms.ModelForm):

    class Meta:
        fields=['comment']
        model=Comment


class AddressForm(forms.ModelForm):
    mobilenumber = forms.CharField(label='Mobile Number', max_length=50)
    address = forms.CharField(label='Address', max_length=100)
    pincode = forms.CharField(label='Pincode', max_length=10)
    state = forms.CharField(label='State', max_length=50)
    city = forms.CharField(label='City', max_length=50)
    

    class Meta:

        fields=['mobilenumber','address','pincode','state','city']
        model=Address


class SearchForm(forms.Form):

    query=forms.CharField(label='Search', max_length=200)
 

 
class CategoryForm(forms.ModelForm):
  class Meta:
    model = Categories
    fields = ['name']