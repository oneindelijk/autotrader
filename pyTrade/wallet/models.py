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
    
    def refresh(self):
        pass

    def getByAbbreviation(self, abbreviation):
        try:
            currency = Currency.objects.get(abbreviation = abbreviation)
        except Currency.DoesNotExist:
            raise CurrencyError('Currency {} is not known in the database'.format(abbreviation))
        else:
            return currency
    
class Wallet(models.Model):
    owner = models.CharField('Owner', max_length = 200)
    baseCurrency = models.ForeignKey(Currency, on_delete = models.CASCADE)
    refresh_interval = models.IntegerField('Refresh Interval', default = 86400)
     

    def __str__(self):
        return self.owner

    def total_balance(self):
        total = 0
        for bal in Balance.objects.filter(wallet = self):
            total += bal.converted_balance()
        return total

    def get_CurrencyByAbbreviation(self, currency_abbr):
        ''' wrapper to deal with None values for currency_abbr '''
        if currency_abbr == None:
            return self.baseCurrency
        else:
            return Currency.getByAbbreviation(None, abbreviation = currency_abbr)

    def single_balance(self, currency_abbr = None):
        currency = self.get_CurrencyByAbbreviation(currency_abbr)
        return Balance.objects.get(wallet = self, currency = currency).amount

    def total_balance_str(self):
        return '{} {:0.2f}'.format(self.baseCurrency.symbol,self.total_balance())

    def wallet_rate(self):
        ''' return rate to use for conversion '''
        return 1/self.baseCurrency.rate 

    def addToBalance(self, amount, currency_abbr = None):
        O = Operation(wallet = self)
        O.addToBalance(amount, currency_abbr)

    def getBalanceAmount(self, currency_abbr = None):
        currency = self.get_CurrencyByAbbreviation(currency_abbr)
        try:
            balance = Balance.objects.get(wallet = self, currency = currency)
        except Balance.DoesNotExist:
            raise BalanceError('Wallet does not contain any amount from {}'.format(currency))
        else:
            return balance.amount

    def subtractFromBalance(self, amount, currency_abbr = None):
        balance_amount = self.getBalanceAmount(currency_abbr)
        currency = self.get_CurrencyByAbbreviation(currency_abbr) 
        if balance_amount < amount:
            raise BalanceError('Wallet contains only {} {}'.format(currency, balance_amount))
        else:
            balance = Balance.objects.get(wallet = self, currency = currency)
            balance.amount -= amount
            O = Operation(wallet = self, amount = amount, operation_sign = False, currency = currency, balance = balance)
            balance.save()
            O.save()


class Balance(models.Model):
    ''' keeps track of balance per currency in Wallet '''
    wallet = models.ForeignKey(Wallet, on_delete = models.CASCADE) 
    currency = models.ForeignKey(Currency, on_delete = models.CASCADE)
    amount = models.FloatField('Amount', default = 0)

    def __str__(self):
        totalstr = '[W{}]{} {:0.2f}'.format(self.wallet.id, self.currency.__str__(), self.amount)
        return totalstr
    
    def converted_balance(self, to_currency = None):
        ''' convert to currency of Wallet or currency given '''
        if to_currency == None:
            return self.amount / self.currency.rate * self.wallet.baseCurrency.rate

        else:
            to_currency = Currency.objects.get(abbreviation = to_currency)
            return self.amount / self.currency.rate * to_currency.rate 
        
class Operation(models.Model):
    ''' serves as a table keeping a history off all transactions '''
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField('Amount')
    operation_sign = models.BooleanField('Increase')
    currency = models.ForeignKey(Currency, on_delete = models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete = models.CASCADE)
    balance = models.ForeignKey(Balance, on_delete = models.CASCADE)

    def __str__(self):
        return datetime.datetime.strftime(self.timestamp, '%y-%m-%d %H:%M')

    def addToBalance(self, amount, currency_abbr = None):
        
        ''' assumes a wallet is already linked '''
        
        self.currency = self.wallet.get_CurrencyByAbbreviation(currency_abbr)
        if Balance.objects.filter(currency = self.currency, wallet = self.wallet).count() == 0:
            self.balance = Balance(currency = self.currency, wallet = self.wallet, amount = amount)
        else:
            self.balance = Balance.objects.get(currency = self.currency,wallet = self.wallet)
            self.balance.amount += amount
        self.amount = amount
        self.operation_sign = True
        self.balance.save()
        self.save()

 
