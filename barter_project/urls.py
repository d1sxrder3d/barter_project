from django.contrib import admin
from django.urls import path
from barter_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.ad_list, name="ad_list"),
    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),

    path('ad_create/', views.ad_create, name='ad_create'),
    path('ad_detail/<int:ad_id>/', views.ad_detail, name='ad_detail'),
]
