from django import forms
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Trade
from .api.utils import is_ticker_in_session_pool
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', })
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        
        fields = ['ticker', 'buy_date', 'buy_price', 'quantity', 'sell_date', 'sell_price']
        
        widgets = {
            'ticker': forms.TextInput(attrs={
                'id': 'ticker', 
                'class': 'form-control',
                'placeholder': 'Ej: AAPL',
                'autocomplete': 'off'
            }),
            'buy_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sell_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'buy_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sell_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_ticker(self):
        ticker = self.cleaned_data.get('ticker').upper().strip()
        session_id = self.request.session.session_key if self.request else None
        if not is_ticker_in_session_pool(session_id, ticker):
            raise forms.ValidationError(
                "Error: Ticker must be selected from dropdown list."
            )

        return ticker