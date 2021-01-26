#Todo get url from settings
import shutil
import pandas_datareader as pdr
trade_symbols_url = 'https://www.nasdaq.com/market-activity/stocks/screener?exchange=NYSE&render=download'

def download_ticker_data(dl_url):
    ''' download csv to temporary folder  
        !!! werkt niet via deze link !!!
    ''' #TODO
    tempfolder = '/tmp/autotrade_donwload_temp'
    # remove folder is it exists
    if shutil.os.path.exists(tempfolder):
        shutil.os.removedirs(tempfolder)
    # (re)create folder
    shutil.os.makedirs(tempfolder)
    command = 'wget -P {destination} {url}'.format(
        destination = tempfolder,
        url = dl_url
    )
    shutil.os.system(command)
    return shutil.os.listdir(tempfolder)[0]

def download_ticker_dataframe():
    return pdr.nasdaq_trader.get_nasdaq_symbols()

def import_ticker_list(dataframe = None):
    ''' import trade symbols from a nasdaq csv downloaded file '''
    if dataframe == None:
        dataframe = download_ticker_dataframe()

    for row in dataframe.itertuples():
        symbol = row[1] 
        self.tickerdata[row[1]] = {}
        for i, r in enumerate(cols):
            self.tickerdata[symbol].update({r: row[i + 1]})
        if 'Last Sale' in self.tickerdata[symbol]:
            SaleStr = self.tickerdata[symbol]['Last Sale']
            try:
                self.tickerdata[symbol]['last_sale'] = float(SaleStr.strip('$'))
            except:
                self.tickerdata[symbol]['last_sale'] = -1
        if '% Change' in self.tickerdata[symbol]:
            percent_change = self.tickerdata[symbol]['% Change']
            try:
                self.tickerdata[symbol]['percent_change'] = float(percent_change.strip('$'))
            except:
                self.tickerdata[symbol]['percent_change'] = 100
    self.save()
    