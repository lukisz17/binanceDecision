import numpy as np
import pandas as pd
import pandas_ta as ta

def calculateDMI(df):
    adx = ta.adx(close=df['close'], high=df['high'], low=df['low'])
    df['DMP'] = ta.ema(adx['DMP_14'], length=24)
    df['DMN'] = ta.ema(adx['DMN_14'], length=24)  # to 14 i  24 musi byc parametrem
    df['ADX'] = adx['ADX_14']

    dfN = ta.psar(df['DMN'], df['DMN'])  # tutaj to tez musza byc parametry
    dfP = ta.psar(df['DMP'], df['DMP'])  # tutaj to tez musza byc parametry

    df['PSARDMN'] = dfN['PSARl_0.02_0.2']
    df['PSARDMP'] = dfP['PSARl_0.02_0.2']

    df['DMP_BUY'] = df['DMP'] > df['PSARDMP']
    df['DMN_BUY'] = df['DMN'] < df['PSARDMN']

    df['DMP_SELL'] = df['DMP'] < df['PSARDMP']
    df['DMN_SELL'] = df['DMN'] > df['PSARDMN']

    return df