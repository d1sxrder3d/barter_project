from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, CustomUserAuthenticationForm, AdForm, ProfileForm, CreateExchange, MyExchangesForm
from .models import Ad, User, ExchangeProposal

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

@login_required
def exchange_create(request, ad_r_id):
    r_ad = get_object_or_404(Ad, pk=ad_r_id) # Объявление, которое хотят получить

    if r_ad.user == request.user:
        messages.error(request, "Вы не можете предложить обмен на свое собственное объявление.")
        return redirect('ad_detail', ad_id=r_ad.id)

    # Проверка, есть ли у пользователя объявления для предложения
    user_ads_to_offer = Ad.objects.filter(user=request.user).exclude(pk=r_ad.pk)
    if not user_ads_to_offer.exists():
        messages.error(request, "У вас нет объявлений, которые можно предложить для обмена (кроме текущего, если оно ваше).")
        return redirect('ad_detail', ad_id=r_ad.id)

    if request.method == 'POST':
        form = CreateExchange(request.POST, user=request.user, ad_for_exchange=r_ad)
        if form.is_valid():
            exchange = form.save(commit=False)
            exchange.ad_reciever = r_ad 
            
            exchange.save()
            messages.success(request, 'Предложение обмена успешно отправлено.')
            return redirect('exc/my_exchanges')
            #return redirect('ad_detail', ad_id=r_ad.id) 
        else:
            
            return render(request, 'exc/exchange_create.html', {
                'form': form, 
                'r_ad': r_ad
            })
    else: # GET request
        form = CreateExchange(user=request.user, ad_for_exchange=r_ad)
    return render(request, 'exc/exchange_create.html', {'form': form, 'r_ad': r_ad})

@login_required
def my_exchanges(request):
    all_user_exchanges = request.user.get_user_exchanges().order_by('-created_at')

    incoming = all_user_exchanges.filter(
        ad_reciever__user=request.user, 
        status=ExchangeProposal.EP_STATUS[0][0]  # 'Pending'
    )

    outgoing = all_user_exchanges.filter(
        ad_sender__user=request.user, 
        status=ExchangeProposal.EP_STATUS[0][0]  # 'Pending'
    )

    accepted = all_user_exchanges.filter(
        status = ExchangeProposal.EP_STATUS[1][0]
    )
    rejected = all_user_exchanges.filter(
        status = ExchangeProposal.EP_STATUS[2][0]
    )

    return render(request, 'exc/my_exchanges.html', {'incoming': incoming, 
                            'outgoing': outgoing, 'accepted': accepted, 'rejected': rejected})



@login_required
def exchange_detail(request, exchange_id, exchange_type):

    exchange = get_object_or_404(ExchangeProposal, pk=exchange_id)
    r_ad = exchange.ad_reciever
    s_ad = exchange.ad_sender
    
    if exchange_type == 1:
        #Входящее
        return render(request, 'exc/inc_exchange_detail.html', {'exchange': exchange, 'r_ad': r_ad, 's_ad': s_ad})
    if exchange_type == 2:
        #Исходяшее
        return render(request, 'exc/out_exchange_detail.html', {'exchange': exchange, 'r_ad': r_ad, 's_ad': s_ad})
    #Архивное
    return render(request, 'exc/arc_exchange_detail.html', {'exchange': exchange, 
            'r_ad': r_ad, 's_ad': s_ad, 'exchange_status': exchange.get_status_display()})

@login_required
def exchange_cancel(request, exchange_id):

    exchange = get_object_or_404(ExchangeProposal, pk=exchange_id)

    if request.method == 'POST':
        exchange.delete()
        return redirect('my_exchanges')
    return render(request, 'exc/exchange_cancel.html', {'exchange': exchange})

@login_required
def exchange_reject(request, exchange_id):

    exchange = get_object_or_404(ExchangeProposal, pk=exchange_id)
    if request.method == 'POST':
        exchange.status = ExchangeProposal.EP_STATUS[2][0]
        exchange.save()
        return redirect('my_exchanges')
    
@login_required
def exchange_accept(request, exchange_id):

    exchange = get_object_or_404(ExchangeProposal, pk=exchange_id)
    if request.method == 'POST':
        exchange.status = ExchangeProposal.EP_STATUS[1][0]
        exchange.save()
        return redirect('my_exchanges')
    