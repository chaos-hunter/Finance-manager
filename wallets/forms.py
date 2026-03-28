from django import forms
from .models import Wallet, Transaction
from decimal import Decimal


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ["name", "starting_balance"]
        widgets = {
            "starting_balance": forms.NumberInput(attrs={"step":"0.01"}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'reason', 'amount']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

class TopUpForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, decimal_places=2,
        min_value=Decimal("0.01"),
        widget=forms.NumberInput(attrs={"step":"0.01"})
    )
