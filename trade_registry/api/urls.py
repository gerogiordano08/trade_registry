from django.urls import path
from .views import TickerSearchAPIView

urlpatterns = [
    path('search/', TickerSearchAPIView.as_view(), name='ticker-search'),
]