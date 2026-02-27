from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Trade, Ticker, News, BlacklistedIP
from .services.utils import get_price
from django.db import transaction
from django.contrib.auth import login
from .forms import CustomUserCreationForm, TradeForm, TickerForm
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
import logging

logger = logging.getLogger('trade_registry')
# Create your views here.
@login_required
def register_trade(request):
    if request.method == 'POST':
        trade_form = TradeForm(request.POST, prefix='trade')
        ticker_form = TickerForm(request.POST, prefix='ticker')

        ticker_valid = ticker_form.is_valid()
        trade_valid = trade_form.is_valid()
        
        if ticker_valid and trade_valid:
            symbol = ticker_form.cleaned_data.get('symbol').upper()
            try:
                with transaction.atomic():
                    ticker_obj, created = Ticker.objects.get_or_create(symbol=symbol)
                    
                    if created:
                        ticker_obj.symbol = symbol
                        ticker_obj.name = ticker_form.cleaned_data.get('name') or ""
                        ticker_obj.save()
                        ticker_obj.last_price = get_price(ticker_obj)
                        ticker_obj.save()
                    
                    trade = trade_form.save(commit=False)
                    trade.user = request.user
                    trade.ticker = ticker_obj
                    trade.save()
                    return redirect('trades')
            except Exception as e:
                logger.error(f"Database error in register_trade: {e}")
                trade_form.add_error(None, f"Database error: {e}")
        else:
            if not ticker_valid:
                logger.warning(f"Ticker form errors: {ticker_form.errors.as_json()}")
                print(f"DEBUG: Ticker form errors: {ticker_form.errors.as_json()}")
            if not trade_valid:
                logger.warning(f"Trade form errors: {trade_form.errors.as_json()}")
                print(f"DEBUG: Trade form errors: {trade_form.errors.as_json()}")
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
    query = request.GET.get('q')
    if query:
        trades = trades.filter(
            Q(ticker__symbol__icontains=query) |
            Q(ticker__name__icontains=query)
        )

    status = request.GET.get('status')
    if status == 'ended':
        trades = trades.filter(sell_price__isnull=False)
    elif status == 'ongoing':
        trades = trades.filter(sell_price__isnull=True)

    for trade in trades:
        try:
            trade.live_metrics = trade.get_live_metrics(trade.ticker.last_price)
        except Exception as e:
            print("Live price couldn't be fetched")
            trade.live_metrics = trade.get_live_metrics(trade.buy_price)

    return render(request, 'trade_registry/trades.html', {'trades': trades})
@login_required
def index(request):
    news = News.objects.all()
    trades = Trade.objects.filter(user=request.user).order_by('-buy_date')
    tickers = Ticker.objects.all()
    for trade in trades:
        try:
            trade.live_metrics = trade.get_live_metrics(trade.ticker.last_price)
        except Exception as e:
            print("Live price couldn't be fetched")
            trade.live_metrics = trade.get_live_metrics(trade.buy_price)
            return render(request, 'trade_registry/index.html', {'tickers': tickers, 'news': news, 'trades': trades})
    return render(request, 'trade_registry/index.html', {'tickers': tickers, 'news': news, 'trades': trades})
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
def trade_detail(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id, user=request.user)
    trade.price = get_price(trade.ticker)
    trade.live_metrics = trade.get_live_metrics(trade.price)
    return render(request, 'trade_registry/trade_detail.html', {'trade': trade})

@login_required
def delete_trade(request, trade_id):
    if request.method == 'POST':
        trade = get_object_or_404(Trade, id=trade_id, user=request.user)
        symbol = trade.ticker.symbol
        if request.POST.get('symbol').upper() == symbol:
            trade.delete()
            messages.success(request, f"{symbol} trade has been deleted permanently.")
        else:
            messages.error(request, "Incorrect symbol entered.")
            return redirect('trade_detail', trade_id=trade_id)
    return redirect('trades')

@login_required
def close_trade(request, trade_id):
    if request.method == 'POST':
        trade = get_object_or_404(Trade, id=trade_id)
        
        sell_price = request.POST.get('sell_price')
        
        if sell_price:
            trade.sell_price = sell_price
            trade.sell_date = timezone.now()
            trade.save()
            messages.success(request, f"Trade closed")
        else:
            messages.error(request, "Must enter a valid price.")
            
        return redirect('trade_detail', trade_id=trade_id)
    
    return redirect('trades')

def honeypot(request):
    """
    Honeypot endpoint to log and detect unauthorized access attempts.
    Auto-blacklists IPs after 3 failed attempts.
    Respects DEBUG mode and whitelisted IPs for development.
    """
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown'))
    if ',' in client_ip:  # Handle multiple IPs from proxies
        client_ip = client_ip.split(',')[0].strip()
    
    user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
    
    # Check if honeypot is enabled
    honeypot_enabled = getattr(settings, 'HONEYPOT_ENABLED', True)
    auto_blacklist_enabled = getattr(settings, 'HONEYPOT_AUTO_BLACKLIST', True)
    whitelisted_ips = getattr(settings, 'HONEYPOT_WHITELIST_IPS', ['127.0.0.1', '::1'])
    
    # Skip blacklisting for whitelisted IPs (useful for localhost testing)
    is_whitelisted = client_ip in whitelisted_ips
    
    # Check if IP is already blacklisted (skip if not enabled or whitelisted)
    if honeypot_enabled and not is_whitelisted:
        try:
            blacklisted = BlacklistedIP.objects.get(ip_address=client_ip)
            logger.warning(
                f"HONEYPOT BLOCKED - Blacklisted IP attempted access | "
                f"IP: {client_ip} | Attempts: {blacklisted.attempt_count} | "
                f"User-Agent: {user_agent}"
            )
            return HttpResponseForbidden("Access denied.")
        except BlacklistedIP.DoesNotExist:
            pass
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        logger.warning(
            f"HONEYPOT ALERT - Unauthorized access attempt | "
            f"IP: {client_ip} | Username: {username} | "
            f"User-Agent: {user_agent}"
        )
        
        # Track attempt and potentially blacklist (if enabled and not whitelisted)
        if honeypot_enabled and auto_blacklist_enabled and not is_whitelisted:
            try:
                blacklist_entry = BlacklistedIP.objects.get(ip_address=client_ip)
                blacklist_entry.attempt_count += 1
                blacklist_entry.save(update_fields=['attempt_count', 'last_attempt'])
                
                if blacklist_entry.attempt_count >= 3:
                    logger.critical(
                        f"HONEYPOT - IP BLACKLISTED after {blacklist_entry.attempt_count} attempts | "
                        f"IP: {client_ip}"
                    )
                    return HttpResponseForbidden("Access denied.")
            except BlacklistedIP.DoesNotExist:
                BlacklistedIP.objects.create(
                    ip_address=client_ip,
                    reason=f"Honeypot login attempt - Username: {username}"
                )
    
    logger.info(f"HONEYPOT - GET request from IP: {client_ip} | User-Agent: {user_agent}")
    
    return render(request, 'trade_registry/honeypot.html', {
        'error': 'Invalid credentials' if request.method == 'POST' else None
    })