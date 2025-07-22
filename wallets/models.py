from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db import models
from decimal import Decimal

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallets")
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    starting_balance = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        help_text="Optional: enter your initial budget"
    )

    @property
    def total_spent(self):
        return self.transactions.aggregate(
            total=models.Sum("amount")
        )["total"] or Decimal("0")

    @property
    def remaining_balance(self):
        if self.starting_balance is None:
            return None
        return self.starting_balance - self.total_spent

    def __str__(self):
        return self.name

class Transaction(models.Model):
    wallet    = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
    date      = models.DateField()
    reason    = models.CharField(max_length=255)
    amount    = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-date']
