from django import forms 
from daraz.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model=User
        fields=["email","name","password1","password2"]

    

class PasswordResetForm(forms.Form):
    email=forms.EmailField(max_length=254,required=True,widget=forms.EmailInput(attrs={'placeholder':'you@gmail.com'}))
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(('No account is associated with this email address'))
        return email
