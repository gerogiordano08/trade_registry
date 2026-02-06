from django.urls import path
from .views import TickerSearchAPIView

urlpatterns = [
    path('search/<str:service>/', TickerSearchAPIView.as_view(), name='ticker-search'),
]