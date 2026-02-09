from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trade
from .api.service_utils import get_live_prices_bulk
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm, TradeForm
# Create your views here.
@login_required
def register_trade(request):
    if request.method == 'POST':
        form = TradeForm(request.POST, request=request)
        if form.is_valid():
            # Aquí Django ya validó que los números sean números y las fechas sean fechas
            trade = form.save(commit=False)
            trade.user = request.user
            trade.save()
            return redirect('trades')
    else:
        form = TradeForm()
    return render(request, 'trade_registry/register.html', {'form': form})
@login_required
def list_trades(request):
    trades = Trade.objects.filter(user=request.user).order_by('-buy_date')
    ticker_set = set(trade.ticker for trade in trades if not trade.sell_date)
    live_prices = get_live_prices_bulk(ticker_set)
    for trade in trades:
        if not trade.sell_date:
            price = live_prices[trade.ticker]
            try:
                trade.live_metrics = trade.get_live_metrics(price)
            except Exception as e:
                print("Live price couldn't be fetched")
                trade.live_metrics = trade.get_live_metrics(trade.buy_price)
                return render(request, 'trade_registry/trades.html', {'trades': trades})
    return render(request, 'trade_registry/trades.html', {'trades': trades})
@login_required
def index(request):
    first_name = request.user.first_name if request.user.first_name else "User"
    return render(request, 'trade_registry/index.html', {'first_name': first_name})
@login_required
def help(request):
    return render(request, 'trade_registry/help.html')
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error= form.errors.as_data()
            return render(request, 'registration/signup.html', {'form': form, 'error': error})
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
@login_required
def settings(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        if first_name:
            user.first_name = first_name
        if email:
            user.email = email
        if username:
            user.username = username
        user.save()
        return redirect('index')
    return render(request, 'trade_registry/settings.html', {'user': user})
@login_required
def delete_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id, user=request.user)
    if request.method == 'POST':
        trade.delete()
        return redirect('trades')
    return render(request, 'trade_registry/confirm_delete.html', {'trade': trade})
@login_required
def trade_detail(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id, user=request.user)
    return render(request, 'trade_registry/trade_detail.html', {'trade': trade})