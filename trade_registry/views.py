from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Trade
from .utils import get_price
from django.utils import timezone
from decimal import Decimal
# Create your views here.
@login_required
def register_trade(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        quantity = int(request.POST['quantity'])
        buy_date = request.POST['buy_date']
        buy_price = float(request.POST['buy_price'])
        sell_date = request.POST.get('sell_date') or None
        sell_price = request.POST.get('sell_price')
        sell_price = float(sell_price) if sell_price else None

        buy_date = timezone.datetime.strptime(buy_date, '%Y-%m-%d').date()

        if sell_date:
            sell_date = timezone.datetime.strptime(sell_date, '%Y-%m-%d').date()


        trade = Trade(
            user = request.user,
            ticker = ticker,
            quantity = quantity,
            buy_date = buy_date,
            buy_price = buy_price,
            sell_date = sell_date,
            sell_price = sell_price,
        )
        trade.save()
        return redirect('trades')
    return render(request, 'trade_registry/register.html')
@login_required
def list_trades(request):
    trades = Trade.objects.filter(user=request.user).order_by('-buy_date')
    ticker_set = set(trade.ticker for trade in trades if not trade.sell_date)
    live_prices = {}
    for ticker in ticker_set:
        live_prices[ticker] = get_price(ticker)
    for trade in trades:
        if not trade.sell_date:
            price = live_prices[trade.ticker]
            trade.live_profit = (Decimal(price) - trade.buy_price) * trade.quantity
            trade.live_percentage_profit = trade.live_profit / (trade.quantity * trade.buy_price)
    
    return render(request, 'trade_registry/trades.html', {'trades': trades})