from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

class UserUpdateForm(UserChangeForm):
    # Remove password field
    password = None
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name','mobile_number']
        widgets = {
            'email': forms.EmailInput(attrs={'required': True}),
        }
   
