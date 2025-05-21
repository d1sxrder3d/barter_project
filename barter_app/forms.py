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
        # ad_reciever устанавливается в view, ad_sender выбирается пользователем из его объявлений
        fields = ['ad_sender', 'comment']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        ad_for_exchange = kwargs.pop('ad_for_exchange', None) # Это r_ad из view
        super().__init__(*args, **kwargs)

        if user:
            
            queryset = Ad.objects.filter(user=user)
            if ad_for_exchange:
                queryset = queryset.exclude(pk=ad_for_exchange.pk)
            
            self.fields['ad_sender'].queryset = queryset
            self.fields['ad_sender'].label = "Ваше объявление для обмена"
            self.fields['ad_sender'].empty_label = "Выберите ваше объявление" # Опционально
            
            if not queryset.exists():
                # Если у пользователя нет подходящих объявлений, можно отключить поле
                self.fields['ad_sender'].disabled = True
                self.fields['ad_sender'].help_text = "У вас нет других объявлений для предложения обмена."
        else:
            self.fields['ad_sender'].queryset = Ad.objects.none()
            self.fields['ad_sender'].disabled = True
        
        self.fields['comment'].label = "Комментарий к предложению (необязательно)"


class MyExchangesForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=ExchangeProposal.status)
        }
    