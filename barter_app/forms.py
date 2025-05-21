from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Ad, ExchangeProposal


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name','email']  

class CustomUserAuthenticationForm(AuthenticationForm):
    pass

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }


class ProfileEditForm(forms.ModelForm):
    password = None  # Убираем поле смены пароля
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name', 
            'last_name',
            'email',
            'bio',
            # 'avatar'  # Если у вас есть поле avatar в модели
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': True}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'category': forms.Select(choices=Ad.category),
            'condition': forms.Select(choices=Ad.condition)
        }

class AdDetails(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'category': forms.Select(choices=Ad.get_category_display(Ad)),
            'condition': forms.Select(choices=Ad.get_condition_display(Ad))
        }

class CreateExchange(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_reciever_id', 'ad_sender_id', 'status', 'comment']
        widgets = {
            'status': forms.Select(choices=ExchangeProposal.EP_STATUS)
        }
