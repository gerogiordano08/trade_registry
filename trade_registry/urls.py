from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_trade, name='register_trade'),
    path('trades/', views.list_trades, name='list_trades'),
]