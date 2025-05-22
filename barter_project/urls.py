from django.contrib import admin
from django.urls import path
from barter_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.ad_list, name="ad_list"),
    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),

    path('my_profile/', views.user_profile, name='profile'),
    path('my_profile/edit/', views.user_profile_edit, name='edit_profile'),

    path('ad_create/', views.ad_create, name='ad_create'),
    path('ad_detail/<int:ad_id>/', views.ad_detail, name='ad_detail'),

    path('ad_update/<int:ad_id>/', views.ad_update, name='ad_update'),
    path('ad_delete/<int:ad_id>/', views.ad_delete, name='ad_delete'),
    
    path('exchange_create/<int:ad_r_id>/', views.exchange_create, name='exchange_create'),

    path('exchange_detail/<int:exchange_id>/<int:exchange_type>/', views.exchange_detail, name='exchange_detail'),

    path('exchange_accept/<int:exchange_id>/', views.exchange_accept, name='exchange_accept'),
    path('exchange_reject/<int:exchange_id>/', views.exchange_reject, name='exchange_reject'),

    path('exchange_cancel/<int:exchange_id>/', views.exchange_cancel, name='exchange_cancel'),

    path('my_exchanges/', views.my_exchanges, name='my_exchanges'),

    path('my_ads/', views.my_ads, name='my_ads'),
]
