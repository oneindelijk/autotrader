
from django.db import models
import datetime
from stocktools import download_ticker_dataframe
# Create your models here.

class Company(models.Model):

    # portofolio = models.ForeignKey(Portofolio, on_delete = models.CASCADE)
    symbol = models.CharField('Symbol', max_length = 200) 
    name = models.CharField('Symbol', max_length = 200)  
    last_sale = models.FloatField('Last Sale', null=True, blank=True)  
    net_change = models.FloatField('Net Change', null=True, blank=True) 
    relative_change = models.FloatField('% Change', null=True, blank=True)  
    market_cap = models.FloatField('Market Cap', null=True, blank=True)  
    country = models.CharField('Country', max_length = 200)  
    ipo_year = models.CharField('IPO Year', max_length = 200) 
    volume = models.FloatField('Volume', null=True, blank=True) 
    sector = models.CharField('Industry', max_length = 200) 
    industry = models.CharField('Symbol', max_length = 200)
    favorite = models.BooleanField('Favorite', default = False)
    watched = models.BooleanField('Watched', default = False)
    marked = models.BooleanField('Marked', default = False)
    bought = models.BooleanField('Bought', default = False)
    sell = models.BooleanField('Sell', default = True)

    def __str__(self):
        return f"{self.name}"

    def refresh_companies(self):
        ''' refresh the list of companies listings on nasdaq '''
        dataframe = download_ticker_dataframe()

    
class StockData(models.Model):

    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    datetime = models.DateTimeField('DateTime')
    open = models.FloatField('Open', null=True, blank=True) 
    high = models.FloatField('High', null=True, blank=True) 
    low = models.FloatField('Low', null=True, blank=True) 
    close = models.FloatField('Close', null=True, blank=True) 
    volume = models.FloatField('Volume', null=True, blank=True) 

    def __str__(self):
        return '{}_{}'.format(self.company.name,self.datetime.strftime('%Y/%m/%d %T'))
class Statistic(models.Model):

    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    title = models.CharField('Title', max_length = 200)
    range_lower = models.DateTimeField('From')
    range_upper = models.DateTimeField('Until')
    min = models.FloatField('Minimum', default = 0)
    max = models.FloatField('Maximum', default = 0)
    Q1 = models.FloatField('25 %', default = 0)
    Q2 = models.FloatField('50 %', default = 0)
    Q3 = models.FloatField('75 %', default = 0)

    def __str__(self):
        return '{}:{}-{}'.format(self.company.name,self.range_lower.strftime('%Y/%m/%d %T'),self.range_upper.strftime('%Y/%m/%d %T'))

class Portofolio(models.Model):

    owner = models.CharField('Owner', max_length = 200)
    updated = models.DateTimeField(auto_now_add=True)
    api_key = models.CharField('Api Key', max_length = 200, blank=True) 
    initial_balance = models.FloatField('Initial Balance', null=True, blank=True)  

    def __str__(self):
        return f"{self.owner}'s Portofolio"

class Balance(models.Model):
    ''' keeps track of balance per Company in Portofolio '''
    portofolio = models.ForeignKey(Portofolio, on_delete = models.CASCADE)
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    amount = models.FloatField('Amount', default = 0)

    def __str__(self):
        totalstr = '[{}]{} {:0.2f}'.format(self.portofolio.id, self.company.symbol, self.amount)
        return totalstr

class Operation(models.Model):
    ''' serves as a table keeping a history off all transactions '''
    balance = models.ForeignKey(Balance, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField('Amount')
    price = models.FloatField('Price')
    operation_sign = models.BooleanField('Increase')

    def __str__(self):
        sign = '' if self.operation_sign else '-'
        return '{}{}'.format(sign,datetime.datetime.strftime(self.timestamp, '%y-%m-%d %H:%M'))

