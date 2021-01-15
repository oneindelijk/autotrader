from django.db import models
from utils.at_exceptions import BalanceError, CurrencyError
import datetime

# Create your models here.

class Currency(models.Model):
    symbol = models.CharField('Symbol', max_length = 200)
    name = models.CharField('Name', max_length = 200) 
    abbreviation = models.CharField('Abbreviation', max_length = 200) 
    rate = models.FloatField('Exchange Rate', default = 1.000)

    def __str__(self):
        return self.abbreviation
    
class Wallet(models.Model):
    owner = models.CharField('Owner', max_length = 200)
    baseCurrency = models.ForeignKey(Currency, on_delete = models.CASCADE)
    refresh_interval = models.IntegerField('Refresh Interval', default = 86400)

    def __str__(self):
        return self.owner

    def total_balance(self):
        pass

class Balance(models.Model):
    ''' keeps track of balance per currency in Wallet '''
    wallet = models.ForeignKey(Wallet, on_delete = models.CASCADE) 
    currency = models.ForeignKey(Currency, on_delete = models.CASCADE)
    amount = models.FloatField('Amount', default = 0)

    def __str__(self):
        totalstr = '{} {:0.2f}'.format(self.currency.__str__(), self.amount)
        return totalstr
    
    def converted_balance(self, to_currency = None):
        if to_currency == None:
            return self.currency.rate * self.amount
        else:
            to_currency = Currency.objects.get(abbreviation = to_currency)
            return to_currency.rate * self.currency.rate * self.amount
        
class Operation(models.Model):
    ''' serves as a table keeping a history off all transactions '''
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField('Amount')
    operation_sign = models.BooleanField('Sign')
    currency = models.ForeignKey(Currency, on_delete = models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete = models.CASCADE)
    balance = models.ForeignKey(Balance, on_delete = models.CASCADE)

    def __str__(self):
        return datetime.datetime.strftime(self.timestamp, '%y-%m-%d %H:%M')

    def addToBalance(self, amount, currency_abbr = None):
        if currency_abbr == None:
            wallet = self.wallet
            self.currency = wallet.baseCurrency
        else:
            try:
                self.currency = Currency.objects.get(abbreviation = currency_abbr)
            except Currency.DoesNotExist:
                raise CurrencyError('Currency {} is not known in the database'.format(currency_abbr))
        if Balance.objects.filter(currency = self.currency).count() == 0:
            self.balance = Balance(currency = self.currency, wallet=self.wallet, amount = amount)
        else:
            self.balance = Balance.objects.filter(currency = self.currency)[0]
            self.balance.amount += amount
        self.amount = amount
        self.operation_sign = True
        self.balance.save()
        self.save()

    