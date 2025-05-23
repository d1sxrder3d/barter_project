from django.contrib import admin
from django.urls import path
from barter_app.views import AdView, ExchangeView, UserView
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', AdView.ad_list, name="ad_list"),
    
    path('login/', UserView.user_login, name='login'),
    path('logout/', UserView.user_logout, name='logout'),
    path('register/', UserView.user_register, name='register'),

    path('my_profile/', UserView.user_profile, name='profile'),
    path('my_profile/edit/', UserView.user_profile_edit, name='edit_profile'),

    path('ad_create/', AdView.ad_create, name='ad_create'),
    path('ad_detail/<int:ad_id>/', AdView.ad_detail, name='ad_detail'),

    path('ad_update/<int:ad_id>/', AdView.ad_update, name='ad_update'),
    path('ad_delete/<int:ad_id>/', AdView.ad_delete, name='ad_delete'),
    
    path('exchange_create/<int:ad_r_id>/', ExchangeView.exchange_create, name='exchange_create'),

    path('exchange_detail/<int:exchange_id>/<int:exchange_type>/', ExchangeView.exchange_detail, name='exchange_detail'),

    path('exchange_accept/<int:exchange_id>/', ExchangeView.exchange_accept, name='exchange_accept'),
    path('exchange_reject/<int:exchange_id>/', ExchangeView.exchange_reject, name='exchange_reject'),

    path('exchange_cancel/<int:exchange_id>/', ExchangeView.exchange_cancel, name='exchange_cancel'),


    path('my_exchanges/', ExchangeView.my_exchanges, name='my_exchanges'),
    path('my_ads/', AdView.my_ads, name='my_ads'),
]

