from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, CustomUserAuthenticationForm, AdForm
from .models import Ad, User, ExchangeProposal



def ad_list(request):
    ads = Ad.objects.all()    
    categories = Ad.Category.values
    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        ads = ads.filter(title__icontains=query)  
    if category:
        ads = ads.filter(category=category) 

    return render(request, 'ads/ad_list.html', {
        'ads': ads, 'query': query, 'categories': categories
    })



@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)  
            ad.user = request.user  
            ad.save()  
            return redirect('ad_list')
    else:
        form = AdForm()
    return render(request, 'ads/ad_create.html', {'form': form})

@login_required
def my_ads(request):
    ads = Ad.objects.filter(user=request.user)
    return render(request, 'ads/my_ads.html', {'ads': ads})


def ad_detail(request, ad_id):
    ad = Ad.objects.get(pk=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})






def user_register(request):
    if request.method == "POST":
        
        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()
            login(request, user)

            messages.success(request, "Регистрация прошла успешно.")
            
            return redirect('ad_list')
        else:
            messages.error(request, "Ошибка при регистрации.")
            return render(request, 'auth/register.html', {'form': form})
    else:

        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = CustomUserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Вход выполнен успешно.")

                return redirect('ad_list')
            else: 
                messages.error(request, "Неверный логин или пароль.")
                return render(request, 'auth/login.html', {'form': form})
    else:
        form = CustomUserAuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Выход выполнен успешно.")
    return redirect('ad_list')
