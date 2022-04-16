import numpy as np
import pandas as pd
import pandas_ta as ta

def calculateOBV(df, emaLength, signalSmoothing, power):

    df['onBalanceQuoteVolumeEMA'] = ta.ema(close=df['onBalanceQuoteVolume'], length=emaLength)
    df['obv_osc'] = (df['onBalanceQuoteVolume'] - df['onBalanceQuoteVolumeEMA'])
    df['o_ma'] = ta.ema(df['obv_osc'], length=signalSmoothing)  # tu bylo rma
    df['o_ma_s'] = ta.ema(df['o_ma'], round(pow(signalSmoothing, power)))
    df['rsi'] = ta.rsi(df['close'], length=7)

    return df[df['o_ma_s'].notnull()]