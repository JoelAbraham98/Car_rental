from django import forms
from .models import UserProfile,Car,CarCategory,Payment,Booking,Review
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    Name = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
  
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class': 'form-control'}),
        help_text=None,
    ) 
    password2 = forms.CharField(
        label="Password Confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class': 'form-control'}),
        help_text=None,
    ) 
    email = forms.EmailField(
    label="Email",
    widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}),
    )
    class Meta:
        model = User
        fields = ('Name', 'email', 'phone_number', 'username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'username', 'class': 'form-control'}),
           }
class  customloginform(AuthenticationForm):
  
    class meta:
             model= User
             fields = ['username','password']
             widgets= {
                'username': forms.TextInput(attrs={'autocomplete': 'username', 'class': 'form-control', 'id':"formGroupExampleInput", 'placeholder' : "Username"}), 
                  'password': forms.PasswordInput(attrs={'autocomplete': 'new-password','class': 'form-control','id':"formGroupExampleInput" ,'placeholder' : "Password"}),
                  }
      

class BookingForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
          model =Booking
          fields =['start_date','end_date']

  
    
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['user', 'booking', 'amount', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'status']