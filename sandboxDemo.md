# Coinbase Pro Sandbox Demo

The Coinbase Pro Sandbox Demo is a Jupyter notebook file (*.ipynb)

## You need a Coinbase Pro Account and log-in to the Coinbase Pro Sandbox to get api keys and credentials:
* [Coinbase Pro Sandbox](https://public.sandbox.pro.coinbase.com/)

```
# Coinbase Sandbox Demo
#
# this demo uses the Coinbase Pro client for Python: 
# https://github.com/danpaquin/coinbasepro-python
#
# it's recommended to run cbpro in its own Python environment:
# conda create --name environment_name
#
# pip install cbpro
# or
# pip install git+git://github.com/danpaquin/coinbasepro-python.git
#
# there are a number of libraries that need to be in the python environment for this demo
# to run.  please review the import statements below and install the necessary dependencies
# before running this notebook.

import os

import cbpro

import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

import time
import numpy as np
import pandas as pd
import datetime as dt
from pylab import mpl, plt

# the Coinbase Pro Sandbox api key, secret, and passphrase have been stored locally as environment variables.
# in order to implement this project, setup a Coinbase Pro account and generate a Coinbase Pro Sandbox
# api key.  For more information go to the Coinbase Pro Sandbox Documentation url below--
# https://docs.pro.coinbase.com/#sandbox

# get current directory
dir_path = os.getcwd()

# Authentication credentials
api_key = os.environ.get('coinbaseSandboxKey')
api_secret = os.environ.get('coinbaseSandboxSecret')
passphrase = os.environ.get('coinbaseSandboxPassphrase')

# sandbox authenticated client
auth_client = cbpro.AuthenticatedClient(api_key, api_secret, passphrase, \
                                        api_url='https://api-public.sandbox.pro.coinbase.com')
# live account authenticated client
# uses a different set of API access credentials (api_key, api_secret, passphrase)
# auth_client = cbpro.AuthenticatedCliet(api_key, api_secret, passphrase)

# get accounts listed for api key
# account_info = auth_client.get_accounts()

# df = pd.DataFrame(account_info)

# df.to_csv('account_info.csv') # save data locally for development use
```
```
# get list of products

import cbpro

import pandas as pd

import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

# Define Public Client
public_client = cbpro.PublicClient()

# Get Products
products = pd.DataFrame(public_client.get_products())

products.sort_values('max_market_funds')

print(products[:10])

products.to_csv('products.csv')
```
```
# Get Historic Rates
# the max number of data points for a single request is 300 candles
# if start/end time and granularity results in more than 300 data points,
# the request will be rejected.
# Make multiple requests if fine granularity results in > 300 data points.

import cbpro

import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

# Define Public Client
public_client = cbpro.PublicClient()

# Define ticker symbol to retrieve
symbol = 'BTC-USD'

# Issue: start and end dates results in error
# Default returns 300 data points at specified granularity
# Optional parameters: start and end dates need to be in ISO 8601 format (YYYYMMDD)
#start = 20201215
#end = 20201231

# granularity is the time between ticks and must be one of these values:
# {60, 300, 900, 3600, 21600, 86400} which corresponds to
# one minute (60 sec), five minutes (300 sec), fifteen minutes (900 sec),
# one hour (3600 sec), six hours (21600 sec), and one day (86400 sec)

granularity = 86400

try:
    tick_data = pd.DataFrame(public_client.get_product_historic_rates(symbol, granularity=granularity))
except: print("Request is invalid: verify start-end dates and granularity results in less than 300 data points")

tick_data.rename(columns={0:'time', 1:'low', 2:'high', 3:'open', 4:'close', 5:'volume'}, inplace=True)

tick_data.to_csv('BTC-USD.csv')
```
```
# work with saved historic data to minimize the number of api requests

import pandas as pd

tick_data = pd.read_csv('BTC-USD.csv', index_col=0, infer_datetime_format=True, parse_dates=True)

tick_data.iloc[:, 0] = pd.to_datetime(tick_data.iloc[:, 0], infer_datetime_format=True, unit='s')

tick_data.set_index('time', inplace=True)

tick_data.sort_values(by='time', inplace=True)

data = tick_data

data.head
```
```
# Create the features data by lagging the log returns

# Adapted from Python For Finance, 2nd ed., Hilpisch, Yves.
# Chapter 16 - Automated Trading, ML-Based Trading Strategy: Vectorized Backtesting

import numpy as np
import pandas as pd

data['mid'] = (data['high']+data['low'])/2

data['returns'] = np.log(data['mid']/data['mid'].shift(1))

lags = 5

def create_lags(data):
    global cols
    cols = []
    for lag in range(1, lags + 1):
        col = 'lag_{}'.format(lag)
        data[col] = data['returns'].shift(lag)
        cols.append(col)

create_lags(data)

data.dropna(inplace=True)

data[cols] = np.where(data[cols] > 0, 1, 0)

data['direction'] = np.where(data['returns'] > 0, 1, -1)

data[cols + ['direction']].head
```
```
# A support vector machine algorithm for classification is used.
# The code trains and tests the algorithmic trading strategy based on a sequential train-test split.

# Adapted from Python For Finance, 2nd ed., Hilpisch, Yves.
# Chapter 16 - Automated Trading, ML-Based Trading Strategy: Vectorized Backtesting

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

model = SVC(C=1, kernel='linear', gamma = 'auto')

split = int(len(data) * 0.80)

train = data.iloc[:split].copy() # training dataset

model.fit(train[cols], train['direction'])

accuracy_score(train['direction'], model.predict(train[cols]))
```
```
test = data.iloc[split:].copy()  # test dataset

test['position'] = model.predict(test[cols])

accuracy_score(test['direction'], test['position'])
```
```
# Backtesting with Proportional Transaction Costs (ptc)

# Coinbase uses a maker-taker fee model.  However, for amounts < $10k the maker-taker fee is 0.50%
# The maker-taker fee model uses a pricing tier model where larger transaction volumes, in USD,
# are charged a lower percentage: 
#                                  < $10k   0.50%  (taker = maker)
#                            $50M - $100M   0.10% (taker) 0.00% (maker)

# https://help.coinbase.com/en/pro/trading-and-funding/trading-rules-and-fees/fees.html

ptc = 0.005  # 0.50%

test['strategy'] = test['position'] * test['returns']

sum(test['position'].diff() !=0)
```
```
test['strategy_tc'] = np.where(test['position'].diff() != 0,
                              test['strategy'] - ptc,
                              test['strategy'])

test[['returns', 'strategy', 'strategy_tc']].sum().apply(np.exp)
```
```
# plot results

from pylab import mpl, plt

test[['returns', 'strategy', 'strategy_tc']].cumsum().apply(np.exp).plot(figsize=(10,6))
plt.savefig('10-BTC-USD_SVM.png')
plt.show()
```
