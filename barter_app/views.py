from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, CustomUserAuthenticationForm, AdForm, ProfileForm
from .models import Ad, User, ExchangeProposal
from barter_app import models

cat = {
    'Электроника': 'Electronics',
    'Одежда': 'Clothing',
    'Книги': 'Books',
    'Другое': 'Other',
}


def ad_list(request):
    ads = Ad.objects.all()    
   
    categories = Ad.AD_CATEGORY_VALUES

    query = request.GET.get('q')
    category = request.GET.get('category')
    
    if query:
        ads = ads.filter(title__icontains=query)  
    if category:

        view_category = cat[category]

        ads = ads.filter(category=view_category) 

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
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('my_ads')
    else:
        form = AdForm()
    return render(request, 'ads/my_ads.html', {'ads': ads, 'form': form})


def ad_detail(request, ad_id):
    ad = Ad.objects.get(pk=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})


@login_required
def ad_update(request, ad_id):
    ad = Ad.objects.get(pk=ad_id)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', ad_id)
        #return redirect(f'ad_detail/{ad.id}')
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/ad_update.html', {'form': form, 'ad': ad})

@login_required
def ad_delete(request, ad_id):
    ad = Ad.objects.get(pk=ad_id)
    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ads/ad_delete.html', {'ad': ad})






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

@login_required
def user_profile(request):
    return render(request, 'auth/my_profile.html')



@login_required
def user_profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'auth/edit_profile.html', {'form': form})

def my_exchanges(request):
    pass