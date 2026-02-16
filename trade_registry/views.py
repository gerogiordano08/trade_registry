from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trade, Ticker
from .services.utils import get_live_prices_bulk, get_price
from django.db import transaction
from django.contrib.auth import login
from .forms import CustomUserCreationForm, TradeForm, TickerForm
from django.contrib import messages
from django.utils import timezone

# Create your views here.
@login_required
def register_trade(request):
    if request.method == 'POST':
        trade_form = TradeForm(request.POST, prefix='trade')
        ticker_form = TickerForm(request.POST, prefix='ticker')
        if ticker_form.is_valid() and trade_form.is_valid():
            symbol = ticker_form.cleaned_data.get('symbol').upper()
            try:
                with transaction.atomic():
                    ticker_obj, created = Ticker.objects.get_or_create(symbol=symbol)
                    
                    if created:
                        ticker_obj.symbol = symbol
                        ticker_obj.name = ticker_form.cleaned_data.get('name') or ""
                        ticker_obj.save()
                    
                    trade = trade_form.save(commit=False)
                    trade.user = request.user
                    trade.ticker = ticker_obj
                    trade.save()
                    return redirect('trades')
            except Exception as e:
                trade_form.add_error(None, f"Database error: {e}")
    else:
        trade_form = TradeForm(prefix='trade')
        ticker_form = TickerForm(prefix='ticker')

    return render(request, 'trade_registry/register.html', {
        'trade_form': trade_form,
        'ticker_form': ticker_form
    })
@login_required
def list_trades(request):
    trades = Trade.objects.filter(user=request.user).order_by('-buy_date')
    ticker_set = set(trade.ticker.symbol for trade in trades if not trade.sell_date)
    live_prices = get_live_prices_bulk(ticker_set)
    for trade in trades:
        if not trade.sell_date:
            trade.price = live_prices[trade.ticker.symbol]
            try:
                trade.live_metrics = trade.get_live_metrics(trade.price)
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
    trade.price = get_price(trade.ticker)
    trade.live_metrics = trade.get_live_metrics(trade.price)
    return render(request, 'trade_registry/trade_detail.html', {'trade': trade})

@login_required
def delete_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id, user=request.user)
    symbol = trade.ticker.symbol
    trade.delete()
    
    messages.success(request, f"{symbol} trade has been deleted permanently.")
    return redirect('trades') 

@login_required
def close_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id, user=request.user)
    
    trade.sell_date = timezone.now()
    # trade.sell_price =
    trade.save()
    
    messages.info(request, f"{trade.ticker.symbol} closed succesfully.")
    return redirect('trade_detail', {'trade': trade})