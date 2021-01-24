'''
# Technical Indicators Libary calculates:
# rsi, net returns
# convenience function: fillinValues()
'''
import pandas as pd
import numpy as np

def fillinValues(dataframe):
    # fill in NaN values
    dataframe.fillna(method='ffill', inplace=True)
    dataframe.fillna(method='bfill', inplace=True)
    return dataframe

def net_returns(df):
    '''
    Net return(t) = Price(t)/Price(t-1) - 1
    from: page 13, Machine Trading by Chan, E.P.

    returns an instrument's net return

    df is a dataframe that needs to be in the following format:
    index        0    1     2   3    4
    YYYY-MM-DD   open close low high volume
    '''
    price = df['close']
    rets = price/price.shift(1)-1
    # fill in NaN values
    rets = fillinValues(rets)
    return rets

def rsi(rets, window):
    '''
    RSI: Relative Strength Index
        RSI = 100 - (100/(1+RS))
        RS = (avg of x days' up closes)/(avg of x days' down closes)

        avg of x days' up closes = total points gained on up days/weeks divide by x days/weeks
        avg of x days' down closes = total points lost on down days/weeks divide by x days/weeks

        from: page 239 Technical Analysis of the Financial Markets, 1st ed. by Murphy, John J.

        rets are the net returns. use function net_returns() to calculate.

        window is x days for the moving average calculation

    returns a series of RSI values
    '''
    # date_range is used to reindex after separating days up from days down
    date_range = rets.index
    up = rets.loc[rets.iloc[:] >= 0.0]
    up = up.reindex(date_range, fill_value = 0.0)
    #save_data('up', up)

    up_avg = up.rolling(window=window).mean()

    up_avg = up_avg.fillna(value = 0.0)
    #save_data('up_avg', up_avg)
    down = rets.loc[rets.iloc[:] < 0.0]
    down = down.reindex(date_range, fill_value = 0.0)
    #save_data('down', down)

    down_avg = down.rolling(window=window).mean()*-1

    down_avg = down_avg.fillna(value = 0.0)
    # replace 0s with 1s
    down_avg.replace(to_replace = 0.0, value = 1.0)
    #save_data('down_avg', down_avg)
    # calculate rsi
    rs = up_avg/down_avg
    rsi = 100 - (100/(1+rs))
    rsi = rsi.to_frame()
    rsi.rename(columns={0:'RSI'}, inplace=True)
    rsi.set_index(date_range, inplace=True)
    rsi.fillna(value=1.0, inplace=True)
    #save_data('rsi_SPY', rsi)
    return rsi
