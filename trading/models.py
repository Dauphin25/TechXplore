from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
import random
import threading
import time
from django.db.models.signals import post_save
from django.dispatch import receiver


class Trader(models.Model):
    STATUS_CHOICES = [
        ('Pupil', 'School Pupil'),
        ('Student', 'Student'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)  # Updated to store total value

    def calculate_total_value(self):
        total_value = self.balance
        stocks = Stock.objects.filter(trader=self)

        for stock in stocks:
            total_value += stock.company.percentage * stock.investment

        return total_value.quantize(Decimal('0.01'))  # Ensure the total_value is rounded to two decimal places

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"

    @classmethod
    def update_all_traders_total_value(cls):
        while True:
            traders = cls.objects.all()
            for trader in traders:
                trader.total_value = random.randint(980, 1050)  # This will trigger the total_value property
                trader.save()
            time.sleep(5)


class Company(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, unique=True)
    change = models.DecimalField(max_digits=6, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    volume = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    @classmethod
    def update_values(cls):
        while True:
            companies = cls.objects.all()
            for company in companies:
                new_volume = random.randint(4000000, 45000000)
                new_change = random.uniform(-10, 10)
                new_percentage = random.uniform(-1, 1)

                company.volume = new_volume
                company.change = new_change
                company.percentage = new_percentage

                company.save()

            time.sleep(5)


class Stock(models.Model):
    trader = models.ForeignKey('Trader', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    investment = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def percentage(self):
        return (self.investment / self.trader.balance) * 100

    def __str__(self):
        return f"{self.trader.user.username} - {self.company.name}: ${self.investment}"


class Buy(models.Model):
    trader = models.ForeignKey('Trader', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Buy: {self.trader.user.username} - {self.company.name}: ${self.amount}"


class Sell(models.Model):
    trader = models.ForeignKey('Trader', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sell: {self.trader.user.username} - {self.company.name}: ${self.amount}"


@receiver(post_save, sender=Buy)
def update_trader_balance_buy(sender, instance, created, **kwargs):
    if created:
        trader = instance.trader
        trader.balance -= instance.amount
        trader.save()


@receiver(post_save, sender=Sell)
def update_trader_balance_sell(sender, instance, created, **kwargs):
    if created:
        trader = instance.trader
        trader.balance += instance.amount
        trader.save()


# Start the update threads when the server starts
company_update_thread = threading.Thread(target=Company.update_values)
company_update_thread.daemon = True
company_update_thread.start()

trader_update_thread = threading.Thread(target=Trader.update_all_traders_total_value)
trader_update_thread.daemon = True
trader_update_thread.start()
