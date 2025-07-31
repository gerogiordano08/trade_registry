from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register-trades/', views.register_trade, name='register_trade'),
    path('trades/', views.list_trades, name='trades'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('help/', views.help, name='help'),
    path('signup/', views.signup, name='signup'),
]