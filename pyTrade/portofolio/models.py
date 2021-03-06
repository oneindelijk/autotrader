
from django.db import models
from django.db.utils import DataError
import datetime
from .stocktools import download_ticker_dataframe
import shutil
# Create your models here.

class Company(models.Model):

    # portofolio = models.ForeignKey(Portofolio, on_delete = models.CASCADE)
    symbol = models.CharField('Symbol', max_length = 200)
    name = models.CharField('Name', max_length = 512)   
    symbol_cqs = models.CharField('CQS Symbol', max_length = 200, null=True, blank=True) 
    symbol_nasdaq = models.CharField('NASDAQ Symbol', max_length = 200, null=True, blank=True)
    etf = models.BooleanField('ETF', max_length = 200, null=True, blank=True)  
    market_category = models.CharField('Market Category', null=True, blank=True, max_length = 200) 
    last_sale = models.FloatField('Last Sale', null=True, blank=True)  
    net_change = models.FloatField('Net Change', null=True, blank=True) 
    relative_change = models.FloatField('% Change', null=True, blank=True)  
    market_cap = models.FloatField('Market Cap', null=True, blank=True)  
    country = models.CharField('Country', null=True, blank=True, max_length = 200)  
    ipo_year = models.CharField('IPO Year', null=True, blank=True, max_length = 200) 
    volume = models.FloatField('Volume', null=True, blank=True) 
    sector = models.CharField('Sector', null=True, blank=True, max_length = 200) 
    industry = models.CharField('Industry', null=True, blank=True, max_length = 200)
    favorite = models.BooleanField('Favorite', default = False)
    watched = models.BooleanField('Watched', default = False)
    marked = models.BooleanField('Marked', default = False)
    bought = models.BooleanField('Bought', default = False)
    sell = models.BooleanField('Sell', default = True)  # Sell if conditions are right, 
                                                        # specifically hold back from selling when untrue

    def __str__(self):
        return f"{self.symbol}"

    def refresh_companies(self):
        ''' refresh the list of companies listings on nasdaq '''
        dataframe = download_ticker_dataframe()
        print('Dataframe with {} rows acquired'.format(len(dataframe)))
        index_lookup = list(dataframe.keys())
        field_links = [('Security Name','name'), 
                       ('Market Category','market_category'),
                       ('ETF','etf'),
                       ('CQS Symbol','symbol_cqs'),
                       ('NASDAQ Symbol','symbol_nasdaq') ]
        ALL = Company.objects.all()
        for df_row in dataframe.itertuples():
            update = False
            QS = ALL.filter(symbol = df_row.Index)
            if QS.count() == 0:
                C = Company.objects.create(symbol = df_row.Index)
                update = True
            else:
                # update first match, even if there are more (shouldn't be)
                try:
                    C = QS[0]
                except IndexError:
                    print(df_row)
                    print(QS)
                    raise IndexError
                except DataError:
                    print('Data Error for record {} \nSkipping.'.format(df_row)) 
                else: 
                    if self.check_fields(df_row, C):
                        update = True
            if update:
                for df_field, table_col in field_links:
                    setattr(C, table_col,df_row[index_lookup.index(df_field) + 1])
                C.save()

    def check_fields(self, dataframe_row, recordset):
        ''' check if anything is different, return True if an update is needed '''
        # Todo: turn on updating of change fields
        return False

    
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

