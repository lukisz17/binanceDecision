import numpy as np
import pandas as pd
import pandas_ta as ta

def calculate4Emas(df, shortLength, mediumLength, longLength):

    df['demaShort'] = ta.dema(close=df['close'], length=shortLength)
    df['demaMedium'] = ta.dema(close=df['typicalPrice'], length=mediumLength)
    df['demaLong'] = ta.dema(close=df['typicalPrice'], length=longLength)
    df['dema100'] = ta.dema(close=df['typicalPrice'], length=80)
    df['dema200'] = ta.dema(close=df['typicalPrice'], length=150)

    return df[df['demaLong'].notnull()]