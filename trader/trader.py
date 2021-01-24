'''
# Tenzin Trader
# https://github.com/wchen38/tenzin

# run from project root directory:
    C:/Users/user/tenzin>ipython -i ./trader/trader.py

# requires ipython to be configured to use matplotlib
# https://ipython.readthedocs.io/en/stable/interactive/plotting.html
'''
import os
import cbpro
import time
from tech_indicators import net_returns, rsi
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def viz(x, y1, y2, symbol):
    fig, axs = plt.subplots(2, 1, figsize=(10,6))
    plt.subplots_adjust(hspace=0.3)
    locator = mdates.AutoDateLocator(minticks=5, maxticks=30)
    formatter = mdates.ConciseDateFormatter(locator)

    axs[0].set_title(symbol+' Price')
    axs[0].xaxis.set_major_locator(locator)
    axs[0].xaxis.set_major_formatter(formatter)
    # transpose data for boxplots (i.e. candle plots)
    y1_transposed = y1.T
    axs[0].boxplot(y1_transposed, whis=[0,100])
    axs[0].set_ylabel('Price')
    axs[0].grid(True)

    axs[1].set_title('RSI')
    axs[1].xaxis.set_major_locator(locator)
    axs[1].xaxis.set_major_formatter(formatter)
    axs[1].plot(x, y2)
    axs[1].set_xlabel('Date')
    axs[1].set_ylabel('RSI')
    axs[1].grid(True)

    plt.show()
    return


def portfolio(symbol, df_accounts, df_fills):
    '''
    Portfolio is a minimal example that plots the equity curve
    for the cryptocurrency being traded.
    Future improvements could include:
        plotting multiple cryptocurrencies
        portfolio gain/loss
    '''
    # datetime for request to Coinbase
    from datetime import datetime
    from datetime import timedelta

    granularity = 21600              # Coinbase specified time interval
    delta = timedelta(days=40)       # time before now, max: days = 50
    start = datetime.now() - delta
    start = start.isoformat()        # convert to ISO 8601 format
    now = datetime.now().isoformat()

    data = auth_client.get_product_historic_rates(symbol, start=start, end=now, \
    granularity=granularity)
    ''' Coinbase uses granularity to specify the time interval 'tick'
    granularity is a tick in seconds.  Allowable values are 60, 300, 900, 3600,
    21600, and 86400.
    seconds       minutes    hours
        60           1
       300           5
       900          15
      3600          60          1
     21600         360          6
     86400        1440         24
    '''
    df = pd.DataFrame(data)
    '''
    historic_rates format:
    0       1       2       3       4       5
    time    low     high    open    close   volume
    '''
    df.rename(columns={0:'time', 1:'low', 2:'high', 3:'open', \
    4:'close', 5:'volume'}, inplace=True)

    pd.to_datetime(df['time'], infer_datetime_format=True)

    # save historic_rates data
    path = os.path.dirname(__file__)
    now = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    filepath = os.path.join(path, 'historic_rates-{}.csv'.format(now))
    df.to_csv(filepath)

    returns = net_returns(df)

    window = 5
    rsi_crypto = rsi(returns, window)

    x = -window*3
    price = df[['open', 'close', 'low', 'high']]
    viz(df.index[x:], price.iloc[x:], rsi_crypto.iloc[x:], symbol)

    return


