from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Trade
from .utils import get_price
from django.utils import timezone
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
        ended = sell_date is not None and sell_price is not None

        buy_date = timezone.datetime.strptime(buy_date, '%Y-%m-%d').date()

        if sell_date:
            sell_date = timezone.datetime.strptime(sell_date, '%Y-%m-%d').date()

        if sell_price:
            profit = (sell_price - buy_price) * quantity 
        else:
            if get_price(timezone.now().date().isoformat(), ticker) == None:
              return render(request, 'trade_registry/register.html', 
                {'error': f'Error fetching price data for: {ticker}',
                 'buy_date': buy_date, 'quantity': quantity, 'buy_price': buy_price,})
            else:
                profit = (get_price(timezone.now().date().isoformat(), ticker) - buy_price) * quantity

        trade = Trade(
            user = request.user,
            ticker = ticker,
            quantity = quantity,
            buy_date = buy_date,
            buy_price = buy_price,
            sell_date = sell_date,
            sell_price = sell_price,
            ended = ended,
            profit = profit
        )
        trade.save()
        return redirect('trades')
    return render(request, 'trade_registry/register.html')
@login_required
def list_trades(request):
    trades = Trade.objects.filter(user=request.user).order_by('-buy_date')
    return render(request, 'trade_registry/trades.html', {'trades': trades})