def trading(twentyfour, symbol, amount, df_accounts, df_fills):
    print('')
    print('*'*50)
    print('***   Welcome to Tenzin Cryptocurrency Trader  ***')
    print('*'*50)
    print('')
    print('Trading: ', symbol)
    print('Amount per trade: ', amount)
    print('')
    print('Last 24 hrs:')
    print('')
    print('Open: .........', twentyfour['open'])
    print('Last: .........', twentyfour['last'])
    print('High: .........', twentyfour['high'])
    print('Low:    .......', twentyfour['low'])
    print('Volume:  ......', twentyfour['volume'])
    print('30 day Volume: ', twentyfour['volume_30day'])
    print('')
    print('Recent orders: ')
    print(df_fills.loc[-3:,['product_id', 'fee', 'side', 'settled', 'usd_volume']])
    print('')
    print('Account Positions: ')
    print(df_accounts[['currency', 'balance']])
    print('')

    # initialize variables
    trading = 'n'
    signal = 0         # signal to take action- buy = 1, sell = -1
    trade = 0          # last trade made- buy = 1, sell = -1
    portfolio = 'n'    # analyze porfolio Y/n

    trading = input("Start trading? [Y]/[n]:")

    if trading == 'n':
        folio_analyze = input("Analyze portfolio? [Y]/[n]:")

    if folio_analyze == 'Y':
        return
    else:
        print('*** Tenzin trading session ended ***')
        exit

    while trading == 'Y':
        print('Current amount per trade in USD: $', amount)
        change_amt = input('Change amount to trade? [Y]/[n]:')
        if change_amt == 'Y':
            amount = input('Enter a new amount to trade in USD: $')
        else:
            print('Trading amount not changed USD: $', amount)

        buy = input("Buy? [Y]/[n]:")
        if buy == 'Y':
            signal = 1
        else:
            sell = input("Sell? [Y]/[n]:")
            if sell == 'Y':
                signal = -1
            else:
                signal = 0

        if signal == 1:
            auth_client.place_market_order(product_id = symbol, side = 'buy',\
            funds = amount)
            trade = 1
            time.sleep(3) # rate limited to 4 sec per request
        elif signal == -1:
            auth_client.place_market_order(product_id = symbol, side = 'sell',\
            funds = amount)
            trade = -1
            time.sleep(3) # rate limited to 4 sec per request

        trading = input("Continue trading? [Y]/[n]:")


if __name__ == '__main__':
    # Authentication credentials
    api_key = os.environ.get('CB_SANDBOX_KEY')
    api_secret = os.environ.get('CB_SANDBOX_SECRET')
    passphrase = os.environ.get('CB_SANDBOX_PASSPHRASE')

    # sandbox authenticated client
    auth_client = cbpro.AuthenticatedClient(api_key, api_secret, passphrase, \
                                            api_url='https://api-public.sandbox.pro.coinbase.com')
    # live account authenticated client
    # uses a different set of API access credentials (api_key, api_secret, passphrase)
    # auth_client = cbpro.AuthenticatedCliet(api_key, api_secret, passphrase)

    symbol = 'BTC-USD'
    amount = 100        # amount to be traded in $USD

    # datetime stamp for filenames
    date = datetime.now()
    now = date.strftime("%Y-%m-%d-%H%M%S")

    # orders & fills generators to report positions:
    orders_gen = auth_client.get_orders()
    fills_gen = auth_client.get_fills(product_id=symbol)

    # Get stats for the last 24 hrs
    twentyfour = auth_client.get_product_24hr_stats(symbol)

    # File path to save data to
    path = os.path.dirname(__file__)

    # Get filled orders
    all_fills = list(fills_gen)
    df_fills = pd.DataFrame(all_fills)
    df_fills = df_fills.round(3)
    #filepath = os.path.join(path, 'fills-{}.csv'.format(now))
    #df_fills.to_csv(filepath)

    # Get account positions
    accounts = auth_client.get_accounts()
    df_accounts = pd.DataFrame(accounts)
    df_accounts = df_accounts.round(3)
    #filepath = os.path.join(path, 'accounts-{}.csv'.format(now))
    #df_accounts.to_csv(filepath)

    # Start trading
    trading(twentyfour, symbol, amount, df_accounts, df_fills)

    # Analyze Portfolio
    portfolio(symbol, df_accounts, df_fills)

    # End session?
    tradeMore = input('Continue trading? [Y]/[n]:')
    if tradeMore == 'Y':
        trading(twentyfour, symbol, amount, df_accounts, df_fills)
    else:
        print('*** Tenzin trading session ended ***')
        exit


    '''
    Live feed for price updates - needs debugging

    # Coinbase Pro web socket connection is rate-limited to 4 seconds per request per IP.
    wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com", products=symbol, channels=["ticker"], \
                                     should_print=False)
    wsClient.start()

    try:
        while True:
            wsClient.on_message((trading,))
    except KeyboardInterrupt:
        wsClient.close()

    if wsClient.error:
        print('Error - stopping program')
        wsClient.close()
        sys.exit(1)
    else:
        sys.exit(0)
    '''
